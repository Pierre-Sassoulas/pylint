"""This shows missing W4701"""
import glob

files = glob.glob("$VALID_PATH_GLOB")  # this explicitly types return to list
for _f in files:
    # infinite loop not triggering W4701
    files.append("whatever")

random_list = [1, 2, 3, 4, 5]
for _i in random_list:
    # infinite loop triggering W4701
    random_list.append(6)
