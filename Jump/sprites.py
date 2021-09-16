# classes des sprites du jeu
import pygame as pg
from pygame import sprite
from pygame.sprite import Sprite
from settings import *
vec = pg.Vector2
import random
from screenSize import *
import os


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((40, 50))
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, self.rect.height / 2)
        self.acc = vec(0,0.3)
        self.vel = vec(0, 0)
        self.pathS = os.path.join(CUR_PATH, "sound", "soundJump.wav")
        self.soundJump = pg.mixer.Sound(self.pathS)

    def update(self):
        self.acc = vec(0, 0.3)
        self.rect.midbottom = self.pos
        self.keys = pg.key.get_pressed()
        if (self.keys[pg.K_SPACE] or self.keys[pg.K_UP]) and self.pos.y >= (HEIGHT - 50):
            self.acc.y = -9
            if not muting:
                self.soundJump.play()
        self.vel.y += self.acc.y
        self.rect.y += self.vel.y
        self.pos += 0.5 * self.acc + self.vel

class Platform(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((WIDTH, 15))
        self.image.fill(jaune2)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - 50
        self.all_deco = pg.sprite.Group()
        self.image2 = pg.Surface((WIDTH, 35))
        self.image2.fill(jaune3)
        #self.deco = Deco_platform
        
    def drawUnderGround(self, screen):
        screen.blit(self.image2, (0,HEIGHT-35))
    
class Hole(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((85, 50))
        self.image.fill((37, 171, 252))
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 50
        self.vel = vec(0,0)

    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Bird(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "attributes", "bird.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (70,45))
        self.rect = self.image.get_rect()
        self.positions = random.randint(1,8)
        self.rect.x = WIDTH
        if self.positions == 1:
            self.rect.y = HEIGHT - 110
        elif self.positions == 2:
            self.rect.y = HEIGHT - 220
        elif self.positions == 3:
            self.rect.y = HEIGHT - 310
        elif self.positions == 4:
            self.rect.y = HEIGHT - 410
        else:
            self.rect.y = HEIGHT - 140
        self.vel = vec(0,0)
        
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Obstacle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((40, 40))
        self.image.fill(jaune2)
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 90
        self.vel = vec(0,0)
        
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Plane(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "attributes", "plane.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (200, 75))
        self.rect = self.image.get_rect() 
        self.positions = random.randint(1, 5)
        self.rect.x = WIDTH
        if self.positions == 1:
            self.rect.y = HEIGHT - 500
        elif self.positions == 2:
            self.rect.y = HEIGHT - 550
        elif self.positions == 3:
            self.rect.y = HEIGHT - 600
        elif self.positions == 4:
            self.rect.y = 100
        else:
            self.rect.y = 30
        self.vel = vec(0,0)

    def update(self, vel, obstacleVelocity):
        self.vel.x = 2*obstacleVelocity + vel
        self.rect.x += self.vel.x



# BOUCHEZ
class Bouchez(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Bouchez", "bouchez.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH-110
        self.rect.y = HEIGHT-210
        self.direction = "up"
        self.vel = vec(0,0)

    def update(self):
        if self.direction == "up":
            if self.rect.y == HEIGHT-250:
                self.direction = "down"
            else:
                self.rect.y -= 1
        elif self.direction == "down":
            if self.rect.y == HEIGHT - 160:
                self.direction = "up"
            else:    
                self.rect.y += 1

    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1) * obstacleVelocity - vel
        self.rect.x += self.vel.x

class Chemise(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Bouchez", "chemise.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (75, 100))
        self.rect = self.image.get_rect()
        self.positions = random.randint(1,6)
        self.rect.x = WIDTH
        if self.positions == 1:
            self.rect.y = HEIGHT - 220
        elif self.positions == 2:
            self.rect.y = HEIGHT - 200
        elif self.positions == 3:
            self.rect.y = HEIGHT - 180
        elif self.positions == 4:
            self.rect.y = HEIGHT - 160
        elif self.positions == 5:
            self.rect.y = HEIGHT - 140
        else:
            self.rect.y = HEIGHT - 120
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x
    
class Banane(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Bouchez", "banane.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 120
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x


# BESSON
class Besson(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Besson", "besson.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH-110
        self.rect.y = HEIGHT-210
        self.direction = "up"
        self.vel = vec(0,0)

    def update(self):
        if self.direction == "up":
            if self.rect.y == HEIGHT-250:
                self.direction = "down"
            else:
                self.rect.y -= 2
        elif self.direction == "down":
            if self.rect.y == HEIGHT - 150:
                self.direction = "up"
            else:    
                self.rect.y += 2
    
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1) * obstacleVelocity - vel
        self.rect.x += self.vel.x

class Missile(pg.sprite.Sprite):
    def __init__(self, bossRectY):
        super().__init__()
        self.path1 = os.path.join(CUR_PATH, "boss", "Besson", "missile.png")
        self.path2 = os.path.join(CUR_PATH, "boss", "Besson", "apple_pencil.png")
        self.imageNbr = random.randint(0, 1)
        self.imageList = [self.path1, self.path2]
        self.image = pg.image.load(self.imageList[self.imageNbr])
        if self.imageNbr == 0:
            self.image = pg.transform.scale(self.image, (70,30))
        else:
            self.image = pg.transform.scale(self.image, (70,20))
        
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 120
        self.rect.y = bossRectY + Besson().rect.height / 2
        self.vel = vec(0,0)

    def update(self, vel, obstacleVelocity):
        self.vel.x = 1.5*obstacleVelocity + vel
        self.rect.x += self.vel.x


# ROCHAT
class Rochat(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Rochat", "rochat.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT-130
        self.direction = "left"
        self.vel = vec(0,0)

    def update(self):
        self.listDirections = ["up", "down", "right", "left"]
        if self.direction == "left":
            if self.rect.x == WIDTH-300:
                self.listDirections.remove("left")
                self.direction = random.choice(self.listDirections)
            else:
                self.rect.x -= 2

        elif self.direction == "up":
            if self.rect.y == HEIGHT - 400:
                self.listDirections.remove("up")
                self.direction = random.choice(self.listDirections)
            else:    
                self.rect.y -= 2

        elif self.direction == "right":
            if self.rect.x == WIDTH - 130:
                self.listDirections.remove("right")
                self.direction = random.choice(self.listDirections)
            else:    
                self.rect.x += 2

        elif self.direction == "down":
            if self.rect.y == HEIGHT - 120:
                self.listDirections.remove("down")
                self.direction = random.choice(self.listDirections)
            else:    
                self.rect.y += 2
        
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class Kinder(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path1 = os.path.join(CUR_PATH, "boss", "Rochat", "kinder1.png")
        self.path2 = os.path.join(CUR_PATH, "boss", "Rochat", "kinder2.png")
        self.image = pg.image.load(self.path1)
        self.image = pg.transform.scale(self.image, (70, 75))
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 120
        self.vel = vec(0,0)
        self.eat = False
    
    def eaten(self):
        if not self.eat:
            self.eat = True
            self.image = pg.image.load(self.path2)
            self.image = pg.transform.scale(self.image, (70, 75))
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Coca(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Rochat", "coca.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (50, 75))
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 120
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x


# VUILLE
class Vuille(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Vuille", "vuille.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT-160
        self.vel = vec(0,0)

    def update(self):
        None
        
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class TM(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Vuille", "tm.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (55, 75))
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH - 100
        self.rect.y = HEIGHT - 300
        self.vel = vec(0,0)
        self.acc = vec(0,2)
        self.randNbr = random.randint(1, 50)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x
        if self.rect.y < HEIGHT - 120:
            self.vel.y += (1/self.randNbr)*self.acc.y
            self.rect.y += self.acc.y + self.vel.y

class Trebuchet(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path1 = os.path.join(CUR_PATH, "boss", "Vuille", "trebuchet1.png")
        self.path2 = os.path.join(CUR_PATH, "boss", "Vuille", "trebuchet2.png")
        self.image = pg.image.load(self.path1)
        self.image = pg.transform.scale(self.image, (300,300))
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH - 300
        self.rect.y = HEIGHT - 310
    
    def update(self, position):
        self.listeImg = [self.path1, self.path2]
        self.image = pg.image.load(self.listeImg[position])
        self.image = pg.transform.scale(self.image, (300,300))
        if position == 1:
            self.rect.y = HEIGHT - 324
        else:
            self.rect.y = HEIGHT - 310


# BUCHMAN
class Buchman(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Buchman", "buchman.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = HEIGHT - 140
        self.vel = vec(0,0)

    def update(self):
        None
        
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class Emerentia(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Buchman", "emerentia.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (65, 75))
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 120
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x
    
class PressText(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.nbr = random.randint(0, 25)
        self.keyToPress = listOfKeys[self.nbr]
        self.text = f"Ecrivez une dissertation de 80 lignes sur la touche {self.keyToPress}"
        self.myfont = pg.font.SysFont("Helvetica", 20)
        self.image = self.myfont.render(self.text, False, (255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = int(HEIGHT/2)
        self.counteKey = 0
        self.death = True
        

    def update(self):
        self.keys = pg.key.get_pressed()
        if self.keys[self.nbr + 97]:#pg.self.keyToPress]:
            if self.counteKey < 100:
                self.counteKey += 1
            self.text = f"""Ecrivez une dissertation de 80 lignes sur la touche {self.keyToPress} ;
            {100 - self.counteKey} lignes restantes"""
            self.image = self.myfont.render(self.text, False, (255, 0, 0))
        if self.counteKey == 99:
            self.death = False


# FAGGIONI
class Faggioni(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Faggioni", "faggioni1.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT-150
        self.vel = vec(0,0)

    def update(self, playerH):
        if self.rect.y < playerH:
            if self.rect.y < HEIGHT - 160:
                self.rect.y += 1  
        else:
            self.rect.y -= 1
        
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class NotesMus(pg.sprite.Sprite):
    def __init__(self, bossRectY):
        super().__init__()
        self.path1 = os.path.join(CUR_PATH, "boss", "Faggioni", "note_noire.png")
        self.path2 = os.path.join(CUR_PATH, "boss", "Faggioni", "note_blanche.png")
        self.path3 = os.path.join(CUR_PATH, "boss", "Faggioni", "note_croche.png")
        self.path4 = os.path.join(CUR_PATH, "boss", "Faggioni", "note_dcroche.png")
        self.imageNbr = random.randint(0, 3)
        self.imageList = [self.path1, self.path2, self.path3, self.path4]
        self.image = pg.image.load(self.imageList[self.imageNbr])
        self.image = pg.transform.scale(self.image, (30,70))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 120
        self.rect.y = bossRectY + int(Faggioni().rect.height / 2)
        self.vel = vec(0,0)

    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x    

class CleMus(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path1 = os.path.join(CUR_PATH, "boss", "Faggioni", "cle_sol.png")
        self.path2 = os.path.join(CUR_PATH, "boss", "Faggioni", "cle_fa.png")
        self.imageNbr = random.randint(0, 1)
        self.imageList = [self.path1, self.path2]
        self.image = pg.image.load(self.imageList[self.imageNbr])
        if self.imageNbr == 0:
            self.image = pg.transform.scale(self.image, (50,90))
        else:
            self.image = pg.transform.scale(self.image, (75,75))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 120
        self.rect.y = HEIGHT - 140
        self.vel = vec(0,0)

    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x


# ANDENMATTEN
class Andenmatten(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Andenmatten", "andenmatten.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = HEIGHT - 140
        self.vel = vec(0,0)

    def update(self):
        None
    
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class Chaussures(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Andenmatten", "chaussure.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (90, 75))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 120
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Vent(pg.sprite.Sprite):
    def __init__(self, timeCounte):
        super().__init__()
        self.nbr = random.randint(1, 3)
        self.path = os.path.join(CUR_PATH, "boss", "Andenmatten", "wind.png")
        self.imageW = pg.image.load(self.path)
        self.image = pg.transform.scale(self.imageW, (80, 80))
        if self.nbr == 2:
            self.image = pg.transform.rotate(self.image, 90)
        elif self.nbr == 3:
            self.image = pg.transform.rotate(self.image, -90)
        
        self.time = timeCounte
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - 120
        if self.nbr == 3:
            self.rect.x = int(WIDTH / 2) - 100
        elif self.nbr == 2:
            self.rect.x = int(WIDTH/2) + 100
        else:
            self.rect.x = int(WIDTH/2)


# REYMOND
class Reymond(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Reymond", "reymond.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = HEIGHT - 220
        self.vel = vec(0,0)
        self.direction = "down"

    def update(self):
        if self.direction == "up":
            if self.rect.y == HEIGHT-450:
                self.direction = "down"
            else:
                self.rect.y -= 1
        elif self.direction == "down":
            if self.rect.y == HEIGHT - 200:
                self.direction = "up"
            else:
                self.rect.y += 1
    
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class Chimie1(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Reymond", "chimie1.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (70, 90))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 120
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Chimie2(pg.sprite.Sprite):
    def __init__(self, bossRectY):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Reymond", "chimie2.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (70, 90))
        self.image = pg.transform.rotate(self.image, 45)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = bossRectY
        self.vel = vec(0,0)
        self.acc = vec(0,2)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x
        if self.rect.y < HEIGHT - 120:
            self.vel.y += (1/40)*self.acc.y
            self.rect.y += self.acc.y + self.vel.y

class Explosion(pg.sprite.Sprite):
    def __init__(self, contactX, contactY):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Reymond", "explosion.png")
        self.image = pg.image.load(self.path)
        self.scale = (120,120)
        self.image = pg.transform.scale(self.image, (self.scale))
        self.rect = self.image.get_rect()
        self.rect.x = contactX
        self.rect.y = contactY - 45
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x


# GRATZL
class Gratzl(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Gratzl", "gratzl.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT-170
        self.vel = vec(0,0)
        self.direction = "up"

    def update(self):
        if self.direction == "up":
            if self.rect.y == HEIGHT-250:
                self.direction = "down"
            else:
                self.rect.y -= 1.5
        elif self.direction == "down":
            if self.rect.y == HEIGHT - 150:
                self.direction = "up"
            else:    
                self.rect.y += 1.5
        
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class Quitas(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Gratzl", "quintas.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 300 
        self.vel = vec(0,0)

    def update(self):
        None
        
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity + vel
        self.rect.x += self.vel.x

class Schorle(pg.sprite.Sprite):
    def __init__(self, quintas):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Gratzl", "schorle.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (30, 90))
        if not quintas:
            self.image = pg.transform.rotate(self.image, 90)

        self.rect = self.image.get_rect()
        self.positions = random.randint(1,6)
        self.rect.x = WIDTH
        if self.positions == 1:
            self.rect.y = HEIGHT - 240
        elif self.positions == 2:
            self.rect.y = HEIGHT - 220
        elif self.positions == 3:
            self.rect.y = HEIGHT - 180
        elif self.positions == 4:
            self.rect.y = HEIGHT - 160
        elif self.positions == 5:
            self.rect.y = HEIGHT - 120
        else:
            self.rect.y = HEIGHT - 100
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class PlaqueFemmes(pg.sprite.Sprite):
    def __init__(self, bossRectY):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Gratzl", "plaque.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (85, 50))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = bossRectY
        self.vel = vec(0,0)
        self.acc = vec(0,2)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x
        if self.rect.y < HEIGHT - 100:
            self.vel.y += (1/20)*self.acc.y
            self.rect.y += self.acc.y + self.vel.y


# BROCHETTA
class Brochetta(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()




# SAHRAOUI
class Sahraoui(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Sahraoui", "sahraoui.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (140,140))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT-160
        self.vel = vec(0,0)


    def update(self):
        None
        
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class EnglishFile(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pathS = os.path.join(CUR_PATH, "sound", "sahraoui_haha.mp3")
        self.sound = pg.mixer.Sound(self.pathS)
        self.path1 = os.path.join(CUR_PATH, "boss", "Sahraoui", "eng_file.png")
        self.path2 = os.path.join(CUR_PATH, "boss", "Sahraoui", "tutorial.png")
        self.nbr = random.randint(0,1)
        self.images = [self.path1, self.path2]
        self.image = pg.image.load(self.images[self.nbr])
        if self.nbr:    self.image = pg.transform.scale(self.image, (100, 80))
        else:           self.image = pg.transform.scale(self.image, (60, 110))

        self.rect = self.image.get_rect()
        self.positions = random.randint(1,6)
        self.music = random.randint(0,1)
        self.rect.x = WIDTH
        if self.positions == 1:
            self.rect.y = HEIGHT - 200
        elif self.positions == 2:
            self.rect.y = HEIGHT - 190
        elif self.positions == 3:
            self.rect.y = HEIGHT - 180
        elif self.positions == 4:
            self.rect.y = HEIGHT - 170
        elif self.positions == 5:
            self.rect.y = HEIGHT - 160
        else:
            self.rect.y = HEIGHT - 150
        self.vel = vec(0,0)

        if not muting and self.music:
            self.sound.play()
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class ImmigrationBook(pg.sprite.Sprite):
    def __init__(self, bossRectY):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Sahraoui", "immigration_book.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (70, 100))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = bossRectY - random.randint(50,150)
        self.acc = vec(0,2)
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x
        if self.rect.y < HEIGHT - 150:
            self.vel.y += (1/30)*self.acc.y
            self.rect.y += self.acc.y + self.vel.y


# MOIX
class Moix(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Moix", "moix.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT-150
        self.vel = vec(0,0)

    def update(self, playerH):
        if self.rect.y < playerH:
            if self.rect.y < HEIGHT - 160:
                self.rect.y += 1  
        else:
            self.rect.y -= 1
        
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class Baguette(pg.sprite.Sprite):
    def __init__(self, bossRectY):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Moix", "micro.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (70,50))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 120
        self.rect.y = bossRectY + int(Moix().rect.height / 2)
        self.vel = vec(0,0)

    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x   

class Instument(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path1 = os.path.join(CUR_PATH, "boss", "Moix", "guitare.png")
        self.path2 = os.path.join(CUR_PATH, "boss", "Moix", "piano.png")
        self.imageNbr = random.randint(0, 1)
        self.imageList = [self.path1, self.path2]
        self.image = pg.image.load(self.imageList[self.imageNbr])
        self.image = pg.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 140
        self.vel = vec(0,0)

    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x   


# IGLESIAS
class Iglesias(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Iglesias", "iglesias.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT-160
        self.vel = vec(0,0)
        self.direction = "up"

    def update(self):
        if self.direction == "up":
            if self.rect.y == HEIGHT-300:
                self.direction = "down"
            else:
                self.rect.y -= 1
        elif self.direction == "down":
            if self.rect.y == HEIGHT - 150:
                self.direction = "up"
            else:
                self.rect.y += 1
        
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class Cable1(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Iglesias", "jack.png")
        self.lenght = random.randint(3, 8)
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120, 20))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - random.randint(55, 155)
        self.acc = vec(0,2)
        self.vel = vec(0,0)
        self.cableDel = 3
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Cable2(pg.sprite.Sprite):
    def __init__(self, cableY):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Iglesias", "cable.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (100, 15))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH 
        self.rect.y = cableY
        self.acc = vec(0,2)
        self.vel = vec(0,0)
        self.cableDel = 0
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Ordi(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path1 = os.path.join(CUR_PATH, "boss", "Iglesias", "ordi.png")
        self.path2 = os.path.join(CUR_PATH, "boss", "Iglesias", "X32.png")
        self.imageNbr = random.randint(0, 1)
        self.imageList = [self.path1, self.path2]
        self.image = pg.image.load(self.imageList[self.imageNbr])
        if self.imageNbr:   self.image = pg.transform.scale(self.image, (120,90))
        else:   self.image = pg.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 130
        self.vel = vec(0,0)

    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x   


# DONZE
class Donze(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Donze", "donze.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT-160
        self.vel = vec(0,0)
        self.direction = "up"
        self.status = random.randint(1,10)
        
    def update(self):
        if self.status < 6:
            None
        else:
            if self.direction == "up":
                if self.rect.y == HEIGHT-300:
                    self.direction = "down"
                else:
                    self.rect.y -= 5
            elif self.direction == "down":
                if self.rect.y == HEIGHT - 150:
                    self.direction = "up"
                else:
                    self.rect.y += 5

    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-self.actualis)*obstacleVelocity - vel
        self.rect.x += self.vel.x

class Voiture(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Donze", "voiture.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (160, 85))
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 100
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Brochure(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Donze", "brochure.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (75, 110))
        self.rect = self.image.get_rect()
        self.positions = random.randint(1,6)
        self.rect.x = WIDTH
        if self.positions == 1:
            self.rect.y = HEIGHT - 200
        elif self.positions == 2:
            self.rect.y = HEIGHT - 190
        elif self.positions == 3:
            self.rect.y = HEIGHT - 180
        elif self.positions == 4:
            self.rect.y = HEIGHT - 170
        elif self.positions == 5:
            self.rect.y = HEIGHT - 160
        else:
            self.rect.y = HEIGHT - 150
        self.vel = vec(0,0)
    
    def update(self, vel, obstacleVelocity):
        self.vel.x = obstacleVelocity + vel
        self.rect.x += self.vel.x

class Tumble(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(CUR_PATH, "boss", "Donze", "tumble.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - random.randint(110,130)
        self.vel = vec(0,0)
        self.acc = vec(0.1,0)
    
    def update(self):
        self.vel.x += self.acc.x 
        self.vel.y += 1 - random.randint(0,2)
        self.rect.x -= self.vel.x
        self.rect.y -= self.vel.y
        if self.rect.y > HEIGHT - 100:
            self.vel.y = -self.vel.y
    
    def death_update(self, vel, obstacleVelocity):
        self.vel.x = (-1)*obstacleVelocity - vel
        self.rect.x += self.vel.x



# BURRI