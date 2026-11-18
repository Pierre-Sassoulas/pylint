def outer_definition():
    i = 0
    all_possible_cases = [1, 2, 3, "4"]
    for case in all_possible_cases:  # [consider-using-enumerate]
        i += 1
        print(i, case)
