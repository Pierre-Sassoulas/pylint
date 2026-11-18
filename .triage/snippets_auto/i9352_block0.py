
def mutate_signature_deco(func):  # pylint: signature-mutator
    """ Add times parameter to functions to repeat that number of times """

    def replacement(times: int, *args, **kwargs):
        for _ in range(times):
            func(*args, **kwargs)

    return replacement


@mutate_signature_deco
def say_hi(name):
    """ Say hi to {name} """
    print(f"Hello, {name}!")


if __name__ == "__main__":
    say_hi(5, name="Bob")

