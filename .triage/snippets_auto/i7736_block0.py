def my_func(cls, my_list):
    if len(my_list) == 0:
        my_list.append(1)

class MyClass:
    def __init__(self):
        pass

MyClass.my_class_method = my_func.__get__(MyClass)

a_list = []
MyClass.my_class_method(a_list)
print(a_list)
