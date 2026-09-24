async def f() -> bytes:
    return b""


g = f()
g.send(None)
