def foo():
    yield


async def agen():
    yield


def should_not_give_E1142():
    assert (await x for x in foo())


def should_give_E1142():
    assert [x async for x in agen()]


def correctly_gives_E1142():
    assert (x for x in await foo())


def correctly_does_not_give_E1142():
    assert (x async for x in agen())
