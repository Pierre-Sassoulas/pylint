import functools
from collections.abc import Callable
from typing import NamedTuple


class Module(NamedTuple):
    init: Callable
    apply: Callable


def module(module_maker):
    @functools.wraps(module_maker)
    def fabricate_module(*args, **kwargs):
        init, apply = module_maker(*args, **kwargs)
        return Module(init, apply)

    return fabricate_module


@module
def my_module():
    def my_module_init(x_in):
        return x_in

    def my_module_apply(x_in):
        return x_in

    return my_module_init, my_module_apply


mod = my_module()
mod.init(0.0)
mod.apply(0.0)
