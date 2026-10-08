Pylint issues the error logging-too-many-args for the following file (named logerr.py:

#! /usr/bin/env python3
"""
Demonstrate wrong message from pylint
"""
import logging
logging.warning( "The frequency is: %f MHz", 2.3 )
