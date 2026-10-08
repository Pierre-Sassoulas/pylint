def test_unneeded_not():
    first_string = '123'
    second_string = '456'
    assert not first_string == second_string
    assert not hash(first_string) == hash(second_string)
    assert not int(first_string) == int(second_string)
