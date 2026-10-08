if sys.version_info >= (3, 12):
    from importlib.resources.abc import TraversableResources
else:
    from importlib.abc import TraversableResources # [deprecated-class]
