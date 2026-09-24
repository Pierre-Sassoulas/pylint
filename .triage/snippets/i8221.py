gens = []
loop_vars = [1, 2]
for loop_var in loop_vars:
    g = (value for value in [1, 2] if value == loop_var)
    gens.append(g)

for gen in gens:
    print(list(gen))
