from typing import Protocol


class Handler(Protocol):
    def __call__(self, value: int, name: str) -> int:
        pass


def invalid_func_arg_type_mismatch(value: str, name: str) -> int:
    return value * 2


def invalid_func_return_type_mismatch(value: int, name: str) -> str:
    return value * 2


class AsyncHandler(Protocol):
    async def __call__(self, value: int, name: str) -> int:
        pass


async def invalid_async_func_arg_type_mismatch(value: str, name: str) -> int:
    return value * 2


async def invalid_async_func_return_type_mismatch(value: int, name: str) -> str:
    return value * 2



# None of the following lines triggers a pylint issue regarding
# mismatch of the return-type or argument-type from the defined Protocol.
# My IntelliJ IDE complains on all 4 lines, because either an argument-type
# or the return-type of the function will not match the `Protocol` I try to assign
# to.

# Expected type 'Handler', got '(value: str, name: str) -> int' instead
my_handler_a: Handler = invalid_func_arg_type_mismatch

# Expected type 'Handler', got '(value: int, name: str) -> str' instead
my_handler_b: Handler = invalid_func_return_type_mismatch

# Expected type 'AsyncHandler', got '(value: str, name: str) -> Coroutine[Any, Any, int]' instead
my_handler_c: AsyncHandler = invalid_async_func_arg_type_mismatch

# Expected type 'AsyncHandler', got '(value: int, name: str) -> Coroutine[Any, Any, str]' instead 
my_handler_d: AsyncHandler = invalid_async_func_return_type_mismatch
