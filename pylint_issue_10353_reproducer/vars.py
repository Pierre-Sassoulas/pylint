"""
This file demonstrates the issue where Pylint crashes when analyzing code
that imports a module that accesses an environment variable that doesn't exist.
"""
from os import environ
from typing import Literal

# This line will cause a KeyError when the ENVIRONMENT variable is not set
# This is what causes Pylint to crash with an AstroidError
ENVIRONMENT: Literal["DEV", "PROD", "TEST"] = environ["ENVIRONMENT"]  # type: ignore - narrowing

# Other constants that depend on ENVIRONMENT
if ENVIRONMENT == "DEV":
    API_URL = "https://dev-api.example.com"
elif ENVIRONMENT == "PROD":
    API_URL = "https://api.example.com"
else:  # TEST
    API_URL = "https://test-api.example.com"
