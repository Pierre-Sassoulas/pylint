def foo(numbers):
    for i in numbers:
        def bar():
            print(i)
        bar()
