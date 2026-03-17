# OOP - Day 2: Classes & Inheritance
# What I learned: A class is a blueprint. __init__ runs on object creation.

class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def __str__(self):
        return f"{self.name} says {self.sound}"

    def speak(self):
        print(self.__str__())


class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "Woof")  # super() calls parent __init__

    def fetch(self):
        print(f"{self.name} fetches the ball!")


dog = Dog("Bruno")
dog.speak()     # Bruno says Woof
dog.fetch()     # Bruno fetches the ball!

ani = Animal("Tomy", "Whhhooo")

print(ani)
