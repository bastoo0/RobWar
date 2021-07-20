import pygame as pg
import settings as set
import random

class Player(pg.sprite.Sprite):
    # Création du joueur
    def __init__(self, game, x, y, est_ennemi, a_un_ennemi):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((set.TILESIZE, set.TILESIZE))
        self.image.fill(set.BLANC)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vie = set.VIE
        self.viePrecedente = 3
        self.cooldown = set.FPS * 2
        self.positions_ennemis = []
        self.est_ennemi = est_ennemi
        self.a_un_ennemi = a_un_ennemi

    # Fonction pour bouger, dy = nombre de cases en colonne, dx = nombre de cases en ligne
    def bouger(self, dx=0, dy=0):
        if not self.touche_un_mur(dx, dy):
            self.x += dx
            self.y += dy
            return True
        return False
    
    # Fonctions de déplacement d'une case
    def haut(self):
        self.bouger(dy=1)
    
    def bas(self):
        self.bouger(dy=-1)
    
    def droite(self):
        self.bouger(dx=1)
    
    def gauche(self):
        self.bouger(dx=-1)

    # Pour rester sur le terrain
    def touche_un_mur(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    # Pour localiser les ennemis présents sur les lignes / colonnes
    def ennemi_a_gauche_ligne(self):
        positions = self.positions_ennemis
        for pos in positions:
            if pos[1] == self.y and pos[0] < self.x:
                return True
        return False

    def ennemi_a_droite_ligne(self):
        positions = self.positions_ennemis
        for pos in positions:
            if pos[1] == self.y and pos[0] > self.x:
                return True
        return False

    def ennemi_en_haut_colonne(self):
        positions = self.positions_ennemis
        for pos in positions:
            if pos[0] == self.x and pos[1] < self.y:
                return True
        return False

    def ennemi_en_bas_colonne(self):
        positions = self.positions_ennemis
        for pos in positions:
            if pos[0] == self.x and pos[1] > self.y:
                return True
        return False

    # Pour savoir si un ennemi se situe à sa droite, a sa gauche, en haut, ou en bas
    def ennemi_quelque_part_a_gauche(self):
        positions = self.positions_ennemis
        for pos in positions:
            if pos[0] < self.x: return True 
            else: return False
    
    def ennemi_quelque_part_a_droite(self):
        positions = self.positions_ennemis
        for pos in positions:
            if pos[0] > self.x: return True 
            else: return False
    
    def ennemi_quelque_part_en_haut(self):
        positions = self.positions_ennemis
        for pos in positions:
            if pos[1] < self.y: return True 
            else: return False

    def ennemi_quelque_part_en_bas(self):
        positions = self.positions_ennemis
        for pos in positions:
            if pos[1] > self.y: return True 
            else: return False

    # Pour savoir si un ennemi est dans les environs (par exemple si x = 2, on vérifie si
    # un ennemi est dans les 2 cases qui entourent le joueur)
    def ennemi_a_moins_de_x_cases(self, x):
        positions = self.positions_ennemis
        for pos in positions:
            if abs(self.x - pos[0]) >= x or abs(self.y - pos[1]) >= x : 
                return True 
            else : 
                return False

    # Retourne une liste de tuples avec les coordonnées (x, y) des ennemis
    def liste_positions_ennemis(self):
        positions = []
        for mob in self.game.mobs:
            positions.append((mob.x, mob.y))
        if self.a_un_ennemi:
            positions.append((self.ennemi.x, self.ennemi.y))
        return positions

    # Tire dans la direction demandée
    def tirer(self, direction):
        x = self.x
        y = self.y
        if direction == set.GAUCHE: x = x - 1
        if direction == set.DROITE: x = x + 1
        if direction == set.HAUT: y = y - 1
        if direction == set.HAUT: y = y + 1
        if self.est_ennemi: id = 0
        else : id = 1
        balle = Balle(self.game, x, y, direction, id)
        self.game.all_sprites.add(balle)
        self.game.balles.add(balle)

    def liste_positions_balles(self):
        positions = []
        balles = []
        for balle in self.game.balles:
            if self.est_ennemi:
                if balle.id == 1:
                    positions.append((balle.x, balle.y))
                    balles.append(balle)
            else:
                if balle.id == 0: 
                    positions.append((balle.x, balle.y))
                    balles.append(balle)
        return positions, balles

    # Fonction qui met à jour l'objet, est appelée à chaque image par seconde (donc ici 10 fois par seconde)
    def update(self):
        balles_coord, balles = self.liste_positions_balles()
        for i in range(len(balles_coord)):
            if (self.x, self.y) == balles_coord[i] and self.cooldown == 0:
                self.vie -= 1
                balles[i].kill()

        if self.a_un_ennemi :
            if self.est_ennemi :
                self.ennemi = self.game.players.sprites()[0]
            else: 
                self.ennemi = self.game.players.sprites()[1]
        self.positions_ennemis = self.liste_positions_ennemis()
        self.update_auto()
        self.rect.x = self.x * set.TILESIZE
        self.rect.y = self.y * set.TILESIZE
        mobs_coord = self.positions_ennemis
        if self.cooldown > 0:
            self.cooldown -= 1
        if (self.x, self.y) in mobs_coord and self.cooldown == 0:
            self.vie -= 1
            self.cooldown = set.FPS * 2
        
        if self.viePrecedente != self.vie:
            if self.vie == 2:
                self.game.coeurs.sprites()[2].desactiver()
            if self.vie == 1:
                self.game.coeurs.sprites()[1].desactiver()
            if self.vie == 0:
                if self.est_ennemi :
                    print("Ennemi a perdu")
                else: print("Joueur a perdu")
                self.game.quit()
            
            if self.est_ennemi :
                print("Vie ennemi: " + str(self.vie))
            else:                     
                print("Vie joueur: " + str(self.vie))

        self.viePrecedente = self.vie

    # Intelligence artificielle du joueur
    def update_auto(self):
        rand = random.randrange(0, 4)
        if rand == 0:
            self.droite()
        if rand == 1:
            self.gauche()
        if rand == 2:
            self.haut()
        if rand == 3:
            self.bas()

        if self.ennemi_a_gauche_ligne():
            self.tirer(set.GAUCHE)
        if self.ennemi_a_droite_ligne():
            self.tirer(set.DROITE)
        if self.ennemi_en_haut_colonne():
            self.tirer(set.HAUT)
        if self.ennemi_en_bas_colonne():
            self.tirer(set.BAS)

# Classe de la balle
class Balle(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction, id):
        pg.sprite.Sprite.__init__(self)
        self.x = x 
        self.y = y
        self.game = game
        self.image = pg.Surface((set.TILESIZE, set.TILESIZE), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.direction = direction
        self.duree = set.DUREE_BALLE
        self.id = id

    def update(self):
        if self.duree <= 0:
            self.kill()
        if self.direction == 0:
            self.x -= 1
        if self.direction == 1:
            self.x += 1
        if self.direction == 2:
            self.y -= 1
        if self.direction == 3:
            self.y += 1
        
        self.rect.x = self.x * set.TILESIZE
        self.rect.y = self.y * set.TILESIZE
        self.circle = pg.draw.circle(self.image, set.BLANC, (set.TILESIZE / 2, set.TILESIZE / 2), 10)
        self.duree -= 1

class Coeur(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = x 
        self.y = y
        self.game = game
        self.actif = True
        self.image = pg.Surface((set.TILESIZE, set.TILESIZE), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * set.TILESIZE
        self.rect.y = self.y * set.TILESIZE

    def update(self):
        if self.actif:
            color = set.ROUGE
        else:
            color = set.NOIR
        
        self.circle = pg.draw.circle(self.image, color, (set.TILESIZE / 2, set.TILESIZE / 2), 10)

    def desactiver(self):
        self.actif = False