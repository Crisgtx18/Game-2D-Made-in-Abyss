from pygame import *

class Player(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((32,32))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image.fill((255,0,0))
        self.speed = 1
    def update(self, screen):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
            
        screen.blit(self.image,self.rect)
        