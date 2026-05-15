def outer():
    def inner():
        print(i)

    inner()
    for i in range(5):
        inner()


outer()
