#!/bin/bash

# This script demonstrates the issue and the workaround

# Make sure the ENVIRONMENT variable is not set
unset ENVIRONMENT

echo "=== Testing the issue ==="
echo "Running: pylint pylint_issue_10353_reproducer/file.py"
echo "Expected: Pylint crashes with an AstroidError"
pylint pylint_issue_10353_reproducer/file.py || echo "Pylint crashed as expected"

echo ""
echo "=== Testing the workaround ==="
echo "Running: pylint pylint_issue_10353_reproducer/file_fixed.py"
echo "Expected: Pylint runs successfully"
pylint pylint_issue_10353_reproducer/file_fixed.py && echo "Pylint ran successfully with the workaround"

echo ""
echo "=== Testing with ENVIRONMENT variable set ==="
echo "Setting ENVIRONMENT=DEV"
export ENVIRONMENT=DEV
echo "Running: pylint pylint_issue_10353_reproducer/file.py"
echo "Expected: Pylint runs successfully"
pylint pylint_issue_10353_reproducer/file.py && echo "Pylint ran successfully with ENVIRONMENT set"
