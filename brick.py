from constants import *

class Brick:
    def __init__(self, image, position):
        self.image = image
        self.color = random.randint(0, 16777215)
        self.rect = image.get_rect().move(position[0], position[1])
