class Rectangle2:

    def __init__(self, width, length):
        self.width = width
        self.length = length

    def __bool__(self):
        return True if self.width == 0 and self.length == 0 else False
