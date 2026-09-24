values = {}
accumulated_values = {}
id_ = 0
for r in [1, 2, 3, 4, 5]:
    id_ += 1
    if id_ == 1:
        key = str(1)
        values[key] = r
        accumulated_values[key] = r
    else:
        if key == "1":
            accumulated_values[key] = values[key]
        else:
            previous = str(int(key) - 1)
            accumulated_values[key] = accumulated_values[previous] + values[key]

        key = str(1 + int(key))
        values[key] = r
        previous = str(int(key) - 1)
        accumulated_values[key] = accumulated_values[previous] + values[key]
print(values)
print(accumulated_values)
