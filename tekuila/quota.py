#!/usr/bin/env python
"""
quota.py
Fetch and act upon your ISPs quota limits.

Copyright (C) 2014  Mike O'Driscoll <mike@mikeodriscoll.ca>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import os
import json
import configobj
import argparse
import httplib
import errno

API_URL = '/web/Usage/UsageSummaryRecords?$filter=IsCurrent%20eq%20true'
CONFIG_PATH = '~/.tekuila'


class Tekuila():
    """Class for parsing ISP quota API and acting upon the results."""
    def __init__(self, args):
        self.api = None
        self.cap = None
        self.data = None
        self.download_total = None
        self.warn_ratio = None
        self.verbose = False
        self.config_path = CONFIG_PATH
        self.args = args

        self.load_config()
        self.fetch_data()
        self.print_data()

    def load_config(self):
        """Loads in the config file from CONFIG_PATH looking for api key, cap
        limit and warn limit.
        """
        if self.args.config is not None:
            path = self.args.config
        else:
            path = os.path.expanduser('~/.tekquota')

        if os.path.isfile(path):
            config = configobj.ConfigObj(path)

            if "API" in config:
                self.api = config["API"]
            if "CAP" in config:
                self.cap = float(config["CAP"])
            if "WARN_RATIO" in config:
                self.warn_ratio = float(config["WARN_RATIO"])
        else:
            print "Config file does not exist"

        # Allow override with args
        if self.args.API is not None:
            self.api = self.args.API
        if self.args.cap is not None:
            self.cap = self.args.cap
        if self.args.warn is not None:
            self.warn_ratio = self.args.warn
        self.verbose = self.args.verbose

    def fetch_data(self):
        """Pull JSON data from ISP api url using API key pulled from config
        file set by user.
        """
        if self.api is None:
            print "No API key provided"
            return errno.ENOENT

        headers = {"TekSavvy-APIKey": self.api}
        conn = httplib.HTTPSConnection("api.teksavvy.com")
        conn.request('GET',
                     API_URL,
                     '', headers)
        response = conn.getresponse()
        json_data = response.read()
        self.data = json.loads(json_data)
        self.download_total = float(self.data["value"][0]["OnPeakDownload"])

    def check_cap(self):
        """Check if cap exists, if so check if download total has been exceeded
        based on fetched results.
        returns True if exceeded false otherwise.
        """
        if self.cap is not None:
            if self.download_total > self.cap:
                print "Cap exceeded"
                return True
            else:
                return False

    def check_warn(self):
        """If cap and warn limit are set, check if the user has passed the set
        threshold set in the config file.
        returns True if exceeded, false otherwise.
        """
        if self.cap is not None and self.warn_ratio is not None:
            if (self.download_total/self.cap) > self.warn_ratio:
                print "Warn level exceeded"
                return True
            else:
                return False

    def print_data(self):
        """Prints the data pulled from the JSON results."""
        peakdl = self.data["value"][0]["OnPeakDownload"]
        peakul = self.data["value"][0]["OnPeakUpload"]
        offpeakdl = self.data["value"][0]["OffPeakDownload"]
        offpeakul = self.data["value"][0]["OffPeakUpload"]
        startdate = self.data["value"][0]["StartDate"]
        enddate = self.data["value"][0]["EndDate"]

        if self.verbose:
            print "OnPeakDownload: %s" % (peakdl)
            print "OnPeakUpload: %s" % (peakul)
            print "OffPeakDownload: %s" % (offpeakdl)
            print "OffPeakUpload: %s" % (offpeakul)
            print "Start Date: %s" % (startdate)
            print "End Date: %s" % (enddate)


def main():
    PARSER = argparse.ArgumentParser(description='Check TekSavvy Cap')
    PARSER.add_argument("-c", "--config", help="Alternative config file")
    PARSER.add_argument("--cap", help="Your cap in GB")
    PARSER.add_argument("--API", help="API Key")
    PARSER.add_argument("--warn", help="Warn ratio against data cap, "
                                       "causes nonzero return code")
    PARSER.add_argument("-v", "--verbose", action="store_true",
                        help="Show output, don't just use return code")

    ARGS = PARSER.parse_args()
    TQ = Tekuila(ARGS)
    TQ.check_cap()
    TQ.check_warn()
