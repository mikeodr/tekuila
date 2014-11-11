#!/usr/bin/env python

import os
import json
import configobj
import argparse
import httplib
import errno

API_URL = '/web/Usage/UsageSummaryRecords?$filter=IsCurrent%20eq%20true'
CONFIG_PATH = '~/.tekquota'


class TekQuota():
    def __init__(self, args):
        self.API = None
        self.cap = None
        self.warn_ratio = None
        self.verbose = False
        self.config_path = CONFIG_PATH
        self.load_config()

        data = self.fetchData()
        self.printData(data)

    def load_config(self):
        if args.config is not None:
            path = args.config
        else:
            path = os.path.expanduser('~/.tekquota')

        if os.path.isfile(path):
            config = configobj.ConfigObj(path)
            self.API = config["API"]
        else:
            print "Config file does not exist"
            return errno.ENOENT

        # Allow override with args
        if args.API is not None:
            self.API = args.API
        if args.cap is not None:
            self.cap = args.cap
        if args.warn is not None:
            self.warn_ratio = args.warn
        self.verbose = args.verbose

    def fetchData(self):
        if self.API is None:
            print "No API key provided"
            return errno.ENOENT

        headers = {"TekSavvy-APIKey": self.API}
        conn = httplib.HTTPSConnection("api.teksavvy.com")
        conn.request('GET',
                     API_URL,
                     '', headers)
        response = conn.getresponse()
        jsonData = response.read()
        data = json.loads(jsonData)
        return data

    def printData(self, data):
        pd = data["value"][0]["OnPeakDownload"]
        pu = data["value"][0]["OnPeakUpload"]
        opd = data["value"][0]["OffPeakDownload"]
        opu = data["value"][0]["OffPeakUpload"]
        sd = data["value"][0]["StartDate"]
        ed = data["value"][0]["EndDate"]

        if self.verbose:
            print "OnPeakDownload: %s" % (pd)
            print "OnPeakUpload: %s" % (pu)
            print "OffPeakDownload: %s" % (opd)
            print "OffPeakUpload: %s" % (opu)
            print "Start Date: %s" % (sd)
            print "End Date: %s" % (ed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check TekSavvy Cap')
    parser.add_argument("-c", "--config", help="Alternative config file")
    parser.add_argument("--cap", help="Your cap in GB")
    parser.add_argument("--API", help="API Key")
    parser.add_argument("--warn", help="Warn ratio against data cap, "
                                       "causes nonzero return code")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show output, don't just use return code")

    args = parser.parse_args()
    TekQuota(args)
