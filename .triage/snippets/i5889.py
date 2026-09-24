class MyException(ArithmeticError, ValueError):
    pass


try:
    raise MyException
except ArithmeticError:
    raise
except ValueError:
    pass
