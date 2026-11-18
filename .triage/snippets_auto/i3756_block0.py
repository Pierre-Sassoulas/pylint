for i in range(5):
    i # /!\ This is important
    a = lambda p: p * \
        i # pylint: disable=cell-var-from-loop
