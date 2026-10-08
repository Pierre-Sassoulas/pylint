#!/usr/bin/python

""" The program's entry point """

import sys
import i2c


if __name__ == '__main__':
    if "-f" in sys.argv:
        pic = i2c.PicComms(i2c.HardCoded())
    else:
        pic = i2c.PicComms()
