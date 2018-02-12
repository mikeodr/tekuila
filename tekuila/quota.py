"""
quota.py
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
import argparse
import sys
from pkg_resources import get_distribution
try:
    from tekuila.isp.startca import StartCA
    from tekuila.isp.teksavvy import Teksavvy
except ImportError:
    from isp.startca import StartCA
    from isp.teksavvy import Teksavvy


def main():
    """Main function to parse args and call init of Tekuila API class.
    Also calls all necessary functions if run as a command line application.

    :returns: EOK on no errors and under the cap/warn settings.
        Otherwise non-zero when errors or over cap level.
    """

    ver = get_distribution('tekuila').version
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
    parse.add_argument("-s", "--startca", action="store_true",
                       help="Use StartCA instead of TekSavvy API")
    parse.add_argument('--version', action='version', version='%(prog)s ' + ver)

    args = parse.parse_args()

    api = None
    # Select the API to use
    if args.startca:
        api = StartCA(args.api, args.cap, args.warn, args.verbose)
    else:
        api = Teksavvy(args.api, args.cap, args.warn, args.verbose)

    if api is not None:
        if args.config is not None:
            api.load_config(args.config)
        else:
            api.load_config()

        if not api.fetch_data():
            return 1
        api.print_data()

        # Check if over ratio/cap
        cap_warn = api.check_cap()
        ratio_warn = api.check_warn()

        if cap_warn or ratio_warn:
            return 1  # "You've had to much to download!"
    else:
        print("No API type selection", file=sys.stderr)
        return 1

    return 0
