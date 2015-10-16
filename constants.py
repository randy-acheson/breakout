import pygame
from pygame.locals import *
import random
import os

### All constants and global variables

PADDLE_HEIGHT = 16
BRICK_WIDTH = 64
BRICK_HEIGHT = 16

screen = pygame.display.set_mode((640, 480))
screen_rect = screen.get_rect()

pygame.init()
pygame.display.set_caption('Breakout!')
