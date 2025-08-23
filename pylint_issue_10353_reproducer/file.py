"""
This is the main file that will be linted by Pylint.
It imports the helper module, which imports vars.py.
"""
from pylint_issue_10353_reproducer.module.submodule.helper import get_api_url, get_environment

def main():
    """Main function."""
    print(f"Current environment: {get_environment()}")
    print(f"API URL: {get_api_url()}")

if __name__ == "__main__":
    main()
