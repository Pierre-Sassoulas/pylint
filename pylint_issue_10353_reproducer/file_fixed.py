"""
This is the main file that will be linted by Pylint.
It imports a module that uses the fixed version of vars.py.
"""
# This version imports from vars_fixed.py instead of vars.py
# pylint: disable=unused-import
from pylint_issue_10353_reproducer.vars_fixed import ENVIRONMENT, API_URL

def main():
    """Main function."""
    print(f"Current environment: {ENVIRONMENT}")
    print(f"API URL: {API_URL}")

if __name__ == "__main__":
    main()
