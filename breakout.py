import pygame
from pygame.locals import *
import random
import os

my_dir = os.path.dirname(__file__)

PADDLE_HEIGHT = 16
BRICK_WIDTH = 64
BRICK_HEIGHT = 16

BrickDict = {}
def createBrick(row, width, i):
    if row < 5*BRICK_HEIGHT:
        BrickDict["Brick" + str(i)] = Brick(brick_img, (width*BRICK_WIDTH, row))
        i += 1
        if width*BRICK_WIDTH+(2*BRICK_WIDTH) > screen_rect.width:
            row += BRICK_HEIGHT
            width = -1
        createBrick(row, width + 1, i)


class Paddle():

    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        self.rect = image.get_rect().move(
            screen_rect.centerx, screen_rect.height - PADDLE_HEIGHT)

    def move(self, direction):
        if self.rect.left < screen_rect.left:
            self.rect.left = screen_rect.left
        elif self.rect.right > screen_rect.right:
            self.rect.right = screen_rect.right
        else:
            screen.blit(background, self.rect, self.rect)
            self.rect = self.rect.move(direction*self.speed, 0)
            screen.blit(self.image, self.rect)
            pygame.display.update()

class Ball():

    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        self.x_dir = 1
        self.y_dir = 1
        self.rect = image.get_rect().move(0, screen_rect.height)
        self.fastspeed = False

    def move(self):
        # if hit paddle, change direction based on where on paddle hit
        if self.rect.colliderect(paddle.rect):
            if self.rect.centerx < paddle.rect.left:
                self.rect.right = paddle.rect.left
                self.x_dir *= -1
            if self.rect.centerx > paddle.rect.right:
                self.rect.left = paddle.rect.right
                self.x_dir *= -1
            else:
                self.y_dir *= -1
                ball_x = self.rect.centerx
                paddle_x = paddle.rect.centerx
                self.x_dir = (ball_x - paddle_x) / (paddle.rect.width / 2.0)
                if self.x_dir > 1.0: self.x_dir = 1.0
                if self.x_dir < -1.0: self.x_dir = -1.0
            print self.x_dir


        # if hit sides of screen, change x direction
        if self.rect.left < screen_rect.left:
            self.x_dir *= -1
            self.rect.left = screen_rect.left
        if self.rect.right > screen_rect.right:
            self.rect.right = screen_rect.right
            self.x_dir *= -1

        # if hit top of screen, change y direction and increase speed
        if self.rect.top < screen_rect.top:
            self.rect.top = screen_rect.top
            self.y_dir *= -1
            if not self.fastspeed:
                self.speed *= 1.4
                self.fastspeed = True

        ###
        ### CHANGE
        ###
                
        # if hit bottom, reset ball and decrement life counter
        if self.rect.bottom > screen_rect.bottom:
            self.rect.bottom = screen_rect.bottom
            self.y_dir *= -1
            
        # if hit brick, remove brick and reverse x direction
        brick = False
        for i in BrickDict.keys():
            if self.rect.colliderect(BrickDict[i].rect):
                brick = BrickDict[i]
                bricknum = i
                
        # move and blit ball
        screen.blit(background, self.rect, self.rect)

        self.move_one_axis(0, self.y_dir*self.speed, brick)
        self.move_one_axis(self.x_dir*self.speed, 0, brick)
        
        # if brick collision, remove brick from dictionary
        if brick:
            screen.blit(background, brick.rect, brick.rect)
            BrickDict.pop(bricknum)
        
        screen.blit(self.image, self.rect)
        pygame.display.update()

    def move_one_axis(self, dx, dy, brick):
        self.rect.x += dx
        self.rect.y += dy

        if brick:
            if self.rect.colliderect(brick.rect):
                print self.rect.x
                if dx > 0:
                    self.rect.right = brick.rect.left
                    self.x_dir *= -1
                if dx < 0:
                    self.rect.left = brick.rect.right
                    self.x_dir *= -1
                if dy > 0:
                    self.rect.bottom = brick.rect.top
                    self.y_dir *= -1
                if dy < 0:
                    self.rect.top = brick.rect.bottom
                    self.y_dir *= -1
                
class Brick:
    def __init__(self, image, position):
        self.image = image
        self.color = random.randint(0, 16777215)
        self.rect = image.get_rect().move(position[0], position[1])

    

### initialize game
pygame.init()
pygame.display.set_caption('Breakout!')
clock = pygame.time.Clock()
running = True

# initialize screen
screen = pygame.display.set_mode((640, 480))
screen_rect = screen.get_rect()

# initialize background
background_size = screen.get_size()
background = pygame.Surface(background_size)
background = background.convert()
background.fill((250, 250, 250))

# import images
paddle_img = pygame.image.load("paddle.png").convert()
ball_img = pygame.image.load("ball.png").convert()
ball_img.set_colorkey((255, 0, 0))
brick_img = pygame.image.load("brick.png").convert()

# create objects
paddle = Paddle(paddle_img, 8)
ball = Ball(ball_img, 8)
createBrick(BRICK_HEIGHT, 0, 0)

# play music
music = os.path.join(my_dir, "music/breakout_full_long.ogg")
pygame.mixer.init()
pygame.mixer.music.load(music)
pygame.mixer.music.play()


# blit sprites
screen.blit(background, (0, 0))
screen.blit(paddle_img, paddle.rect)
screen.blit(ball_img, ball.rect)
for i in range(len(BrickDict)):
    pygame.draw.rect(screen, BrickDict["Brick" + str(i)].color, BrickDict["Brick" + str(i)].rect)

pygame.display.update()


### main game loop
while running:


    # interrupt if 'enter' pressed -- ends game
    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_RETURN) or event.type == QUIT:
            running = False


    ball.move()

    # poll for player input
    keystate = pygame.key.get_pressed()
    paddle_direction = keystate[K_RIGHT] - keystate[K_LEFT]

    paddle.move(paddle_direction)


    # limit to 40 FPS
    clock.tick(40)

pygame.quit()
