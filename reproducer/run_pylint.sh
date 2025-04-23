#!/bin/bash

# Run pylint with --jobs 0 to reproduce the infinite loop
cd "$(dirname "$0")"
pylint --jobs 0 test_c_extension.py
