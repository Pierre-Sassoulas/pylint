"""Open and print plist file."""
import sys
from plistlib import load, FMT_BINARY

with open(sys.argv[1], 'rb') as plist:
    print(load(plist, fmt=FMT_BINARY))
