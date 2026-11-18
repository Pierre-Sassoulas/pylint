import os

def get_config(value=os.getenv('CONFIG')):
    return value

# If the environment variable 'CONFIG' changes after the function is defined,
# the function will still return the old value as the default.

