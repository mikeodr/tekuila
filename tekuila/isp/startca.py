#!/usr/bin/env python
"""
startca.py
Fetch and act upon your ISPs quota limits.

Copyright (C) 2018  Mike O'Driscoll <mike@mikeodriscoll.ca>

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
import http.client as httplib
from json import loads, dumps
import sys
import xmltodict
from tekuila.tekuila import Tekuila
from xml.parsers.expat import ExpatError


class StartCA(Tekuila):
    """Fetch and parse Start.ca quota API"""
    API_URL = '/account/usage/api?key='

    def __init__(self, apikey=None, cap=None, warn_ratio=None, verbose=False):
        super(self.__class__, self).__init__(apikey, cap, warn_ratio, verbose)
        self._data = None

    def fetch_data(self):
        """Pull XML data from Start.ca API url using API key.
        Store it within the class for processing.
        """
        if self.api_key is None:
            print("No API key provided", file=sys.stderr)
            return None

        conn = httplib.HTTPSConnection("www.start.ca")
        conn.request('GET',
                     self.API_URL + self.api_key)
        response = conn.getresponse()
        if response.status == httplib.OK:
            xml_data = response.read()
            try:
                self._data = xmltodict.parse(xml_data)
            except ExpatError:
                return None
            download_total = self._data['usage']['used']['download']
            download_total = self.b_to_GB(float(download_total))
            self._download_total = download_total
            return loads(dumps(self._data))
        else:
            print("Data fetch failed. HTTP: %s" % response.reason, file=sys.stderr)
            return None

    @staticmethod
    def b_to_GB(value):
        """Convert from bytes to GB.

        :param value: The value in bytes to convert to GB.
        :return: Converted GB value
        """
        return float(value) * 10 ** -9

    def print_data(self, verbose=False):
        """Prints the data pulled from the JSON results. Can be forced or
        defaulted to print if `verbose` is set in `__init__`

        :param verbose: Print details.
        """
        if self._data is not None:
            used_dl = self.b_to_GB(self._data['usage']['used']['download'])
            used_ul = self.b_to_GB(self._data['usage']['used']['upload'])
            grace_dl = self.b_to_GB(self._data['usage']['grace']['download'])
            grace_ul = self.b_to_GB(self._data['usage']['grace']['upload'])
            total_dl = self.b_to_GB(self._data['usage']['total']['download'])
            total_ul = self.b_to_GB(self._data['usage']['total']['upload'])

            if self.verbose or verbose:
                print("Used Download: %s GB" % used_dl)
                print("Used Upload: %s GB" % used_ul)
                print("Grace Download: %s GB" % grace_dl)
                print("Grace Upload: %s GB" % grace_ul)
                print("Total Download: %s GB" % total_dl)
                print("Total Upload: %s GB" % total_ul)
