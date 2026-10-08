class Horse:
    def talk(self):
        print("Hihaaa!")


class Farm:
    def __init__(self, animal):
        self.animal = animal

    def animaltalk(self):
        self.animal.sing()


def main():
    horse = Horse()
    farm = Farm(horse)
    farm.animaltalk()


main()

