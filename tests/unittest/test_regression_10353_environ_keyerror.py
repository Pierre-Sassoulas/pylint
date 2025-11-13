"""Unit test for issue #10353 - Pylint crashes with AstroidError when analyzing code
that imports a module that accesses an environment variable that doesn't exist.
"""
import os
import pytest
from pylint.testutils.unittest_linter import UnittestLinter
from pylint.lint.pylinter import PyLinter


def test_environ_keyerror_no_crash(monkeypatch):
    """Test that Pylint doesn't crash when analyzing code that imports a module
    that accesses an environment variable that doesn't exist.
    """
    # Ensure ENVIRONMENT variable is not set
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    
    # Create a linter instance
    linter = UnittestLinter()
    
    # The file to lint
    file_path = "tests/functional/r/regression/regression_10353_environ_keyerror_import.py"
    
    # This should not crash with an AstroidError
    try:
        linter.check([file_path])
        # If we get here, the test passes - no crash occurred
        assert True
    except Exception as e:
        # If we get here, Pylint crashed - test fails
        pytest.fail(f"Pylint crashed with: {e}")


def test_environ_keyerror_with_env_set(monkeypatch):
    """Test that Pylint works correctly when the environment variable is set."""
    # Set the ENVIRONMENT variable
    monkeypatch.setenv("ENVIRONMENT", "DEV")
    
    # Create a linter instance
    linter = UnittestLinter()
    
    # The file to lint
    file_path = "tests/functional/r/regression/regression_10353_environ_keyerror_import.py"
    
    # This should not crash
    linter.check([file_path])
    
    # If we get here, the test passes - no crash occurred
    assert True
