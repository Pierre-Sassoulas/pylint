def connect_to_service(api_key=None):
    if api_key is None:
        api_key = os.environ['API_KEY']
    pass


def get_config(value=None):
    if value is None:
        value = os.getenv('CONFIG')
    return value
