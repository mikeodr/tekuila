#!/usr/bin/env python

import json
import ConfigParser
import argparse
import httplib

API_URL = '/web/Usage/UsageSummaryRecords?$filter=IsCurrent%20eq%20true'

def checkCap(args):
    config = ConfigParser.ConfigParser()
    APIKEY = None
    # cap = None
    # warn = None
    if args.config is None:
        pass

    if args.API is None:
        APIKEY = args.API
    if args.cap is None:
        pass
    if args.warn is None:
        pass

    APIKEY = "75C4166BF10C74715DB7E2B3BE365325"

    headers = {"TekSavvy-APIKey": APIKEY}
    conn = httplib.HTTPSConnection("api.teksavvy.com")
    conn.request('GET',
                 API_URL,
                 '', headers)
    response = conn.getresponse()
    jsonData = response.read()

    data = json.loads(jsonData)
    pd  = data["value"][0]["OnPeakDownload"]
    pu  = data["value"][0]["OnPeakUpload"]
    opd = data["value"][0]["OffPeakDownload"]
    opu = data["value"][0]["OffPeakUpload"]
    sd  = data["value"][0]["StartDate"]
    ed  = data["value"][0]["EndDate"]

    if args.verbose:
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
    parser.add_argument("--warn", help="Warn ratio, causes nonzero"
                                       " return code")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show output, don't just use return code")

    args = parser.parse_args()

    checkCap(args)
