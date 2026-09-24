class ClientResponseError(Exception):
    status: int


def f(exc):
    if not isinstance(exc, ClientResponseError) or exc.status != 404:
        print("x")
    else:
        print("y")
