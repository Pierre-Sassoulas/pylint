key = "something"
counts = {"int64": 1, "object": 1}
counts[key] = 3 + counts.get(key, 0)
print(counts)
