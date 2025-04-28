"""File that imports the module that will cause an error."""
# pylint: disable=missing-docstring,unused-import

# This import will cause Pylint to crash with an AstroidError
# if the ENVIRONMENT variable is not set
from tests.functional.r.regression.regression_10353_environ_keyerror_bad import ENVIRONMENT, API_URL

def main():
    """Main function."""
    print(f"Current environment: {ENVIRONMENT}")
    print(f"API URL: {API_URL}")

if __name__ == "__main__":
    main()
