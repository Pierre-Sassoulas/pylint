import sys

import pyroute2

with pyroute2.IPRoute() as ipr:
    idx = ipr.link_lookup(ifname=sys.argv[1])[0]
    link = ipr.get_links(idx)[0]
    print(link)
