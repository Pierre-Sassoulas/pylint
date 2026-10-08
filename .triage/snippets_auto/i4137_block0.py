"Something"
from kazoo.client import KazooClient

KAZOO_CLIENT = None

def init_kazoo_client() -> KazooClient:
    "initialize"
    global KAZOO_CLIENT  # pylint: disable=global-statement
    KAZOO_CLIENT = KazooClient()
    KAZOO_CLIENT.start()
    return KAZOO_CLIENT

def get_kazoo_client() -> KazooClient:
    "get client"
    global KAZOO_CLIENT  # pylint: disable=global-statement
    assert KAZOO_CLIENT is not None, "Uh oh"
    return KAZOO_CLIENT
