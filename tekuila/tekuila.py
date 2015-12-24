#!/usr/bin/env python
"""
tekuila.py
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
import abc
import os
import configobj

CONFIG_PATH = '~/.tekuila'


class Tekuila(object):
    """Base class for parsing the ISP quota API and act upon the results."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, apikey=None, cap=None, warn_ratio=None,
                 verbose=False):
        """Construct a new fetch/parser to check cap and warn levels.

        :param apikey: API key for ISP
        :param cap: Your cap in GB
        :param warn: The ratio you would like a warning to be returned from
            `check_cap` in 0.0 to 1.0 ratio.
        :param verbose: Boolean, True to print output.
        """
        self.api_key = apikey
        self.cap = cap
        self.warn_ratio = warn_ratio
        self.verbose = verbose
        self.data = None
        self.download_total = None

        if self.warn_ratio is not None:
            self.warn_ratio = float(self.warn_ratio)
        if self.cap is not None:
            self.cap = float(self.cap)

    def get_api_key(self):
        return self.api_key

    def get_warn_ratio(self):
        return self.warn_ratio

    def get_cap(self):
        return self.cap

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
                if self.api_key is None:
                    self.api_key = api
                if self.cap is None:
                    self.cap = cap
                if self.warn_ratio is None:
                    self.warn_ratio = warn_ratio

    @abc.abstractmethod
    def fetch_data(self):
        """Child class must implement.
        Fetches the data from the ISPs API URI
        and set's appropriate values see set_download_data.
        """
        raise NotImplementedError('Fetch Method not implemented!')

    @abc.abstractmethod
    def print_data(self, verbose=False):
        """Child class must implement.
        Prints the data pulled from the ISP
        results fetched from the API. Can be forced or defaulted to print if
        `verbose` is set in `__init__`

        :param verbose: Print details.
        """
        raise NotImplementedError('Print Method not implemented!')

    def set_download_total(self, total):
        """Set the total current download as it contributes towards the ISPs
        cap quota.

        :param total: The number of GBs downloaded ex: 33.23
        """
        self.download_total = total

    def check_cap(self, verbose=False):
        """Check if cap exists, if so check if download total has been exceeded
        based on fetched results.

        :param verbose: Force print and warnings or errors.
        :returns: True if exceeded False otherwise.
        """
        if self.cap is not None:
            if self.download_total > self.cap:
                if self.verbose or verbose:
                    print("Cap exceeded", self.download_total, "/", self.cap)
                return True
            else:
                return False

    def check_warn(self, verbose=False):
        """If cap and warn limit are set, check if the user has passed the set
        threshold set in the config file.

        :param verbose: Force print any warnings or errors.
        :returns: True if exceeded, False otherwise.
        """
        if self.cap is not None and self.warn_ratio is not None:
            if (self.download_total / self.cap) >= self.warn_ratio:
                if self.verbose or verbose:
                    print("Warn level exceeded.")
                return True
            else:
                return False
