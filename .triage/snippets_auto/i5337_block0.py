# pylint: disable=missing-docstring

import contextlib

async def bug() -> None:
    async with contextlib.AsyncExitStack() as stack:
        stack.enter_context(open("/tmp/x", "wb"))
