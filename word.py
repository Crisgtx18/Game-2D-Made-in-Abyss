from pygame import *
import numpy as np
import random
from opensimplex import OpenSimplex
import sys

class Generation():
    def __init__(self, ancho = 1000, alto = 700, seed = random.randrange(0,100000)):
        self.alto = alto
        self.ancho = ancho
        self.bloques = np.zeros((alto, ancho), dtype=np.uint8)
        self.generar(seed)

    def generar(self, seed):
        gen = OpenSimplex(seed = seed)

        for x in range(self.ancho):
            #ruido de la superficie
            h = gen.noise2(x * 0.008, 0) * 25
            h += gen.noise2(x * 0.03, 100) * 6
            superficie = 100

            for y in range(self.alto):
                if y < superficie:
                    self.blooques[y, x] = 1
                
