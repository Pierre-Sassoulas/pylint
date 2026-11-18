import os

def connect_to_service(api_key=os.environ['API_KEY']):
    # Connect using the API key
    pass

# If the 'API_KEY' environment variable is updated after the function definition,
# the function will not use the updated key unless explicitly passed.
