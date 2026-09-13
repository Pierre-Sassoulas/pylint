class Basket:
    def __init__(self):
        self.show()  # [access-member-before-initialization]
        self.apples = 3

    def show(self):
        print("The basket holds", self.apples, "apples")
