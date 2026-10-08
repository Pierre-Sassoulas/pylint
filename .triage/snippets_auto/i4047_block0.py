"""False-positive no-member."""
import temppathlib


def _func(params=(True,)):
    new_params = temppathlib.gettempdir().glob("*")

    # this changes the type of the elements of params:
    if True and True:
        params = new_params
    else:
        params = new_params

    # with this equivalent code, linting gives no error, as expected:
    # params = new_params if params else new_params

    for parm in params:
        print(parm.name)


_func()
