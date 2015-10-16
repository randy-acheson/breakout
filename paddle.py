from constants import *

class Paddle():

    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        self.rect = image.get_rect().move(
            screen_rect.centerx, screen_rect.height - PADDLE_HEIGHT)

    def move(self, direction, background):
        if self.rect.left < screen_rect.left:
            self.rect.left = screen_rect.left
        elif self.rect.right > screen_rect.right:
            self.rect.right = screen_rect.right
        else:
            screen.blit(background, self.rect, self.rect)
            self.rect = self.rect.move(direction*self.speed, 0)
            screen.blit(self.image, self.rect)
            pygame.display.update()