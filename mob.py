import pygame as pg
import random
import settings as set

# Classe des mobs (ennemis)
class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        set.init()
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((set.TILESIZE, set.TILESIZE))
        self.image.fill(set.ROUGE)
        self.game = game
        self.rect = self.image.get_rect()
        self.x = random.randrange(0, set.TILECOUNT)
        self.y = random.randrange(0, set.TILECOUNT)
        self.clockCompteur = set.CLOCK_MOB
        self.vie = set.VIE
        self.cooldown = 0

    def update(self):
        balles_coord, balles = self.liste_positions_balles()
        for i in range(len(balles_coord)):
            if (self.x, self.y) == balles_coord[i] and self.cooldown == 0:
                self.vie -= 1
                balles[i].kill()
        
        if self.vie == 0:
            self.kill()
        if self.vie == 1:
            self.image.fill(set.VIOLETFONCE)
        if self.vie == 2:
            self.image.fill(set.VIOLET)
        if self.cooldown > 0:
            self.image.fill(set.NOIR)
        
        if self.clockCompteur > 0:
            self.clockCompteur -= set.CLOCK_MOB
        else:
            self.clockCompteur = 10
            self.mouvement_aleatoire()
        self.rect.x = self.x * set.TILESIZE
        self.rect.y = self.y * set.TILESIZE

        if self.cooldown > 0:
            self.cooldown -= 1
            self.cooldown = set.FPS * 2

        
    def liste_positions_balles(self):
        positions = []
        balles = []
        for balle in self.game.balles:
            positions.append((balle.x, balle.y))
            balles.append(balle)
        return positions, balles


    def mouvement_aleatoire(self):
        while True:
            rnd = random.randrange(0, 4)
            dx = 0
            dy = 0
            if(rnd == 0):
                dy = -1
            if(rnd == 1):
                dy = 1
            if(rnd == 2):
                dx = -1
            if(rnd == 3):
                dx = 1

            if self.bouger(dx, dy):
                break

    def bouger(self, dx=0, dy=0):
        if not self.touche_un_mur(dx, dy):
            self.x += dx
            self.y += dy
            return True
        return False

    def touche_un_mur(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
