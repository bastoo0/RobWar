import sys
import pygame as pg
from pygame.key import set_repeat
from mob import Mob
import settings as set
from player import Player, Coeur

# Classe pour les murs (les trucs invisibles qui enpêchent de sortir de la zone de jeu)
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((set.TILESIZE, set.TILESIZE))
        self.image.fill(set.VERT)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x = x * set.TILESIZE
        self.rect.y = y * set.TILESIZE


# Classe principale du jeu (ne pas toucher sauf si on sait ce que ça fait)
class Game:
    def __init__(self):
        set.init()
        pg.init()
        self.screen = pg.display.set_mode((set.WIDTH, set.HEIGHT))
        pg.display.set_caption(set.TITLE)
        self.clock = pg.time.Clock()
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            """if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.bouger(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.bouger(dx=1)
                if event.key == pg.K_UP:
                    self.player.bouger(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.bouger(dy=1)
                if event.key == pg.K_j:
                    self.player.tirer(0)
                if event.key == pg.K_l:
                    self.player.tirer(1)
                if event.key == pg.K_i:
                    self.player.tirer(2)
                if event.key == pg.K_k:
                    self.player.tirer(3)"""

    def init_env(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.coeurs = pg.sprite.Group()
        self.balles = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.player = Player(self, 8, 8, False, True)
        self.player2 = Player(self, 4, 4, True, True)
        self.players.add(self.player)
        self.players.add(self.player2)
        self.cooldown = 0
        for i in range(set.VIE):
            coeur = Coeur(self, 15, 15 - i)
            self.all_sprites.add(coeur)
            self.coeurs.add(coeur)
        for i in range(set.MOB_COUNT):
            m = Mob(self)
            self.all_sprites.add(m)
            self.mobs.add(m)
        self.init_walls()

    def init_walls(self):
        for x in range(-1, set.TILECOUNT + 1):
            Wall(self, x, -1)
        for x in range(-1, set.TILECOUNT + 1):
            Wall(self, x, set.TILECOUNT)
        for x in range(-1, set.TILECOUNT + 1):
            Wall(self, -1, x)
        for x in range(-1, set.TILECOUNT + 1):
            Wall(self, set.TILECOUNT, x)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(set.FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        if len(self.mobs.sprites()) <= 0:
            self.quit()
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, set.WIDTH, set.TILESIZE):
            pg.draw.line(self.screen, set.GRISCLAIR, (x, 0), (x, set.HEIGHT))
        for y in range(0, set.HEIGHT, set.TILESIZE):
            pg.draw.line(self.screen, set.GRISCLAIR, (0, y), (set.WIDTH, y))

    def draw(self):
        self.screen.fill(set.BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

g = Game()
while True:
    g.init_env()
    g.run()