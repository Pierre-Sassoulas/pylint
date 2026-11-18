class Rectangle3:

    def __init__(self, width, length):
        self.width = width
        self.length = length

    def __bool__(self):
        if self.width == 1:
            return 'Hello'
        if self.width == 2:
            return 3
        if self.width == 3:
            return 4.0
        if self.width == 4:
            return b'World'
        if self.width == 5:
            return None
        if self.width == 6:
            return True
        if self.width == 7:
            return object()
        if self.width == 8:
            return object
