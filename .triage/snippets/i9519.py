class WinHlp:
    def print_text(self, txt):
        print(f"{__class__} {txt=}")


class Window:
    def print_text(self, txt):
        print(f"{__class__} {txt=}")


class Win(WinHlp, Window):
    def __init__(self, txt):
        super().__init__(txt)
        self.print_text(txt)


Win("hello")
