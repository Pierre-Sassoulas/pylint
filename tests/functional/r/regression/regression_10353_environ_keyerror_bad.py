"""Module that will cause an error when imported if ENVIRONMENT is not set."""
# pylint: disable=missing-docstring

from os import environ

# This line will cause a KeyError when the ENVIRONMENT variable is not set
# This is what causes Pylint to crash with an AstroidError
ENVIRONMENT = environ["ENVIRONMENT"]  # This will raise KeyError if ENVIRONMENT is not set

# Other constants that depend on ENVIRONMENT
if ENVIRONMENT == "DEV":
    API_URL = "https://dev-api.example.com"
elif ENVIRONMENT == "PROD":
    API_URL = "https://api.example.com"
else:  # TEST
    API_URL = "https://test-api.example.com"
