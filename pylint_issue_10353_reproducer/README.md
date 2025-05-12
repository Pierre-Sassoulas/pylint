# Pylint Issue #10353 Reproducer

This repository contains a minimal reproducer for [Pylint issue #10353](https://github.com/pylint-dev/pylint/issues/10353).

## Issue Description

Pylint crashes with an `AstroidError` when analyzing code that imports a module that accesses an environment variable that doesn't exist.

The issue occurs because Pylint's AST builder (Astroid) doesn't properly handle KeyErrors that occur during module imports. When `vars.py` tries to access `environ["ENVIRONMENT"]` and the variable doesn't exist, the KeyError bubbles up and causes Pylint to crash with an AstroidError instead of handling it gracefully.

## How to Reproduce

1. Make sure the `ENVIRONMENT` environment variable is not set:
   ```bash
   unset ENVIRONMENT
   ```

2. Run Pylint on the `file.py` file:
   ```bash
   pylint pylint_issue_10353_reproducer/file.py
   ```

3. Pylint will crash with an `AstroidError`.

## Workaround

The workaround is to use `environ.get()` with a default value instead of `environ[]`:

```python
# Instead of:
ENVIRONMENT = environ["ENVIRONMENT"]

# Use:
ENVIRONMENT = environ.get("ENVIRONMENT", "DEV")
```

This is demonstrated in `vars_fixed.py`.

## Files in this Repository

- `file.py` - The main file to be linted by Pylint
- `vars.py` - Contains the code that causes the KeyError (using `environ["ENVIRONMENT"]`)
- `vars_fixed.py` - Contains the workaround using `environ.get("ENVIRONMENT", "DEV")`
- `module/submodule/helper.py` - Imports the vars module
- `test_reproducer.sh` - Script to test both the issue and the workaround

## Running the Test Script

The `test_reproducer.sh` script demonstrates the issue and the workaround:

```bash
./test_reproducer.sh
```

It will:
1. Run Pylint on `file.py` with `ENVIRONMENT` not set (should crash)
2. Run Pylint on `file_fixed.py` with `ENVIRONMENT` not set (should succeed)
3. Run Pylint on `file.py` with `ENVIRONMENT` set (should succeed)
