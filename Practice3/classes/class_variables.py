class Student:
    school_name = "KBTU"

    def __init__(self, name):
        self.name = name

s1 = Student("Ali")
s2 = Student("Aruzhan")

print(s1.school_name)
print(s2.school_name)
