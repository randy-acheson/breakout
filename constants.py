import pygame
from pygame.locals import *
import random
import os

PADDLE_HEIGHT = 16
BRICK_WIDTH = 64
BRICK_HEIGHT = 16

screen = pygame.display.set_mode((640, 480))
screen_rect = screen.get_rect()

pygame.init()
pygame.display.set_caption('Breakout!')
if not pygame.font: print ('Font module cannot load')
font1 = pygame.font.Font(None, 12)
