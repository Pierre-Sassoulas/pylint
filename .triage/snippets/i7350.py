def test():
    try:
        try:
            x = None
        except:
            x = None
            raise
    finally:
        print("x", x)
