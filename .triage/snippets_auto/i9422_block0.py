import csv
result = {}

def f():
    with open("/tmp/file1", 'r') as route:
        for row in csv.reader(route, delimiter="\t"):
            counter = counter + 1
            result[row[0]] = row[1]
        ...
    return counter

f()
