"""
This file demonstrates the workaround for the issue where Pylint crashes when analyzing code
that imports a module that accesses an environment variable that doesn't exist.
"""
from os import environ
from typing import Literal

# Using environ.get() with a default value prevents the KeyError
# This is the workaround for the issue
ENVIRONMENT: Literal["DEV", "PROD", "TEST"] = environ.get("ENVIRONMENT", "DEV")  # type: ignore - narrowing

# Other constants that depend on ENVIRONMENT
if ENVIRONMENT == "DEV":
    API_URL = "https://dev-api.example.com"
elif ENVIRONMENT == "PROD":
    API_URL = "https://api.example.com"
else:  # TEST
    API_URL = "https://test-api.example.com"
