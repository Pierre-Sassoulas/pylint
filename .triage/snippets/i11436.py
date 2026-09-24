# Reporter used polars.read_excel; one of its @overload variants returns NoReturn.
# The overloads must live in another module: defined in this file, 4.0.x is clean too.
import i11436_fruitlib

i11436_fruitlib.pick("apple")
print("still here")  # 4.0.x: unreachable (W0101); main: clean
