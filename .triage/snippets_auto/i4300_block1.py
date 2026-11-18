"""
dynamic.py
"""

def __getattr__(name):
    if name.startswith('x'):
        raise AttributeError
    return 42
