"""OKest docstring.
"""


def not_foo():
    """OKest docstring.
    """
    random_dict = not_bar()

    # invalid-sequence-index:
    print([value["a"] for key, value in random_dict.items()])

    # No error:
    print([value["a"] for value in random_dict.values()])

    for key, value in random_dict.items():
        # invalid-sequence-index:
        print(key, value["a"])

    # No error:
    for value in random_dict.values():
        print(value["a"])

    # No error:
    for key in random_dict:
        print(random_dict[key]["a"])


def not_bar():
    """OKest docstring.
    """
    return {"Oh look": "A string"}
