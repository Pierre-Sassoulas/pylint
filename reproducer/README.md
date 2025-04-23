# Reproducer for Pylint Issue #7585

This is a reproducer for [Pylint issue #7585](https://github.com/pylint-dev/pylint/issues/7585), which describes an infinite loop when the `c-extension-no-member` checker is activated.

## Steps to Reproduce

1. Install the required dependencies:
   ```
   pip install numpy pylint==3.0.0-a5 astroid==2.11.7
   ```

2. Run the reproducer script:
   ```
   ./run_pylint.sh
   ```

## Expected Behavior

Pylint should complete the linting process and exit normally.

## Actual Behavior

Pylint enters an infinite loop and does not complete.

## Environment

- pylint 3.0.0-a5
- astroid 2.11.7
- Python 3.10.7

## Explanation

The issue occurs when:
1. A C extension module (like numpy) is used
2. The `c-extension-no-member` checker is enabled
3. The `--jobs 0` option is used (which enables parallel processing)

The combination of these factors causes Pylint to enter an infinite loop during the linting process.
