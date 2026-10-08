def halfway_safe():
    """Name used safely inside the loop, unsafely outside it."""
    for _temp in range(0, 1):
        try:
            pass
        except ValueError:
            error = True
        else:
            continue

        print(error)
    print(error)  # Should raise used-before-assignment
