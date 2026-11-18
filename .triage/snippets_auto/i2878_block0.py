class Hello:
    def __init__(self):
        # self.x = 1
        # self.y = 2
        # Set two above attributes dynamically
        d = {'x': 1, 'y': 2}
        for k, v in d.items():
            setattr(self, k, v)
