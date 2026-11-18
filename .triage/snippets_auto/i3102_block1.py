def correct_func(flag, arg):
	if flag:
        arg = "overwritten"
    return arg

def incorrect_func(flag, arg):
    if flag:
        arg = "overwritten if true"
    else:
        arg = "also overwritten if false"
    return arg
