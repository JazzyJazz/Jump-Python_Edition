import pygame as pg
from pygame.sprite import Sprite
from settings import *
vec = pg.Vector2
from random import randint
from screenSize import *

class Cloud(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "attributes", "cloud.png")
        self.changeSize = randint(10, 40)
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120 + self.changeSize,90 + self.changeSize))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = randint(100, 200)
        self.vel = vec(cloudVelocity,0)
        

    def update(self, vel):
        self.vel.x = cloudVelocity + vel
        self.rect.x += self.vel.x

class Deco_platform(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((3,3))
        self.image.fill((37, 171, 252))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT -50 + randint(2, 10)
        self.vel = vec(0,0)

    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Moon(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "attributes", "moon.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (100, 100))
        self.vel = vec(0,0)
        self.rect = self.image.get_rect()
        self.rect.y = randint(100, 200)
        self.init_width()
    
    def init_width(self):
        if WIDTH < 1000:
            self.rect.x = WIDTH + int((1000-WIDTH)/2)
            self.vel.x = -1
        elif WIDTH < 2000:  
            self.rect.x = WIDTH + int((2000-WIDTH)/ 2)
            self.vel.x = -2
        elif WIDTH < 3000:  
            self.rect.x = WIDTH + int((3000-WIDTH)/2)
            self.vel.x = -3
        else: 
            self.rect.x = WIDTH + int((4000-WIDTH)/2)
            self.vel.x = -4

    def update(self, turn):
        if turn%1000 == 1:
            self.init_width()
        self.rect.x += self.vel.x

class ExtraLife(pg.sprite.Sprite):
    def __init__(self, rectX, rectY):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "attributes", "heart.png")
        self.changeSize = randint(10, 40)
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, ((100,100)))
        self.rect = self.image.get_rect()
        self.rect.x = rectX
        self.rect.y = rectY
        self.vel = vec(0, -0.2)
        self.col = (255, 0, 0)
        

    def update(self, col):
        self.rect.y += self.vel.y
        if self.col[0] > col[0]: self.addR = -2
        else: self.addR = 2
        if self.col[1] > col[1]: self.addG = -2
        else: self.addG = 2
        if self.col[2] > col[2]: self.addB = -2
        else: self.addB = 2
        self.image = self.image.copy()
        self.newCol = (self.col[0] + self.addR, self.col[1] + self.addG, self.col[2] + self.addB)
        self.image.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
        self.image.fill(self.newCol[0:3] + (0,), None, pg.BLEND_RGBA_ADD)
        self.col = self.newCol

class MinusLife(pg.sprite.Sprite):
    def __init__(self, rectX, rectY, nb):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "attributes", f"demi_heart{nb}.png")
        self.changeSize = randint(10, 40)
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, ((50,100)))
        self.rect = self.image.get_rect()
        self.rect.x = rectX + (nb-1)*50
        self.rect.y = rectY - 30
        self.vel = vec(0.2, -0.2)
        self.col = (255, 0, 0)
        if nb == 1: self.direction = "l"
        if nb == 2:   self.direction = "r"
        

    def update(self, col):
        if self.direction == "l":
            self.rect.x -= self.vel.x
            self.rect.y += self.vel.y
        elif self.direction == "r":
            self.rect.x += self.vel.x
            self.rect.y += self.vel.y

        if self.col[0] > col[0]: self.addR = -2
        else: self.addR = 2
        if self.col[1] > col[1]: self.addG = -2
        else: self.addG = 2
        if self.col[2] > col[2]: self.addB = -2
        else: self.addB = 2
        self.image = self.image.copy()
        self.newCol = (self.col[0] + self.addR, self.col[1] + self.addG, self.col[2] + self.addB)
        self.image.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
        self.image.fill(self.newCol[0:3] + (0,), None, pg.BLEND_RGBA_ADD)
        self.col = self.newCol

class Text(pg.sprite.Sprite):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.myfont = pg.font.SysFont("Helvetica", 40)
        self.image = self.myfont.render(self.text, False, (255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = int(WIDTH/2)
        self.rect.y = int(HEIGHT/2)