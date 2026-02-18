class Father:
    def gardening(self):
        print("Gardening")

class Mother:
    def cooking(self):
        print("Cooking")

class Child(Father, Mother):
    def sports(self):
        print("Playing football")

c = Child()

c.gardening()
c.cooking()
c.sports()
