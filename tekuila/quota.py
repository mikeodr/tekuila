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

from __future__ import print_function
import os
import sys
import json
import configobj
import argparse
# Support both python 2 and 3
try:
    import httplib
except:
    import http.client as httplib
import errno

API_URL = '/web/Usage/UsageSummaryRecords?$filter=IsCurrent%20eq%20true'
CONFIG_PATH = '~/.tekuila'


class Tekuila:
    """Parse the ISP quota API and act upon the results. """
    def __init__(self, apikey=None, cap=None, warn_ratio=None,
                 verbose=False):
        """Construct a new fetch/parser to check cap and warn levels.

        :param apikey: API key for TekSavvy, acquired from
            https://myaccount.teksavvy.com/ApiKey/ApiKeyManagement
        :param cap: Your cap in GB
        :param warn: The ratio you would like a warning to be returned from
            `check_cap` in 0.0 to 1.0 ratio.
        :param verbose: Boolean, True to print output.
        """
        self.api = apikey
        self.cap = cap
        self.warn_ratio = warn_ratio
        self.verbose = verbose
        self.data = None
        self.download_total = None

        if self.warn_ratio is not None:
            self.warn_ratio = float(self.warn_ratio)
        if self.cap is not None:
            self.cap = float(self.cap)

    def load_config(self, config_path=CONFIG_PATH, override=False):
        """Loads in the config file from config path provided, looking
        for api key, cap limit and warn limit.

        :param config: Path to config file to parse for API key, warn and cap
            variables.
        :param override: Boolean to override values passed on ``__init__``.
            True to replace all, false to replace those that are None.
        """
        api = None
        cap = None
        warn_ratio = None

        path = os.path.expanduser(config_path)

        if os.path.isfile(path):
            config = configobj.ConfigObj(path)

            if "API" in config:
                api = config["API"]
            if "CAP" in config:
                cap = float(config["CAP"])
            if "WARN_RATIO" in config:
                warn_ratio = float(config["WARN_RATIO"])

            if override is True:
                self.api = api
                self.cap = cap
                self.warn_ratio = warn_ratio
            else:
                if self.api is None:
                    self.api = api
                if self.cap is None:
                    self.cap = cap
                if self.warn_ratio is None:
                    self.warn_ratio = warn_ratio

        else:
            print("Config file does not exist.", file=sys.stderr)

    def fetch_data(self):
        """Pull JSON data from TekSavvy api url using API key pulled from config
        file set by user.
        """
        if self.api is None:
            print("No API key provided", file=sys.stderr)
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

        :returns: True if exceeded False otherwise.
        """
        if self.cap is not None:
            if self.download_total > self.cap:
                print("Cap exceeded", self.download_total, "/", self.cap)
                return True
            else:
                return False

    def check_warn(self):
        """If cap and warn limit are set, check if the user has passed the set
        threshold set in the config file.

        :returns: True if exceeded, False otherwise.
        """
        if self.cap is not None and self.warn_ratio is not None:
            if (self.download_total / self.cap) >= self.warn_ratio:
                print("Warn level exceeded.")
                return True
            else:
                return False

    def print_data(self, verbose=False):
        """Prints the data pulled from the JSON results. Can be forced or
        defaulted to print if `verbose` is set in `__init__`

        :param verbose: Print details.
        """
        if self.data is not None:
            peakdl = self.data["value"][0]["OnPeakDownload"]
            peakul = self.data["value"][0]["OnPeakUpload"]
            offpeakdl = self.data["value"][0]["OffPeakDownload"]
            offpeakul = self.data["value"][0]["OffPeakUpload"]
            startdate = self.data["value"][0]["StartDate"]
            enddate = self.data["value"][0]["EndDate"]

            if self.verbose or verbose:
                print("OnPeakDownload:", peakdl)
                print("OnPeakUpload:", peakul)
                print("OffPeakDownload:", offpeakdl)
                print("OffPeakUpload:", offpeakul)
                print("Start Date:", startdate)
                print("End Date:", enddate)


def main():
    """Main function to parse args and call init of Tekuila class.
    Also calls all necessary functions if run as a command line application.

    :returns: EOK on no errors and under the cap/warn settings.
        Otherwise non-zero when errors or over cap level.
    """
    ret = 0  # EOK
    parse = argparse.ArgumentParser(description='Check TekSavvy Cap')
    parse.add_argument("-c", "--config", help="Alternative config file")
    parse.add_argument("--cap", help="Your cap in GB, causes nonzero return"
                                     " code if exceeded")
    parse.add_argument("--api", help="API Key")
    parse.add_argument("--warn", help="Warn ratio against data cap, "
                                      "causes nonzero return code if exceeded"
                                      ", in range 0.1 to 1.0")
    parse.add_argument("-v", "--verbose", action="store_true",
                       help="Show output, don't just use return code")

    args = parse.parse_args()

    tekq = Tekuila(args.api, args.cap, args.warn, args.verbose)
    if args.config is not None:
        tekq.load_config(args.config)
    else:
        tekq.load_config()

    tekq.fetch_data()
    tekq.print_data()

    # Check if over ratio/cap
    cap_warn = tekq.check_cap()
    ratio_warn = tekq.check_warn()

    if cap_warn or ratio_warn:
        ret = errno.ENOMEM  # "You've had to much to download!"

    return ret
