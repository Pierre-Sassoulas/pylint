class C:
    def __init__(self):
        self.data = {}

    def add(self, name, value):
        self.data[name] = value

    def dump(self):
        if len(self.data) == 1:
            ((name, value),) = self.data.items()
            print(f"just one: {name} -> {value}")
        else:
            print("empty or multiple items")
