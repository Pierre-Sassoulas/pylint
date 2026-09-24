test = (lambda: print(i) for i in range(10))
for call in test:
    call()
