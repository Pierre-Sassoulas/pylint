class Wat:
    asdf = None
    @staticmethod
    def get_asdf():
        Wat.asdf = [1, 2, 3]
        return Wat.asdf

    def __init__(self):
        zxcv = [x + 1 for x in Wat.get_asdf()]
        self.zxcv = zxcv

wat = Wat()
print(wat.zxcv)
