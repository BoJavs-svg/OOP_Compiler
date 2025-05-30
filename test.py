class Pet:
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species

    def speak(self):
        return f"{self.name} makes a noise."

    def info(self):
        return f"{self.name} is a {self.species}."


class Dog(Pet):
    def __init__(self, name: str, breed: str):
        super().__init__(name, species="Dog")
        self.breed = breed

    def speak(self):
        return f"{self.name} says Woof!"

    def info(self):
        return f"{self.name} is a {self.breed} dog."


class Cat(Pet):
    def __init__(self, name: str, color: str):
        super().__init__(name, species="Cat")
        self.color = color

    def speak(self):
        return f"{self.name} says Meow!"

    def info(self):
        return f"{self.name} is a {self.color} cat."


def main():
    pets = [
        Dog("Rex", "Golden Retriever"),
        Cat("Whiskers", "white"),
        Pet("Milo", "parrot")
    ]

    for pet in pets:
        print(pet.info())
        print(pet.speak())
        print("-" * 30)

if __name__ == "__main__":
    main()
