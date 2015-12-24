#!/usr/bin/env python
"""
teksavvy.py
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
import sys
import errno
import json
try:
    from tekuila import Tekuila
except ImportError:
    from .tekuila import Tekuila

# Support both python 2 and 3
try:
    import httplib
except ImportError:
    import http.client as httplib


class Teksavvy(Tekuila):
    """Parse implementation for TekSavvy API"""
    API_URL = '/web/Usage/UsageSummaryRecords?$filter=IsCurrent%20eq%20true'

    def __init__(self, apikey=None, cap=None, warn_ratio=None, verbose=False):
        super(self.__class__, self).__init__(apikey, cap, warn_ratio, verbose)
        self.data = None

    def fetch_data(self):
        """Pull JSON data from TekSavvy api url using API key pulled from config
        file set by user.
        """
        if self.get_api_key() is None:
            print("No API key provided", file=sys.stderr)
            return errno.ENOENT

        headers = {"TekSavvy-APIKey": self.get_api_key()}
        conn = httplib.HTTPSConnection("api.teksavvy.com")
        conn.request('GET',
                     Teksavvy.API_URL,
                     '', headers)
        response = conn.getresponse()
        json_data = response.read()
        self.data = json.loads(json_data.decode(encoding='UTF-8'))
        self.set_download_total(float(self.data["value"][0]["OnPeakDownload"]))

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
                print("On Peak Download: %s GB" % peakdl)
                print("On Peak Upload: %s GB" % peakul)
                print("Off Peak Download: %s GB" % offpeakdl)
                print("Off Peak Upload: %s GB" % offpeakul)
                print("Start Date:", startdate)
                print("End Date:", enddate)
