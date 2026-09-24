class PossibleNoMember:
    def __init__(self):
        self.member: bool

    def set_member(self, member):
        self.member = member

    def depend_on_member(self):
        print(self.member)
