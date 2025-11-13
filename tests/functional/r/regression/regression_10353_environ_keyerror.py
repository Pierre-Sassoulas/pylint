"""Regression test for https://github.com/pylint-dev/pylint/issues/10353.

This test verifies that Pylint doesn't crash with an AstroidError when analyzing code
that imports a module that accesses an environment variable that doesn't exist.
"""
# pylint: disable=missing-docstring,unused-import

import os
from os import environ

# This variable will be accessed in the test
ENVIRONMENT = environ.get("ENVIRONMENT", "DEV")

# Define a function that uses the environment variable
def get_api_url():
    if ENVIRONMENT == "DEV":
        return "https://dev-api.example.com"
    elif ENVIRONMENT == "PROD":
        return "https://api.example.com"
    else:  # TEST
        return "https://test-api.example.com"
