#!/usr/bin/env python3
"""False negative no-member"""
import datetime

SOME_BOOL = False
if SOME_BOOL:
    print(bar)
    print(datetime.does_not_exist)
