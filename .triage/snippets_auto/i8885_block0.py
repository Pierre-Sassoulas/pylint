#pylint: disable=protected-access, missing-module-docstring, missing-function-docstring
#pylint: disable=missing-class-docstring, too-few-public-methods
import mod.server

class TestServer():

    def test_server(self):
        # pylint: disable=invalid-name
        server = mod.server.Server()
        server._Server__dlt_socket = 1 # pylint: disable=invalid-name

