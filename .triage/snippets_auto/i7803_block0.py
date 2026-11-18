try:
    from cStringIO import StringIO  # pylint: python <= 2.7
except ImportError:
    from io import StringIO
