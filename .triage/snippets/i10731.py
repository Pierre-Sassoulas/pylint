class Bird:
    def flap(self, wing):
        return wing


seagull = Bird()
print(seagull.flap())


class BirdTester:
    def __init__(self, bird: Bird):
        self.bird = bird

    def bar1(self):
        bird: Bird = self.bird
        bird.flap()

    def bar2(self):
        self.bird.flap()

    def bar3(self, bird: Bird):
        bird.flap()
