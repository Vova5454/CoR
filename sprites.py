import pygame as pg
import random


class Player(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 600-self.rect.height/2-15)
        self.boost = 1
        self.speed = 6
        self.hp = 4
        self.useless = {"glue": float('inf'),
                        "trees": float('inf')}

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        keys = pg.key.get_pressed()
        w, a, s, d = False, False, False, False
        spcspeed = self.speed * self.boost
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.rect.y -= spcspeed
            w = True
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.rect.x -= spcspeed
            a = True
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.rect.y += spcspeed
            s = True
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.rect.x += spcspeed
            d = True
        if w and not (a or d):
            self.rect.y -= spcspeed * 2**0.5 - spcspeed
        if a and not (w or s):
            self.rect.x -= spcspeed * 2**0.5 - spcspeed
        if s and not (a or d):
            self.rect.y += spcspeed * 2**0.5 - spcspeed
        if d and not (s or w):
            self.rect.x += spcspeed * 2**0.5 - spcspeed
        if self.rect.right > 795:
            self.rect.right = 795
        if self.rect.bottom > 595:
            self.rect.bottom = 595
        if self.rect.left < 5:
            self.rect.left = 5
        if self.rect.top < 5:
            self.rect.top = 5

    def damage(self):
        self.hp -= 1
        if self.hp <= 0:
            return True
        return False
        

class Meteor(pg.sprite.Sprite):
    def __init__(self, image, mx, my):
        super().__init__()
        self.image = pg.image.load(image)
        self.speedx = random.choice([random.randint(mx, my), -random.randint(mx, my)])
        self.speedy = random.randint(mx, my)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, 600)
        self.rect.bottom = -200

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.top > 600:
            self.kill()

    def update(self):
        self.move()


class Buff(pg.sprite.Sprite):
    def __init__(self, buff_tuple):
        super().__init__()
        self.buff_tuple = buff_tuple
        self.image = pg.image.load(self.buff_tuple[1])
        self.type = self.buff_tuple[0]
        self.rect = self.image.get_rect()
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(5, 10)
        self.rect.centerx = random.randint(0, 800)
        self.rect.bottom = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0 or self.rect.top > 600 or self.rect.left > 800:
            self.kill()

    def update(self):
        self.move()

class Laser():
    def __init__(self):
        self.exists = False
        self.pos = (0, 0)
        self.speed = 46
        self.rect = pg.Rect(-1000, -1000, 0, 0)
        self.light = False


    def delete(self):
        self.exists = False
        self.rect = pg.Rect(-1000, -1000, 0, 0)

    def draw(self, screen):
        if not self.exists:
            return
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        if not self.exists:
            return
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.delete()

    def create(self, image: str, pos: tuple, lt=""):
        if self.exists:
            return
        self.exists = True
        if not self.light:
            self.image = pg.image.load(f"{image[:4]}{lt}{image[4:]}")
        else:
            self.image = pg.image.load(f"{image[:4]}b{image[4:]}")
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def lightning(self):
        if not self.light:
            self.speed *= 10
        self.light = True

    def unlightning(self):
        self.speed /= 10
        self.light = False
