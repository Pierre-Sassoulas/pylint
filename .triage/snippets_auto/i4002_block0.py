    def function_returning_generator(r):
        for i in [r, 1, 2, 3]:
            yield i

    def function_returning_comprehension(r):
        return [x+1 for x in [r, 1, 2, 3]]

    def function_returning_function(r):
        return function_returning_generator(r)
      

    assert len(function_returning_generator(z))   # [len-as-condition]
    assert len(function_returning_comprehension(z))   # [len-as-condition]
    assert len(function_returning_function(z))   # [len-as-condition]
