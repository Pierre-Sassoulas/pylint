"""
Use `hello` module
"""
import hello


def main():
    """Runner function"""
    var = hello.Hello()
    print(var.x)
    print(var.y)

if __name__ == '__main__':
    main()
