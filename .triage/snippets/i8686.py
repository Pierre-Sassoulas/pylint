def test():
    try:
        return [1 / 0]
    except ZeroDivisionError:
        try:
            results = []
        finally:
            pass
    return results
