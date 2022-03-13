from random import seed
from random import randint

class Randomizer:



    @staticmethod
    def generateRandomPoint(maxWidth, maxHeight):
        seed(1)

        x = randint(0, maxWidth)
        y = randint(0, maxHeight)

        return (x, y)