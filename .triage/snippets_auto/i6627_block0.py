class Rectangle1:

    def __init__(self, width, length):
        self.width = width
        self.length = length

    def __bool__(self):
        return 'WrongValue`  # [invalid-bool-returned]
