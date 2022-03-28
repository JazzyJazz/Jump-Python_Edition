from random import randint
import pygame as pg
import os
from tkinter import *
from sprites import *
from settings import *
from record import *
from decoration import *
from screenSize import *
from tkinter import messagebox
from pygame.time import Clock, get_ticks

class Main():
    def __init__(self):
        # initialisation pygame et création de la fenetre
        self.obstacleVelocity = -10
        self.running = True
        try:    self.image = pg.Surface((int(WIDTH/8), 220))
        except:     self.image = pg.Surface((300, 220))
        self.image.fill(jaune3)
        self.profs_list = ["Bouchez", "Besson", "Rochat", "Vuille", "Buchmann", "Faggioni", "Andenmatten", "Reymond", "Gratzl", "Sahraoui", "Moix", "Iglesias", "Donzé", "Gur", "Brochetta", "Burri"]
        self.player_list = ["Adrien B", "Tim", "Mateus", "Loïc", "Jasper", "Malorie", "Karim", "Oscar", "Piotr", "Adrien M", "Diego", "Simon", "Eva", "Frederike", "Matteo", "Shijie", "Evan"]
        self.playerName = random.choice(self.player_list)
        self.mute = muting
    
    def new(self, actualRecord, playerName):

        pg.init()
        pg.display.set_caption(TITLE) # génerer la fenêtre du jeu
        

        self.calibri_font = pg.font.SysFont("Calibri", 25)
        self.clock = pg.time.Clock()
        self.screenGame = pg.display.set_mode((0, 0), pg.FULLSCREEN) # definir la taille de l'ecran
        self.screenRect= self.screenGame.get_rect()
        self.col = (37, 171, 252)
                
        self.shijiePlayer = False
        self.playerName = playerName
        if self.playerName == "Shijie":
            self.shijiePlayer = True
            self.player = Player(self.playerName)
            self.playerName = random.choice(self.player_list)
        else:   self.player = Player(self.playerName)

        self.kat_active = False
        self.shield_active = False

        self.score = 0
        self.record = actualRecord
        self.counte = 0
        self.lifes = 4
        self.stun = 0
        if self.playerName == "Eva":
            self.lifes += int(0.25*self.lifes)
        
        self.mute = muting

        self.velAdd = 0
        self.spawnPlatDec = 10
        self.changeBackGrdColor = [1, 200]

        self.killCooldown = 0
        self.moonCooldown = 0
        self.extraLifeActive = False
        self.minusLifeActive = False
        self.mac = Mac()
        self.MinusLife = pg.sprite.Group()
        self.all_extraLife = pg.sprite.Group()


        self.spawnNbr = 100
        self.spawnCloud = 80
        self.spawnPlane = randint(100, 200)
        self.nbr = 0

        self.bossRotated = -1
        self.spawnBoss = randint(100, 500)
        self.spawnNbrBoss = self.spawnBoss + 100
        self.spawnNbrBossV = self.spawnNbrBoss + randint(0, 100)
        self.bossMusic = False
        self.positionTre = 0
        self.quintasActive = False
        self.bossActive = False
        self.randomProf = False
        self.textCooldown = False

        self.hardCoreMode = False
        self.mode = 1

        self.file = open("screenSize.py", "w")
        self.file.write("\nWIDTH = " + str(self.screenRect.width) + "\nHEIGHT = " + str(self.screenRect.height))

        self.all_sprites = pg.sprite.Group()
        self.all_bird = pg.sprite.Group()
        self.all_holes = pg.sprite.Group()
        self.all_obstacles = pg.sprite.Group()
        self.all_clouds = pg.sprite.Group()
        self.all_platform_dec = pg.sprite.Group()
        self.all_planes = pg.sprite.Group()
        self.p1 = pg.sprite.Group()
        self.moon = pg.sprite.Group()

        if self.bossName == "Profs":
            self.bossName = random.choice(self.profs_list)
            self.randomProf = True
        if self.bossRush:
            self.profs_list2 = self.profs_list
            self.bossName = random.choice(self.profs_list)
            self.profs_list2.remove(self.bossName)
            self.randomProf = True

        self.boss_attibutes(self.bossName)

        self.platform = Platform()
        self.bird = Bird()
        self.platform_dec = Deco_platform()
        self.hole = Hole()
        self.obstacle = Obstacle()
        self.plane = Plane()
        self.cloud = Cloud()
        self.Moon = Moon()

        self.hitP = False
        

        # self.sc = Score()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.platform)
        self.p1.add(self.platform)
        self.moon.add(self.Moon)
        
        self.run()
        pg.quit()

        return(self.record)

    def boss_attibutes(self, name):
        if name == "Besson":
            self.boss = Besson()
            self.all_bossSpawnsMissile = pg.sprite.Group()
            self.missile = Missile(self.boss.rect.y)
            self.musicBoss = os.path.join(CUR_PATH, "music", "besson.mp3")

        elif name == "Bouchez":
            self.boss = Bouchez()
            self.all_bossSpawnsChemise = pg.sprite.Group()
            self.all_bossSpawnsBanane = pg.sprite.Group()
            self.chemise = Chemise()
            self.musicBoss = os.path.join(CUR_PATH, "music", "bouchez.mp3")

        elif name == "Rochat":
            self.boss = Rochat()
            self.all_bossSpawnsKinder = pg.sprite.Group()
            self.all_bossSpawnsCoca = pg.sprite.Group()
            self.kinder = Kinder()
            self.coca = Coca()
            self.hitsCoca = 0
            self.musicBoss = os.path.join(CUR_PATH, "music", "rochat.mp3")

        elif name == "Vuille":
            self.boss = Vuille()
            self.all_bossSpawnsTM = pg.sprite.Group()
            self.tm = TM()
            self.trebuchet = Trebuchet()
            self.musicBoss = os.path.join(CUR_PATH, "music", "vuille.mp3")

        elif name == "Buchmann":
            self.boss = Buchman()
            self.all_bossSpawnsEmerentia = pg.sprite.Group()
            self.all_bossSpawnsKeyToPress = pg.sprite.Group()
            self.emerentia = Emerentia()
            self.keyToPress = PressText()
            self.musicBoss = os.path.join(CUR_PATH, "music", "buchman.mp3")

        elif name == "Faggioni":
            self.boss = Faggioni()
            self.all_bossSpawnsNotesMus = pg.sprite.Group()
            self.notesMus = NotesMus(self.boss.rect.y)
            self.musicBoss = os.path.join(CUR_PATH, "music", "faggioni.mp3")

        elif name == "Andenmatten":
            self.boss = Andenmatten()
            self.all_bossSpawnsChaussures = pg.sprite.Group()
            self.all_bossSpawnsVent = pg.sprite.Group()
            self.chaussures = Chaussures()
            self.vent = Vent(self.counte)
            self.ventBack = True
            self.musicBoss = os.path.join(CUR_PATH, "music", "andenmatten.mp3")

        elif name == "Reymond":
            self.boss = Reymond()
            self.all_bossSpawnsChimie1 = pg.sprite.Group()
            self.all_bossSpawnsChimie2 = pg.sprite.Group()
            self.all_bossSpawnsExplosion = pg.sprite.Group()
            self.chimie1 = Chimie1()
            self.chimie2 = Chimie2(self.boss.rect.y)
            self.explosion = Explosion(self.chimie1.rect.x, self.chimie1.rect.y)
            self.killChimie = random.choice([self.all_bossSpawnsChimie2, self.all_bossSpawnsChimie1])
            self.musicBoss = os.path.join(CUR_PATH, "music", "reymond.mp3")

        elif name == "Gratzl":
            self.boss = Gratzl(self.playerName)
            self.nbr = randint(0, 2)
            if self.nbr == 2:
                self.quintasActive = False
            else:
                self.boss2 = Quitas()
                self.plaque = PlaqueFemmes(self.boss2.rect.y)
                self.quintasActive = True
            self.all_bossSpawnsPlaques = pg.sprite.Group()
            self.schorle = Schorle(self.quintasActive)
            self.all_bossSpawnsSchorle = pg.sprite.Group()
            self.musicBoss = os.path.join(CUR_PATH, "music", "gratzl.mp3")

        elif name == "Sahraoui":
            self.boss = Sahraoui()
            self.all_bossSpawnsImmigrationBook = pg.sprite.Group()
            self.all_bossSpawnsEnglishFile = pg.sprite.Group()
            self.musicBoss = os.path.join(CUR_PATH, "music", "sahraoui.mp3")

        elif name == "Moix":
            self.boss = Moix()
            self.all_bossSpawnsInstument = pg.sprite.Group()
            self.all_bossSpawnsBaguette = pg.sprite.Group()
            self.musicBoss = os.path.join(CUR_PATH, "music", "moix.mp3")

        elif name == "Iglesias":
            self.boss = Iglesias()
            self.cable1 = Cable1()
            self.cable = Cable1()
            self.all_bossSpawnsCable = pg.sprite.Group()
            self.all_bossSpawnsOrdi = pg.sprite.Group()
            self.musicBoss = os.path.join(CUR_PATH, "music", "iglesias.mp3")
            self.nbrCab = 0

        elif name == "Donzé":
            self.boss = Donze()
            self.boss.status = randint(1,10)
            self.nbrDonz = randint(0,4)
            if self.nbrDonz < 3:
                self.bossName = "Tumble"
                self.all_bossSpawnsTumble = pg.sprite.Group()
                self.boss = Tumble()
            else:
                self.all_bossSpawnsVoiture = pg.sprite.Group()
                self.all_bossSpawnsBrochure = pg.sprite.Group()
                self.brochure = Brochure()
                self.voiture = Voiture()
            self.musicBoss = os.path.join(CUR_PATH, "music", "moix.mp3")

        elif name == "Gur":
            self.boss = Gur()
            self.all_bossSpawnsBallon = pg.sprite.Group()
            self.musicBoss = os.path.join(CUR_PATH, "music", "besson.mp3")
        
        elif name == "Brochetta":
            self.boss = Brochetta()
            self.all_bossSpawnsChromosomes = pg.sprite.Group()
            self.all_bossSpawnsBacteria = pg.sprite.Group()
            self.musicBoss = os.path.join(CUR_PATH, "music", "besson.mp3")
        
        elif name == "Burri":
            self.boss = Burri()
            self.all_bossSpawnsFumer = pg.sprite.Group()
            self.all_bossSpawnsAntigone = pg.sprite.Group()
            self.musicBoss = os.path.join(CUR_PATH, "music", "bouchez.mp3")



    def run(self):
        # Boucle du jeu
        self.playing = True
        while self.playing:
            self.tick = pg.time.get_ticks()
            self.clock.tick(FPS)
            self.event()
            self.update()
            self.draw()

    def update(self):
        # Boucle du jeu - mise à jour

        self.counte += 1

        self.score = int(self.counte/5)   

        if self.record < self.score:
            self.record = self.score

        self.velAdd -= acceleration

        ######

        if self.stun == 0:  
            self.player.update(self.playerName)
            if self.playerName == "Adrien B":
                self.n = random.randint(0,330)
        elif self.stun == 1 and self.playerName == "Adrien B":  
            self.all_sprites.remove(self.mac)
            self.stun = 0
            self.path = os.path.join(CUR_PATH, "players", f"Adrien B.png")
            self.player.image = pg.image.load(self.path)
            self.player.image = pg.transform.scale(self.player.image, (80,100))
        else:
            self.stun -= 1

        if self.player.rect.y < -200:
            self.playing = False

        if (self.counte-1)%3000 == 0:
            if self.playerName == "Tim":
                self.lifes += 1
                self.kat_active = True
                self.kat_sup = Kat_Support()
                self.all_sprites.add(self.kat_sup)

            elif self.playerName == "Jasper":
                if not self.shield_active:
                    self.shield = Shield()
                    self.shield_active = True
                    self.all_sprites.add(self.shield)
        
        if self.kat_active:
            self.kat_sup.update()
            if self.kat_sup.rect.y < -100:
                self.kat_active = False
                self.all_sprites.remove(self.kat_sup)

        if self.shield_active:
            self.shield.update(self.player.rect.y)
        
                
        ########
        
        for self.bird in self.all_bird:
            self.bird.update(self.velAdd, self.obstacleVelocity)
            
            if self.bird.rect.x < -100 :
                self.all_bird.remove(self.bird)

        for self.hole in self.all_holes:
            self.hole.update(self.velAdd, self.obstacleVelocity)
            if self.hardCoreMode:
                self.hole.image.fill((randint(1,250), randint(1,250), randint(1,250)))
            elif self.changeBackGrdColor[0] == 1:
                self.hole.image.fill((37, 171, 252))
            elif self.changeBackGrdColor[0] == 2:
                self.hole.image.fill(grey)

            if self.hole.rect.x < -100 :
                self.all_holes.remove(self.hole)

        for self.obstacle in self.all_obstacles:
            self.obstacle.update(self.velAdd, self.obstacleVelocity)
            if self.obstacle.rect.x < -100:
                self.all_obstacles.remove(self.obstacle)
        
        for self.plane in self.all_planes:
            self.plane.update(self.velAdd, self.obstacleVelocity)

            if self.plane.rect.x < -100:
                self.all_planes.remove(self.plane)
        
        if self.bossActive:
            if self.bossName == "Faggioni":
                self.boss.update(self.player.rect.y)
            elif self.bossName == "Moix":
                self.boss.update(self.player.rect.y)
            elif self.bossName == "Burri" and self.playerName == "Adrien B" and self.stun == 0 and self.n == 1:
                self.stun = 50
                self.all_sprites.add(self.mac)
                self.path = os.path.join(CUR_PATH, "players", f"Adrien B2.png")
                self.player.image = pg.image.load(self.path)
                self.player.image = pg.transform.scale(self.player.image, (80,100))

            
            else:
                self.boss.update()
                if self.quintasActive:
                    self.boss2.update()

            if not self.bossMusic and not self.mute:
                pg.mixer.init()
                pg.mixer.music.load(self.musicBoss)
                pg.mixer.music.play(-1)
                self.bossMusic = True
            if self.counte == self.spawnBoss + 1:
                self.boss.rect.x = WIDTH - 150
                if self.bossName == "Gratzl":
                    if self.quintasActive:
                        self.boss2.rect.x = WIDTH - 200

        if self.bossName == "Bouchez":
            for self.chemise in self.all_bossSpawnsChemise:
                self.chemise.update(self.velAdd, self.obstacleVelocity)
                if self.chemise.rect.x < -100:
                    self.all_bossSpawnsChemise.remove(self.chemise)
            for self.banane in self.all_bossSpawnsBanane:
                self.banane.update(self.velAdd, self.obstacleVelocity)
                if self.banane.rect.x < -100:
                    self.all_bossSpawnsBanane.remove(self.banane)
        
        elif self.bossName == "Besson":
            for self.missile in self.all_bossSpawnsMissile:
                self.missile.update(self.velAdd, self.obstacleVelocity)
                if self.missile.rect.x < -100:
                    self.all_bossSpawnsMissile.remove(self.missile)
        
        elif self.bossName == "Rochat":
            for self.kinder in self.all_bossSpawnsKinder:
                self.kinder.update(self.velAdd, self.obstacleVelocity)
                if self.kinder.rect.x < -100:
                    self.all_bossSpawnsKinder.remove(self.kinder)
            for self.coca in self.all_bossSpawnsCoca:
                self.coca.update(self.velAdd, self.obstacleVelocity)
                if self.coca.rect.x < -100:
                    self.all_bossSpawnsCoca.remove(self.coca)
        
        elif self.bossName == "Vuille":
            for self.tm in self.all_bossSpawnsTM:
                self.tm.update(self.velAdd, self.obstacleVelocity)
                if self.tm.rect.x < -100:
                    self.all_bossSpawnsTM.remove(self.tm)
        
        elif self.bossName == "Buchmann":
            for self.emerentia in self.all_bossSpawnsEmerentia:
                self.emerentia.update(self.velAdd, self.obstacleVelocity)
                if self.emerentia.rect.x < -100:
                    self.all_bossSpawnsEmerentia.remove(self.emerentia)
            for self.keyToPress in self.all_bossSpawnsKeyToPress:
                self.keyToPress.update()

                if self.counte == self.spawnNbrBoss + 200:
                    if self.playerName == "Simon":
                        if not self.keyToPress.death:
                            self.lifes += 1
                    else:
                        if self.keyToPress.death:
                                self.playing = False
                        self.all_bossSpawnsKeyToPress.remove(self.keyToPress)
                        self.spawnNbrBoss += randint(201, 250)
                if self.counte == self.spawnNbrBoss + 180 and self.playerName == "Piotr":
                    if self.keyToPress.death:
                        self.playing = False
                    self.all_bossSpawnsKeyToPress.remove(self.keyToPress)
                    self.spawnNbrBoss += randint(201, 250)

        elif self.bossName == "Faggioni":
             for self.notesMus in self.all_bossSpawnsNotesMus:
                self.notesMus.update(self.velAdd, self.obstacleVelocity)
                if self.notesMus.rect.x < -100:
                    self.all_bossSpawnsNotesMus.remove(self.notesMus)
        
        if self.bossName == "Andenmatten":
            for self.chaussures in self.all_bossSpawnsChaussures:
                self.chaussures.update(self.velAdd, self.obstacleVelocity)
                if self.chaussures.rect.x < -500:
                    self.all_bossSpawnsChaussures.remove(self.chaussures)
            for self.vent in self.all_bossSpawnsVent:
                if self.obstacleVelocity < 0:
                    if self.vent.nbr == 2:
                        self.obstacleVelocity = -self.obstacleVelocity
                        self.ventBack = False
                    elif self.vent.nbr == 3 and self.obstacleVelocity >= -10:
                        self.obstacleVelocity = 1.4*self.obstacleVelocity
                if self.vent.nbr == 1:
                    self.player.vel.y = -10

                if self.counte == self.vent.time + 200:
                    if self.vent.nbr == 2:
                        self.obstacleVelocity -= 2*self.obstacleVelocity
                        self.ventBack = True
                    elif self.vent.nbr == 3:
                        self.obstacleVelocity -= (1/5) *self.obstacleVelocity
                    self.all_bossSpawnsVent.remove(self.vent)
        
        elif self.bossName == "Reymond":
            for self.chimie1 in self.all_bossSpawnsChimie1:
                self.chimie1.update(self.velAdd, self.obstacleVelocity)
                if self.chimie1.rect.x < -100:
                    self.all_bossSpawnsChimie1.remove(self.chimie1)
            for self.chimie2 in self.all_bossSpawnsChimie2:
                self.chimie2.update(self.velAdd, self.obstacleVelocity)
                if self.chimie2.rect.x < -100:
                    self.all_bossSpawnsChimie2.remove(self.chimie2)
            for self.explosion in self.all_bossSpawnsExplosion:
                self.explosion.update(self.velAdd, int((3/4)*self.obstacleVelocity))
                if self.explosion.rect.x < -100:
                    self.all_bossSpawnsExplosion.remove(self.explosion)
        
        elif self.bossName == "Gratzl":
            for self.schorle in self.all_bossSpawnsSchorle:
                if self.quintasActive:  self.schorle.update(self.velAdd, self.obstacleVelocity)  
                else:   self.schorle.update(self.velAdd, (1.5)*self.obstacleVelocity)

                if self.schorle.rect.x < -100:
                    self.all_bossSpawnsSchorle.remove(self.schorle)
            if self.quintasActive:
                for self.plaque in self.all_bossSpawnsPlaques:
                    self.plaque.update(self.velAdd, self.obstacleVelocity)
                    if self.plaque.rect.x < -100:
                        self.all_bossSpawnsPlaques.remove(self.plaque)
        
        elif self.bossName == "Sahraoui":
            for self.immigrationBook in self.all_bossSpawnsImmigrationBook:
                self.immigrationBook.update(self.velAdd, self.obstacleVelocity)
                if self.immigrationBook.rect.x < -100:
                    self.all_bossSpawnsImmigrationBook.remove(self.immigrationBook)
            for self.englishFile in self.all_bossSpawnsEnglishFile:
                self.englishFile.update(self.velAdd, self.obstacleVelocity)
                if self.englishFile.rect.x < -100:
                    self.all_bossSpawnsEnglishFile.remove(self.englishFile)
        
        elif self.bossName == "Moix":
            for self.baguette in self.all_bossSpawnsBaguette:
                self.baguette.update(self.velAdd, self.obstacleVelocity)
                if self.baguette.rect.x < -100:
                    self.all_bossSpawnsBaguette.remove(self.baguette)
            for self.instu in self.all_bossSpawnsInstument:
                self.instu.update(self.velAdd, self.obstacleVelocity)
                if self.instu.rect.x < -100:
                    self.all_bossSpawnsInstument.remove(self.instu)
        
        elif self.bossName == "Iglesias":
            for self.cable in self.all_bossSpawnsCable:
                self.cable.update(self.velAdd, self.obstacleVelocity)
                if self.cable.rect.x < -1000:
                    self.all_bossSpawnsCable.remove(self.cable)
            for self.ordi in self.all_bossSpawnsOrdi:
                self.ordi.update(self.velAdd, self.obstacleVelocity)
                if self.ordi.rect.x < -100:
                    self.all_bossSpawnsOrdi.remove(self.ordi)
        
        elif self.bossName == "Donzé":
            for self.voit in self.all_bossSpawnsVoiture:
                self.voit.update(self.velAdd, self.obstacleVelocity)
                if self.voit.rect.x < -100:
                    self.all_bossSpawnsVoiture.remove(self.voit)
            for self.broch in self.all_bossSpawnsBrochure:
                self.broch.update(self.velAdd, self.obstacleVelocity)
                if self.broch.rect.x < -100:
                    self.all_bossSpawnsBrochure.remove(self.broch)
        
        elif self.bossName == "Tumble":
            for self.tumble in self.all_bossSpawnsTumble:
                self.tumble.update()
                if self.tumble.rect.x < -100:
                    self.all_bossSpawnsTumble.remove(self.tumble)
        
        elif self.bossName == "Gur":
            for self.ballon in self.all_bossSpawnsBallon:
                self.ballon.update(self.velAdd, self.obstacleVelocity)
                if self.ballon.rect.x < -100:
                    self.all_bossSpawnsBallon.remove(self.ballon)
        
        elif self.bossName == "Brochetta":
            for self.chromo in self.all_bossSpawnsChromosomes:
                self.chromo.update(self.velAdd, self.obstacleVelocity)
                if self.chromo.rect.x < -100:
                    self.all_bossSpawnsChromosomes.remove(self.chromo)
            for self.bact in self.all_bossSpawnsBacteria:
                self.bact.update(self.velAdd, self.obstacleVelocity)
                if self.bact.rect.x < -100:
                    self.all_bossSpawnsBacteria.remove(self.bact)

        elif self.bossName == "Burri":
            for self.antig in self.all_bossSpawnsAntigone:
                self.antig.update(self.velAdd, self.obstacleVelocity)
                if self.antig.rect.x < -100:
                    self.all_bossSpawnsAntigone.remove(self.antig)
            for self.fume in self.all_bossSpawnsFumer:
                self.fume.update(self.velAdd, self.obstacleVelocity)
                if self.fume.rect.x < -100:
                    self.all_bossSpawnsFumer.remove(self.fume)

            

        if self.counte == self.spawnBoss + 1000:
            self.bossActive = False
            if self.bossName == "Rochat":
                self.obstacleVelocity += 2*self.hitsCoca
                self.hitsCoca = 0
            elif self.bossName == "Andenmatten":
                if self.obstacleVelocity != -10:
                    self.obstacleVelocity = -10
                    self.velAdd = -self.counte*acceleration

        if self.counte > self.spawnBoss + 1000: 
            self.boss.death_update(self.velAdd, self.obstacleVelocity)
            if self.bossName == "Gratzl":
                if self.quintasActive:
                    self.boss2.death_update(self.velAdd, self.obstacleVelocity)
            
            if self.boss.rect.x < -100 or self.boss.rect.x > WIDTH + 100:
                self.all_sprites.remove(self.boss)
                self.lifes += 1
                self.extraLife = ExtraLife(WIDTH-100, HEIGHT-150)
                self.all_extraLife.add(self.extraLife)
                self.extraLifeActive = True
                if self.playerName == "Malorie":
                    if self.bossName == "Gur":
                        self.lifes += 1
                
                if self.bossName == "Gratzl":
                    if self.quintasActive:
                        self.all_sprites.remove(self.boss2)
                if self.bossName == "Tumble" or self.bossName == "Donzé":
                    self.boss_attibutes("Donzé")
                    
                if self.bossRush and self.profs_list2 != []:
                    self.spawnBoss = self.counte + 1
                else:
                    self.spawnBoss += randint(2500, 3500)
                self.bossMusic = False
                if not self.mute:
                    self.path = os.path.join(CUR_PATH, "music", "music.mp3")
                    pg.mixer.init()
                    pg.mixer.music.load(self.path)
                    pg.mixer.music.play(-1)
                if self.randomProf:
                    if self.bossRush:
                        if self.profs_list2 != [] and not self.textCooldown:
                            self.bossName = random.choice(self.profs_list2)
                            self.profs_list2.remove(self.bossName)
                        else:
                            self.text = Text("VOUS AVEZ BATTU TOUS LES BOSS !!!")
                            self.all_sprites.add(self.text)
                            self.textCooldown = True
                            self.spawnBoss = self.counte + 300
                            self.profs_list2 = ["Bouchez", "Besson", "Rochat", "Vuille", "Buchmann", "Faggioni", "Andenmatten", "Reymond", "Gratzl", "Sahraoui", "Moix", "Iglesias", "Donzé", "Gur", "Brochetta", "Burri"]
                            
                            
                    else:
                        self.bossName = random.choice(self.profs_list)
                    self.boss_attibutes(self.bossName)

            if self.bossName == "Vuille":
                self.all_sprites.remove(self.trebuchet)
            elif self.bossName == "Buchmann":
                self.keyToPress.death = False
                self.all_bossSpawnsKeyToPress.remove(self.keyToPress)

        for self.cloud in self.all_clouds:
            self.cloud.update(self.velAdd/5)
            if self.cloud.rect.x < 20:
                self.all_clouds.remove(self.cloud)
        
        if self.changeBackGrdColor[0] == 2:
            self.Moon.update(self.counte)
            if self.moonCooldown > 0:
                self.moonCooldown -= 1
        
        for self.eL in self.all_extraLife:
            self.eL.update(self.col)
            if self.eL.rect.y == 0:
                self.all_extraLife.remove(self.eL)
                self.extraLifeActive = False
        for self.minusLife in self.MinusLife:
            self.minusLife.update(self.col)
            if self.minusLife.rect.x < int(WIDTH/2)-200:
                self.MinusLife = None
                self.MinusLife = pg.sprite.Group()
    
        for self.platform_dec in self.all_platform_dec:
            self.platform_dec.update(self.velAdd, self.obstacleVelocity)

            if self.hardCoreMode:
                self.platform_dec.image.fill((randint(1,250), randint(1,250), randint(1,250)))
            elif self.changeBackGrdColor[0] == 1:
                self.platform_dec.image.fill((37, 171, 252))
            elif self.changeBackGrdColor[0] == 2:
                self.platform_dec.image.fill(grey)

            if self.platform_dec.rect.x < -300:
                self.all_platform_dec.remove(self.platform_dec)

        self.hitsPP = pg.sprite.spritecollide(self.player, self.p1, False)
        if self.hitsPP:
            self.player.pos.y = self.hitsPP[0].rect.top + 1
            self.player.acc.y = 0
            self.player.vel.y = 0
        
        self.hitsPMoon = pg.sprite.spritecollide(self.player, self.moon, False)
        if self.hitsPMoon and self.moonCooldown == 0 and self.playerName != "Mateus":
            self.lifes += 1
            self.moonCooldown = 1000
            self.extraLife = ExtraLife(self.player.rect.x , self.player.rect.y)
            self.all_extraLife.add(self.extraLife)
            self.extraLifeActive = True
        
        ############

        self.hitsPB = pg.sprite.spritecollide(self.player, self.all_bird, False)
        self.hitsPH = pg.sprite.spritecollide(self.player, self.all_holes, False)
        self.hitsPO = pg.sprite.spritecollide(self.player, self.all_obstacles, False)
        self.hitsPP = pg.sprite.spritecollide(self.player, self.all_planes, False)

        if self.hitsPB or self.hitsPH or self.hitsPO or self.hitsPP: 
            self.hitP = 1

        if self.bossName == "Bouchez":
            self.hitsPBossB = pg.sprite.spritecollide(self.player, self.all_bossSpawnsBanane, False)
            self.hitsPBossC = pg.sprite.spritecollide(self.player, self.all_bossSpawnsChemise, False)
            if self.hitsPBossB or self.hitsPBossC:
                self.hitP = 1
                if self.playerName == "Matteo":
                    self.hitP = 3

        elif self.bossName == "Besson":
            self.hitsPBossM = pg.sprite.spritecollide(self.player, self.all_bossSpawnsMissile, False)
            if self.hitsPBossM:
                self.hitP = 1
                if self.playerName == "Adrien M":
                    self.hitP -= random.randint(0,1)
                    if self.hitP == 0:
                        self.killCooldown = 10
 
        elif self.bossName == "Rochat":
            self.hitsPBossK = pg.sprite.spritecollide(self.player, self.all_bossSpawnsKinder, False)
            self.hitsPBossC = pg.sprite.spritecollide(self.player, self.all_bossSpawnsCoca, False)
            self.hitsBossK = pg.sprite.spritecollide(self.boss, self.all_bossSpawnsKinder, False)
            self.hitsBossC = pg.sprite.spritecollide(self.boss, self.all_bossSpawnsCoca, False)
            if self.hitsPBossK:
                self.hitP = 1
                if self.playerName == "Diego":
                    self.hitP = 3
                if self.playerName == "Karim":
                    self.hitP -= random.randint(0,1)

            if self.hitsPBossC:
                if self.playerName != "Karim":
                    self.hitsCoca += 4
                    self.obstacleVelocity -= 6
                    self.all_bossSpawnsCoca.remove(self.coca)
            if self.hitsBossK:
                self.kinder.eaten()
                self.bossRotated = 20
                self.boss.image = pg.transform.scale(self.boss.image, (140,120))
            if self.hitsBossC:
                self.all_bossSpawnsCoca.remove(self.coca)
                self.bossRotated = 20
                self.boss.image = pg.transform.scale(self.boss.image, (140,120))

        elif self.bossName == "Vuille":
            self.hitsPBossTM = pg.sprite.spritecollide(self.player, self.all_bossSpawnsTM, False)
            if self.hitsPBossTM:
                self.hitP = 1
                if self.playerName == "Simon":
                    self.hitP = 100
                elif self.playerName == "Eva":
                    self.hitP = 2

        elif self.bossName == "Buchmann":
            self.hitsPBossE = pg.sprite.spritecollide(self.player, self.all_bossSpawnsEmerentia, False)
            if self.hitsPBossE:
                self.hitP = 1

        elif self.bossName == "Faggioni":
            self.hitsPBossN = pg.sprite.spritecollide(self.player, self.all_bossSpawnsNotesMus, False)
            if self.hitsPBossN:
                self.hitP = 1
                if self.playerName == "Loïc":
                    self.hitP = 2*random.randint(0,1)
                    if self.hitP == 0:
                        self.killCooldown = 10

        elif self.bossName == "Andenmatten":
            self.hitsPBossC = pg.sprite.spritecollide(self.player, self.all_bossSpawnsChaussures, False)
            if self.hitsPBossC:
                self.hitP = 1
        
        elif self.bossName == "Reymond":
            self.hitsPBossC = pg.sprite.spritecollide(self.player, self.killChimie, False)
            self.hitsPBossE = pg.sprite.spritecollide(self.player, self.all_bossSpawnsExplosion, False)
            if self.hitsPBossC or self.hitsPBossE:
                self.hitP = 1
                if self.playerName == "Evan":
                    self.hitP = 2

            for self.chimie1 in self.all_bossSpawnsChimie1:
                self.hitsC1C2 = pg.sprite.spritecollide(self.chimie1, self.all_bossSpawnsChimie2, False)
                if self.hitsC1C2:
                    self.all_bossSpawnsChimie1.remove(self.chimie1)
                    self.all_bossSpawnsChimie2.remove(self.chimie2)
                    self.all_bossSpawnsExplosion.add(Explosion(self.chimie1.rect.x, self.chimie1.rect.y))
                    self.bossRotated = 60
                    self.path = os.path.join(CUR_PATH, "boss", "Reymond", "reymond2.png")
                    self.boss.image = pg.image.load(self.path)
                    self.boss.image = pg.transform.scale(self.boss.image, (130,130))

            for self.chimie in self.killChimie:
                self.hitsCEx = pg.sprite.spritecollide(self.chimie, self.all_bossSpawnsExplosion, False)
                if self.hitsCEx:
                    self.exDim = ()
                    self.killChimie.remove(self.chimie)
                    self.explosion.image = pg.transform.scale(self.explosion.image, (150, 150))
                    self.bossRotated = 40
                    self.path = os.path.join(CUR_PATH, "boss", "Reymond", "reymond2.png")
                    self.boss.image = pg.image.load(self.path)
                    self.boss.image = pg.transform.scale(self.boss.image, (130,130))
        
        elif self.bossName == "Gratzl":
            self.hitsPBossS = pg.sprite.spritecollide(self.player, self.all_bossSpawnsSchorle, False)
            if self.quintasActive:
                self.hitsPBossP = pg.sprite.spritecollide(self.player, self.all_bossSpawnsPlaques, False)
                if self.hitsPBossP:
                    self.hitP = 1
            if self.hitsPBossS:
                self.hitP = 1
                if self.playerName == "Piotr":
                    self.hitP = 0
                    self.killCooldown = 10
        
        elif self.bossName == "Sahraoui":
            self.hitsPBossI = pg.sprite.spritecollide(self.player, self.all_bossSpawnsImmigrationBook, False)
            self.hitsPBossE = pg.sprite.spritecollide(self.player, self.all_bossSpawnsEnglishFile, False)
            if self.hitsPBossI:
                self.hitP = 1
                if self.playerName == "Oscar":
                    self.hitP = 0
                    self.killCooldown = 10
            if self.hitsPBossE:
                self.hitP = 1
                if self.playerName == "Adrien M":
                    self.hitP = 3
        
        elif self.bossName == "Moix":
            self.hitsPBossB = pg.sprite.spritecollide(self.player, self.all_bossSpawnsBaguette, False)
            self.hitsPBossI = pg.sprite.spritecollide(self.player, self.all_bossSpawnsInstument, False)
            if self.hitsPBossB:
                self.hitP = 1
                if self.playerName == "Karim":
                    self.hitP = 2
            if self.hitsPBossI:
                self.hitP = 1 
                if self.playerName == "Diego":
                    self.hitP = 0
                    self.killCooldown = 10

        elif self.bossName == "Iglesias":
            self.hitsPBossC = pg.sprite.spritecollide(self.player, self.all_bossSpawnsCable, False)
            self.hitsPBossO = pg.sprite.spritecollide(self.player, self.all_bossSpawnsOrdi, False)
            if self.hitsPBossC:
                self.hitP = 1
                if self.playerName == "Oscar":
                    self.hitP = 2
            if self.hitsPBossO:
                self.hitP = 1
                if self.playerName == "Adrien B":
                    self.hitP = 0
                    self.killCooldown = 10
                if self.playerName == "Oscar":
                    self.hitP = 2

        elif self.bossName == "Donzé":
            self.hitsPBossV = pg.sprite.spritecollide(self.player, self.all_bossSpawnsVoiture, False)
            self.hitsPBossB = pg.sprite.spritecollide(self.player, self.all_bossSpawnsBrochure, False)
            if self.hitsPB or self.hitsPH or self.hitsPO or self.hitsPP or self.hitsPBossV or self.hitsPBossB:
                self.hitP = 1
        
        elif self.bossName == "Tumble":
            if self.hitsPB or self.hitsPH or self.hitsPO or self.hitsPP:
                self.hitP = 1
        
        elif self.bossName == "Gur":
            self.hitsPBossB = pg.sprite.spritecollide(self.player, self.all_bossSpawnsBallon, False)
            if self.hitsPBossB:
                self.hitP = 1
                if self.playerName == "Evan":
                    self.hitP -= random.randint(0,1)
                    if self.hitP == 0:
                        self.killCooldown = 10
        
        elif self.bossName == "Brochetta":
            self.hitsPBossB = pg.sprite.spritecollide(self.player, self.all_bossSpawnsBacteria, False)
            self.hitsPBossC = pg.sprite.spritecollide(self.player, self.all_bossSpawnsChromosomes, False)
            if self.hitsPBossB:
                self.hitP = 1
            elif self.hitsPBossC:
                self.hitP = 1
                if self.playerName == "Jasper":
                    self.hitP = 4
        
        elif self.bossName == "Burri":
            self.hitsPBossA = pg.sprite.spritecollide(self.player, self.all_bossSpawnsAntigone, False)
            self.hitsPBossF = pg.sprite.spritecollide(self.player, self.all_bossSpawnsFumer, False)
            if self.hitsPBossA:
                self.hitP = 1
            if self.hitsPBossF:
                self.hitP = 1
                if self.playerName == "Frederike":
                    self.hitP = 0

        if self.lifes < 1:
            self.file = open("record.py", "w")
            self.file.write("\nrecord = " + str(self.record))
            self.playing = False
        else:
            if self.hitP > 0 and (self.killCooldown == 0):
                self.killCooldown = 100
                if self.playerName == "Tim":
                    self.hitsTim = self.hitP + int(random.randint(1,5)/5)
                    self.lifes -= self.hitsTim
                    if self.hitsTim == 2:
                        self.MinusLife.add(MinusLife(self.player.rect.x , self.player.rect.y, 1))
                        self.MinusLife.add(MinusLife(self.player.rect.x , self.player.rect.y, 2))
                        self.MinusLife.add(MinusLife(self.player.rect.x -10, self.player.rect.y, 1))
                        self.MinusLife.add(MinusLife(self.player.rect.x -10, self.player.rect.y, 2))
                        self.minusLifeActive = True
                    else: 
                        self.MinusLife.add(MinusLife(self.player.rect.x , self.player.rect.y, 1))
                        self.MinusLife.add(MinusLife(self.player.rect.x , self.player.rect.y, 2))
                        self.minusLifeActive = True




                elif self.playerName == "Mateus":
                    self.hitsMateus = self.hitP - int(random.randint(1,4)/4)
                    self.lifes -= self.hitsMateus
                    if self.hitsMateus != 0:
                        self.MinusLife.add(MinusLife(self.player.rect.x , self.player.rect.y, 1))
                        self.MinusLife.add(MinusLife(self.player.rect.x , self.player.rect.y, 2))
                        self.minusLifeActive = True
                else:
                    if not self.shield_active:
                        self.lifes -= self.hitP
                        for x in range(self.hitP):
                            self.MinusLife.add(MinusLife(self.player.rect.x -10*x, self.player.rect.y, 1))
                            self.MinusLife.add(MinusLife(self.player.rect.x -10*x, self.player.rect.y, 2))
                        self.minusLifeActive = True
                    else:
                        self.shield_active = False
                        self.all_sprites.remove(self.shield)

                self.hitP = 0
                
            else:
                self.hitP = 0
                if self.killCooldown > 0:
                    self.killCooldown -= 1



    def event(self):
        # Boucle du jeu - evenement   
        for event in pg.event.get():
            #check si le joueur a fermé la fenetre. si oui, il arrete le programe
            if event.type == pg.QUIT:
                self.file = open("record.py", "w")
                self.file.write("\nrecord = " + str(self.record))
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    self.playing = False
                    self.file = open("record.py", "w")
                    self.file.write("\nrecord = " + str(self.record))
                if (event.key == pg.K_LCTRL or event.key == pg.K_DOWN) and self.stun == 0 :
                    self.player.vel.y = 0
                    self.player.image = pg.transform.scale(self.player.image, (20,25))
                    self.player.rect.x = HEIGHT -50
                    self.player.rect = self.player.image.get_rect()
                    self.player.pos = vec(WIDTH / 2, HEIGHT-50)
            elif event.type == pg.KEYUP:
                if (event.key == pg.K_LCTRL or event.key == pg.K_DOWN) and self.stun == 0:
                    self.player.image = pg.transform.scale(self.player.image, (80,100))
                    try: 
                        if self.shijiePlayer:   self.player.image = pg.image.load(os.path.join(CUR_PATH, "players", "Shijie.png"))
                        else:   self.player.image = pg.image.load(os.path.join(CUR_PATH, "players", f"{self.playerName}.png"))
                        self.player.image = pg.transform.scale(self.player.image, (80,100))
                    except: None
                    self.player.rect = self.player.image.get_rect()
                    self.player.pos = vec(WIDTH / 2, HEIGHT-50)
    
    def draw(self):
        # Boucle du jeu - "dessiner"
        
        # definit la couleur de la fenêtre
        if self.changeBackGrdColor[1] == self.score:
            if self.hardCoreMode:
                self.hardCoreMode = False
            if self.mode == 1:
                if self.changeBackGrdColor[0] == 2:
                    self.mode = 2
                else:
                    pass
                if self.changeBackGrdColor[0] == 1:
                    self.changeBackGrdColor[0] = 2
                elif self.changeBackGrdColor[0] == 2:
                    self.changeBackGrdColor[0] = 1
            elif self.mode == 2:
                self.mode = 1
                self.hardCoreMode = True
            self.changeBackGrdColor[1] += 200



        if self.hardCoreMode:
            self.screenGame.fill((randint(1,250), randint(1,250), randint(1,250)))
            self.platform.image.fill((randint(1,250), randint(1,250), randint(1,250)))
            self.platform.image2.fill((randint(1,250), randint(1,250), randint(1,250)))

        elif self.changeBackGrdColor[0] == 1:
            self.col = (37, 171, 252)
            self.screenGame.fill((37, 171, 252))
            self.platform.image.fill(jaune2)
            self.platform.image2.fill(jaune3)
            try: self.all_sprites.remove(self.Moon)
            except: None

        elif self.changeBackGrdColor[0] == 2:
            self.col = grey
            self.screenGame.fill(grey)
            self.platform.image.fill(jaune2)
            self.platform.image2.fill(jaune3)
            self.all_sprites.add(self.Moon)

            
        


        # afficher les sprites
        self.all_sprites.draw(self.screenGame)

        if self.counte == self.spawnCloud:
            self.all_clouds.add(Cloud())
            self.spawnCloud += randint(400 , 1000)

        if self.counte == self.spawnPlatDec:
            self.all_platform_dec.add(Deco_platform())
            self.spawnPlatDec += randint(1, 3)

        if self.counte == self.spawnBoss:
            self.all_sprites.add(self.boss)
            if self.bossName == "Vuille":
                self.all_sprites.add(self.trebuchet)
            if self.bossName == "Gratzl":
                if self.quintasActive:
                    self.all_sprites.add(self.boss2)
            self.bossActive = True
            self.textCooldown = False
            try:    self.all_sprites.remove(self.text)
            except: None
        
        if self.bossActive:

            if self.bossName == "Bouchez":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    self.path = os.path.join(CUR_PATH, "boss", "Bouchez", "bouchez.png")
                    if self.nbr < 60:
                        self.all_bossSpawnsChemise.add(Chemise())
                        self.boss.image = pg.image.load(self.path)
                        self.boss.image = pg.transform.scale(self.boss.image, (150, 150))
                        self.bossRotated = 20
                        self.spawnNbrBoss += randint(50, 100)
                    else:
                        self.all_bossSpawnsBanane.add(Banane(self.playerName))
                        self.boss.image = pg.image.load(self.path)
                        self.boss.image = pg.transform.scale(self.boss.image, (150, 150))
                        self.bossRotated = 20
                        self.spawnNbrBoss += randint(50, 100)

                if self.bossRotated == 0:
                    self.boss.image = pg.transform.scale(self.boss.image, (120, 120))
                    self.bossRotated = -1
                elif self.bossRotated > 0:
                    self.bossRotated -= 1

            elif self.bossName == "Besson":
                if self.counte == self.spawnNbrBoss:
                    self.boss.image = pg.transform.rotate(self.boss.image, 90)
                    self.bossRotated = 19
                    self.all_bossSpawnsMissile.add(Missile(self.boss.rect.y))
                    self.spawnNbrBoss += randint(20, 80)

                if self.bossRotated == 0:
                    self.boss.image = pg.transform.rotate(self.boss.image, -90)
                    self.bossRotated = -1
                elif self.bossRotated > 0:
                    self.bossRotated -= 1

            elif self.bossName == "Rochat":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    if self.nbr < 75:
                        self.all_bossSpawnsKinder.add(Kinder())
                        self.spawnNbrBoss += randint(int(50/(self.hitsCoca + 2)), 80)
                    else:
                        self.all_bossSpawnsCoca.add(Coca())
                        self.spawnNbrBoss += randint(int(50/(self.hitsCoca + 2)), 80)

                if self.bossRotated == 0:
                    self.path = os.path.join(CUR_PATH, "boss", "Rochat", "rochat.png")
                    self.boss.image = pg.image.load(self.path)
                    self.boss.image = pg.transform.scale(self.boss.image, (120,120))
                    self.bossRotated = -1
                elif self.bossRotated > 0:
                    self.bossRotated -= 1

            elif self.bossName == "Vuille":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    if self.nbr > 70:
                        self.trebuchet.update(1)
                        self.all_bossSpawnsTM.add(TM())
                        self.spawnNbrBoss += randint(25, 60)*(1+3*(self.playerName=="Matteo"))
                        self.positionTre = 19
                    else:
                        self.spawnNbrBoss += 15*(1+3*(self.playerName=="Matteo"))
            
                if self.positionTre == 0:
                    self.trebuchet.update(0)
                    self.positionTre = -1
                elif self.positionTre > 0:
                    self.positionTre -= 1
            
            elif self.bossName == "Buchmann":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    if self.nbr < 75:
                        self.all_bossSpawnsEmerentia.add(Emerentia())
                        self.spawnNbrBoss += randint(30, 80)
                    else:
                        self.all_bossSpawnsKeyToPress.add(PressText())
            
            elif self.bossName == "Faggioni":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    self.bossRotated += 1

                    if self.nbr < 75:
                        self.all_bossSpawnsNotesMus.add(NotesMus(self.boss.rect.y))
                    else:
                        self.all_bossSpawnsNotesMus.add(CleMus())
                    self.spawnNbrBoss += randint(30, 80)

                    self.path1 = os.path.join(CUR_PATH, "boss", "Faggioni", "faggioni1.png")
                    self.path2 = os.path.join(CUR_PATH, "boss", "Faggioni", "faggioni2.png")
                    self.bossImagesFaggioni = [self.path1, self.path2]
                    self.boss.image = pg.image.load(self.bossImagesFaggioni[self.bossRotated%2])
                    self.boss.image = pg.transform.scale(self.boss.image, (120, 120))

            elif self.bossName == "Andenmatten":
                if self.counte == self.spawnNbrBoss and self.ventBack:
                    self.all_bossSpawnsChaussures.add(Chaussures())
                    self.spawnNbrBoss += randint(40, 100)
                if self.counte == self.spawnNbrBossV:
                    self.all_bossSpawnsVent.add(Vent(self.counte))
                    self.spawnNbrBossV += randint(100, 300)

            elif self.bossName == "Reymond":
                if self.counte == self.spawnNbrBoss:
                    self.all_bossSpawnsChimie1.add(Chimie1())
                    self.spawnNbrBoss += randint(40, 100)
                if self.counte == self.spawnNbrBossV:
                    self.all_bossSpawnsChimie2.add(Chimie2(self.boss.rect.y))
                    self.spawnNbrBossV += randint(60, 100)

                if self.bossRotated == 0:
                    self.path = os.path.join(CUR_PATH, "boss", "Reymond", "reymond.png")
                    self.boss.image = pg.image.load(self.path)
                    self.boss.image = pg.transform.scale(self.boss.image, (120,120))
                    self.bossRotated = -1
                elif self.bossRotated > 0:
                    self.bossRotated -= 1

            elif self.bossName == "Gratzl":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = random.randint(1, 3)
                    self.all_bossSpawnsSchorle.add(Schorle(self.quintasActive))
                    if self.quintasActive:
                        self.spawnNbrBoss += randint(50, 120)
                    else:
                        self.spawnNbrBoss += randint(20, 80)
                if self.quintasActive:
                    if self.counte == self.spawnNbrBossV:
                        self.all_bossSpawnsPlaques.add(PlaqueFemmes(self.boss2.rect.y))
                        self.boss2.rect.y -= 20
                        self.spawnNbrBossV += randint(60, 120)
                
            elif self.bossName == "Sahraoui":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    if self.nbr < 50:
                        self.all_bossSpawnsEnglishFile.add(EnglishFile())
                    else:
                        self.all_bossSpawnsImmigrationBook.add(ImmigrationBook(self.boss.rect.y))
                    self.spawnNbrBoss += randint(40, 80)
            
            elif self.bossName == "Moix":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    if self.nbr < 50:
                        self.all_bossSpawnsBaguette.add(Baguette(self.boss.rect.y))
                    else:
                        self.all_bossSpawnsInstument.add(Instument())
                    self.spawnNbrBoss += randint(40, 80)

            elif self.bossName == "Iglesias":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    if self.nbr < 40 or self.nbrCab != 0:
                        if self.nbrCab == 0:
                            self.all_bossSpawnsCable.add(Cable1())
                            self.cable = Cable1()
                            self.nbrCab += 1
                            self.spawnNbrBoss += int(80/-self.obstacleVelocity+self.velAdd/4)
                        elif self.nbrCab < self.cable1.lenght:
                            self.all_bossSpawnsCable.add(Cable2(self.cable.rect.y + self.cable.cableDel))
                            self.cable = Cable2(self.cable.rect.y + self.cable.cableDel)
                            self.nbrCab += 1
                            self.spawnNbrBoss += int(80/-self.obstacleVelocity+self.velAdd/4) - 1
                        else:
                            self.spawnNbrBoss += randint(50, 150)
                            self.nbrCab = 0
                    else:
                        self.all_bossSpawnsOrdi.add(Ordi())
                        self.spawnNbrBoss += randint(50, 100)

            elif self.bossName == "Donzé":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    if self.nbr < 50:
                        self.all_bossSpawnsVoiture.add(Voiture())
                    else:
                        self.all_bossSpawnsBrochure.add(Brochure())
                    self.spawnNbrBoss += randint(40, 80)

            elif self.bossName == "Tumble":
                if self.counte == self.spawnNbrBoss:
                    self.all_bossSpawnsTumble.add(Tumble())
                    self.spawnNbrBoss += randint(50, 100)
            
            elif self.bossName == "Gur":
                if self.counte == self.spawnNbrBoss:
                    self.all_bossSpawnsBallon.add(Ballon())
                    self.spawnNbrBoss += randint(50, 80)

            elif self.bossName == "Brochetta":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    if self.nbr < 70:
                        self.all_bossSpawnsChromosomes.add(Chromosomes())
                        self.boss.image = pg.transform.rotate(self.boss.image, 90)
                        self.bossRotated = 60
                        self.spawnNbrBoss += randint(50, 100)
                    else:
                        self.all_bossSpawnsBacteria.add(Bacteria())
                        self.boss.image = pg.transform.rotate(self.boss.image, 90)
                        self.bossRotated = 30
                        self.spawnNbrBoss += randint(50, 100)

                if self.bossRotated == 0:
                    self.boss.image = pg.transform.rotate(self.boss.image, -90)
                    self.bossRotated = -1
                elif self.bossRotated > 0:
                    self.bossRotated -= 1
            
            if self.bossName == "Burri":
                if self.counte == self.spawnNbrBoss:
                    self.nbr = randint(1,100)
                    if self.nbr < 80:
                        self.all_bossSpawnsFumer.add(Fumer(self.boss.rect.y))
                        self.boss.image = pg.transform.rotate(self.boss.image, 90)
                        self.bossRotated = 30
                        self.spawnNbrBoss += randint(60, 100)
                    else:
                        self.all_bossSpawnsAntigone.add(Antigone(self.playerName))
                        self.spawnNbrBoss += randint(50, 90)

                if self.bossRotated == 0:
                    self.boss.image = pg.transform.rotate(self.boss.image, -90)
                    self.bossRotated = -1
                elif self.bossRotated > 0:
                    self.bossRotated -= 1

            self.spawnNbr = self.counte + 19

        else:
            if self.counte == self.spawnNbr:
                self.nbr = randint(1,100)
                if self.nbr < 30:
                    self.all_bird.add(Bird())
                    self.spawnNbr += randint(40, 100)
                elif 30 <= self.nbr < 70:
                    self.all_holes.add(Hole())
                    self.spawnNbr += randint(40, 100)
                else :
                    self.all_obstacles.add(Obstacle())
                    self.spawnNbr += randint(40, 100)
            self.spawnNbrBoss = self.counte + 20
            self.spawnNbrBossV = self.spawnNbrBoss + random.randint(50, 200)

        if self.counte == self.spawnPlane:
            self.all_planes.add(Plane())
            self.spawnPlane += randint(300, 1000)

            
        self.platform.drawUnderGround(self.screenGame)
        self.all_holes.draw(self.screenGame)
        self.all_bird.draw(self.screenGame)
        self.all_obstacles.draw(self.screenGame)
        self.all_clouds.draw(self.screenGame)
        self.all_planes.draw(self.screenGame)
        self.all_platform_dec.draw(self.screenGame)
        self.MinusLife.draw(self.screenGame)
        self.all_extraLife.draw(self.screenGame)
        if self.bossName == "Bouchez":
            self.all_bossSpawnsChemise.draw(self.screenGame)
            self.all_bossSpawnsBanane.draw(self.screenGame)
        elif self.bossName == "Besson":
            self.all_bossSpawnsMissile.draw(self.screenGame)
        elif self.bossName == "Rochat":
            self.all_bossSpawnsKinder.draw(self.screenGame)
            self.all_bossSpawnsCoca.draw(self.screenGame)
        elif self.bossName == "Vuille":
            self.all_bossSpawnsTM.draw(self.screenGame)
        elif self.bossName == "Buchmann":
            self.all_bossSpawnsEmerentia.draw(self.screenGame)
            self.all_bossSpawnsKeyToPress.draw(self.screenGame)
        elif self.bossName == "Faggioni":
            self.all_bossSpawnsNotesMus.draw(self.screenGame)
        elif self.bossName == "Andenmatten":
            self.all_bossSpawnsChaussures.draw(self.screenGame)
            self.all_bossSpawnsVent.draw(self.screenGame)
        elif self.bossName == "Reymond":
            self.all_bossSpawnsChimie1.draw(self.screenGame)
            self.all_bossSpawnsChimie2.draw(self.screenGame)
            self.all_bossSpawnsExplosion.draw(self.screenGame)
        elif self.bossName == "Gratzl":
            self.all_bossSpawnsSchorle.draw(self.screenGame)
            self.all_bossSpawnsPlaques.draw(self.screenGame)
        elif self.bossName == "Sahraoui":
            self.all_bossSpawnsEnglishFile.draw(self.screenGame)
            self.all_bossSpawnsImmigrationBook.draw(self.screenGame)
        elif self.bossName == "Moix":
            self.all_bossSpawnsInstument.draw(self.screenGame)
            self.all_bossSpawnsBaguette.draw(self.screenGame)
        elif self.bossName == "Iglesias":
            self.all_bossSpawnsCable.draw(self.screenGame)
            self.all_bossSpawnsOrdi.draw(self.screenGame)
        elif self.bossName == "Donzé":
            self.all_bossSpawnsVoiture.draw(self.screenGame)
            self.all_bossSpawnsBrochure.draw(self.screenGame)
        elif self.bossName == "Tumble":
            self.all_bossSpawnsTumble.draw(self.screenGame)
        elif self.bossName == "Gur":
            self.all_bossSpawnsBallon.draw(self.screenGame)
        elif self.bossName == "Brochetta":
            self.all_bossSpawnsChromosomes.draw(self.screenGame)
            self.all_bossSpawnsBacteria.draw(self.screenGame)
        elif self.bossName == "Burri":
            self.all_bossSpawnsAntigone.draw(self.screenGame)
            self.all_bossSpawnsFumer.draw(self.screenGame)

        self.screenGame.blit(self.image, (0,100))

        # afficher le score et le record sur la fenêtre

        self.score_surface = self.calibri_font.render("SCORE: "+ str(self.score), True, (0,0,0))
        self.screenGame.blit(self.score_surface, (10, 140, 100, 180))

        self.score_surface = self.calibri_font.render("RECORD: "+ str(self.record), True, (0,0,0))
        self.screenGame.blit(self.score_surface, (10, 190, 100, 230))

        self.score_surface = self.calibri_font.render("VIES: "+ str(self.lifes), True, (0,0,0))
        self.screenGame.blit(self.score_surface, (10, 240, 100, 280))

        # mettre à jour l'écran
        pg.display.flip()


    def show_start_screen(self, start_or_restart, xrecord):
        if not self.mute:
            self.path = os.path.join(CUR_PATH, "music", "music.mp3")
            pg.mixer.init()
            pg.mixer.music.load(self.path)
            pg.mixer.music.play(-1)

        self.isTkclosed = False

        self.startScreen = Tk()
        self.startScreen.title("Jump!")
        self.startScreen.resizable(False, False)  # This code helps to disable windows from resizing

        window_height = 500
        window_width = 900

        screen_width = self.startScreen.winfo_screenwidth()
        screen_height = self.startScreen.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.startScreen.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        
        self.startScreen.config(bg=jaune1HEX)

        
        
        def on_closing():
            if messagebox.askokcancel("Quit", "Voulez-vous quitter?"):
                self.startScreen.destroy()
                self.isTkclosed = True
                g.running = False

        def startGame():
            self.getDifficultyChoice = self.difficultyList.get(ANCHOR)
            self.bossRush = False
            if self.getDifficultyChoice == "Facile":
                self.obstacleVelocity = -7
            elif self.getDifficultyChoice == "Moyen":
                self.obstacleVelocity = -10
            elif self.getDifficultyChoice == "Difficile":
                self.obstacleVelocity = -12
            elif self.getDifficultyChoice == "Hardcore":
                self.obstacleVelocity = -20
            elif self.getDifficultyChoice == "Boss Rush":
                self.obstacleVelocity = -10
                self.bossRush = True
 
            self.playerName = self.playerNameList.get(ANCHOR)
            if self.playerName == "":
                self.playerName = random.choice(self.player_list)
            
            
            self.bossName = self.bossList.get(ANCHOR)
            if self.bossName == "":
                self.bossName = "Profs"

            self.startScreen.destroy()

            return(self.obstacleVelocity, self.playerName, self.bossName, self.bossRush)


        self.titleFrame = Frame(self.startScreen, bg=jaune1HEX)
        self.titleFrame.pack()
        self.title = Label(self.titleFrame, text="Jump!", bg=jaune1HEX)
        self.title.config(font=("Consola", 60))
        self.title.pack()




        self.recoreFrame = Frame(self.startScreen, bg=jaune1HEX, pady=20)
        self.recoreFrame.pack()

        if start_or_restart == "Restart":
            self.scoreLabel = Label(self.recoreFrame, text = "Score : " + str(self.score), bg=jaune1HEX)
            self.scoreLabel.config(font=("Consola", 20))
            self.scoreLabel.pack()
        else:
            pass
        
        self.recoreLabel = Label(self.recoreFrame, text = "Best Score : " + str(xrecord), bg=jaune1HEX)
        self.recoreLabel.config(font=("Consola", 20))
        self.recoreLabel.pack()

        
        

        self.listFrame = Frame(self.startScreen, pady= 40, bg=jaune1HEX)
        self.listFrame.pack()


        self.difficultyListFrame = Frame(self.listFrame, padx = 1, bg=jaune1HEX)
        self.difficultyListFrame.pack(side=LEFT)
        self.difficultyListTitle = Label(self.difficultyListFrame, text = "Difficulté", bg=jaune1HEX)
        self.difficultyListTitle.pack(side= TOP)
        self.difficultyList = Listbox(self.difficultyListFrame, height= 6, bg=jaune2HEX, exportselection=0)
        self.difficultyList.pack()
        self.difficultyList.insert(END, "Facile")
        self.difficultyList.insert(END, "Moyen")
        self.difficultyList.insert(END, "Difficile")
        self.difficultyList.insert(END, "Hardcore")
        self.difficultyList.insert(END, "Boss Rush")

        self.playerNameListFrame = Frame(self.listFrame, padx = 1, bg=jaune1HEX)
        self.playerNameListFrame.pack(side=LEFT)
        self.playerNameListTitle = Label(self.playerNameListFrame, text = "Nom du joueur", bg=jaune1HEX)
        self.playerNameListTitle.pack(side = TOP)
        self.playerNameList = Listbox(self.playerNameListFrame, height= 6, bg=jaune2HEX, exportselection=0)
        self.playerNameList.pack()
        self.playerNameList.insert(END, "Adrien B")
        self.playerNameList.insert(END, "Tim")
        self.playerNameList.insert(END, "Mateus")
        self.playerNameList.insert(END, "Loïc")
        self.playerNameList.insert(END, "Jasper")
        self.playerNameList.insert(END, "Malorie")
        self.playerNameList.insert(END, "Karim")
        self.playerNameList.insert(END, "Oscar")
        self.playerNameList.insert(END, "Piotr")
        self.playerNameList.insert(END, "Adrien M")
        self.playerNameList.insert(END, "Diego")
        self.playerNameList.insert(END, "Simon")
        self.playerNameList.insert(END, "Eva")
        self.playerNameList.insert(END, "Frederike")
        self.playerNameList.insert(END, "Matteo")
        self.playerNameList.insert(END, "Shijie")
        self.playerNameList.insert(END, "Evan")

        self.bossFrame = Frame(self.listFrame, padx = 1, bg=jaune1HEX)
        self.bossFrame.pack(side=RIGHT)
        self.bossTitle = Label(self.bossFrame, text = "Présence du boss : ", bg=jaune1HEX)
        self.bossTitle.pack(side= TOP)
        self.bossList = Listbox(self.bossFrame, height= 6, bg=jaune2HEX, exportselection=0)
        self.bossList.pack()
        self.bossList.insert(END, "Besson")
        self.bossList.insert(END, "Bouchez")
        self.bossList.insert(END, "Rochat")
        self.bossList.insert(END, "Vuille")
        self.bossList.insert(END, "Buchmann")
        self.bossList.insert(END, "Faggioni")
        self.bossList.insert(END, "Andenmatten")
        self.bossList.insert(END, "Reymond")
        self.bossList.insert(END, "Gratzl")
        self.bossList.insert(END, "Sahraoui")
        self.bossList.insert(END, "Moix")
        self.bossList.insert(END, "Iglesias")
        self.bossList.insert(END, "Donzé")
        self.bossList.insert(END, "Gur")
        self.bossList.insert(END, "Brochetta")
        self.bossList.insert(END, "Burri")
        self.bossList.insert(END, "Profs")


        self.startButtonFrame = Frame(self.startScreen, pady=10, bg=jaune1HEX)
        self.startButtonFrame.pack()
        self.startButton = Button(self.startButtonFrame, text=start_or_restart, width= 15, height = 2, bg= jaune2HEX, command=startGame)
        self.startButton.config(font=("Consola", 20))
        self.startButton.pack()
        

        self.startScreen.protocol("WM_DELETE_WINDOW", on_closing)

        self.startScreen.mainloop()
        return(self.obstacleVelocity, self.playerName, self.bossName, self.bossRush)

        
g = Main()
try:
    show_start_screen_value = g.show_start_screen("Start", record)
    actualRecord = record
except:
    show_start_screen_value = g.show_start_screen("Start", 0)
    actualRecord = 0

obstacleVelocity = show_start_screen_value[0]
playerName = show_start_screen_value[1]
bossName = show_start_screen_value[2]

while g.running:
    actualRecord = g.new(actualRecord, playerName)
    show_start_screen_value = g.show_start_screen("Restart", actualRecord) 
    obstacleVelocity = show_start_screen_value[0]
    playerName = show_start_screen_value[1]
    bossName = show_start_screen_value[2]
    bossRush = show_start_screen_value[3]
    if obstacleVelocity > -5:
        obstacleVelocity = -7

    if g.isTkclosed:
        g.running = False
    else:
        g = Main()
        g.obstacleVelocity = obstacleVelocity
        g.playerName = playerName
        g.bossName = bossName
        g.record = actualRecord
        g.bossRush = bossRush

pg.quit()