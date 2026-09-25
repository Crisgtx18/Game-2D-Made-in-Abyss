import pygame as py
from pygame import *
from word import *
from player import *


screen = py.display.set_mode((400,400))
clock = time.Clock()

player = Player(100,100)
while True:
    clock.tick(60)
    screen.fill((255,255,0))
    for event in py.event.get():
        if event.type == QUIT:
            quit()
    player.update(screen)
    display.update()
