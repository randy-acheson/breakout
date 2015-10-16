import pygame
from pygame.locals import *
import random
import os
import ball
import brick
import paddle
from constants import *
import pygame._view

### Main file for running the game

my_dir = os.path.dirname('__file__')

brickDict = {}

# creates the rows of bricks recursively
def createBrick(row, width, i):
    if row < 5*BRICK_HEIGHT:
        brickDict["Brick" + str(i)] = brick.Brick(brick_img,
                                                  (width*BRICK_WIDTH, row))
        i += 1
        if width*BRICK_WIDTH+(2*BRICK_WIDTH) > screen_rect.width:
            row += BRICK_HEIGHT
            width = -1
        createBrick(row, width + 1, i)

### initialize game
clock = pygame.time.Clock()
running = True

# initialize background
background_size = screen.get_size()
background = pygame.Surface(background_size)
background = background.convert()
background.fill((250, 250, 250))

# import images
paddle_img = pygame.image.load("assets/paddle.png").convert()
ball_img = pygame.image.load("assets/ball.png").convert()
ball_img.set_colorkey((255, 0, 0))
brick_img = pygame.image.load("assets/brick.png").convert()

# create objects
paddle = paddle.Paddle(paddle_img, 8)
ball = ball.Ball(ball_img, 8)
createBrick(BRICK_HEIGHT, 0, 0)

# blit sprites
screen.blit(background, (0, 0))
screen.blit(paddle_img, paddle.rect)
screen.blit(ball_img, ball.rect)
for i in range(len(brickDict)):
    pygame.draw.rect(screen, brickDict["Brick" + str(i)].color,
                     brickDict["Brick" + str(i)].rect)

pygame.display.update()


### main game loop
while running:


    # interrupt if 'enter' pressed -- ends game
    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_RETURN) or event.type == QUIT:
            running = False

    ball.move(paddle, brickDict, background)

    # poll for player input
    keystate = pygame.key.get_pressed()
    paddle_direction = keystate[K_RIGHT] - keystate[K_LEFT]

    paddle.move(paddle_direction, background)


    # limit to 40 FPS
    clock.tick(40)

pygame.quit()
