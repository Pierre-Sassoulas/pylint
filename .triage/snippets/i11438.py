"""Doc."""
from http.server import BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    """Doc."""

    def log_error(self, format, *args):
        """Doc."""
        print(format, args)
