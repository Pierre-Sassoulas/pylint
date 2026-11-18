def test_use_a_generator():
    assert all(int(i) == i for i in [1, 2, 3, "4"])
