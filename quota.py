#!/usr/bin/env python

import urllib2
import json
import ConfigParser
import argparse


def checkCap():
    APIKEY = "75C4166BF10C74715DB7E2B3BE365325"
    proto = 'https://'
    host = 'api.teksavvy.com'
    path = "/web/Usage/UsageSummaryRecords?$filter=IsCurrent%20eq%20true"
    url = proto + host + path

    request = urllib2.Request(url)
    request.add_header('TekSavvy-APIKey', APIKEY)

    js = json.load(urllib2.urlopen(request))
    # jd = json.dumps(js)

    results = js["value"][0]

    for k in results:
        if "Download" in k:
            v = str(results[k])
            line = k + ' is ' + v.rjust(6, '0') + 'GB'
            newline = "{0} is {1}".format(k, v)
            print line.rjust(28)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check TekSavvy Cap')
    parser.add_argument("--cap", help="Cap in GB")
    parser.add_argument("--API", help="API Key")
    parser.add_argument("--warn", help="Warn ratio, causes nonzero"
                        " return code")
    parser.add_argument("-v", "--verbose", help="Show output, don't just use"
                        " return code")

    args = parser.parse_args()

    checkCap()
