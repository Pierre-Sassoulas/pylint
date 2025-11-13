"""
This file imports vars.py, which will cause Pylint to crash when analyzing this file
if the ENVIRONMENT variable is not set.
"""
from pylint_issue_10353_reproducer.vars import ENVIRONMENT, API_URL

def get_api_url():
    """Return the API URL based on the current environment."""
    return API_URL

def get_environment():
    """Return the current environment."""
    return ENVIRONMENT
