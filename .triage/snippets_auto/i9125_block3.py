_____________ test_use_a_generator _____________ 
    def test_use_a_generator():
>       assert all(int(i) == i for i in [1, 2, 3, "4"])
E       assert False
E        +  where False = all(<generator object test_use_a_generator.<locals>.<genexpr> at 0x7fd1b67eaf80>)
