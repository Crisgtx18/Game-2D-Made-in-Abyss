import pygame
import numpy as np
from opensimplex import OpenSimplex

# ══════════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════════
AIRE   = 0
HIERBA = 1
TIERRA = 2
PIEDRA = 3
ARENA  = 4
COBRE  = 5
HIERRO = 6
ORO    = 7

# Colores (R, G, B)
COLORES = {
    AIRE:   (135, 206, 250),
    HIERBA: (34, 180, 34),
    TIERRA: (139, 90, 43),
    PIEDRA: (128, 128, 128),
    ARENA:  (210, 190, 130),
    COBRE:  (180, 110, 60),
    HIERRO: (180, 140, 100),
    ORO:    (255, 215, 0),
}

# Configuración
ANCHO = 800
ALTO  = 600
TAM_BLOQUE = 4
SEED = 12345


# ══════════════════════════════════════════════════════════
# CLASE MUNDO
# ══════════════════════════════════════════════════════════
class Mundo:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto  = alto
        self.bloques = np.zeros((alto, ancho), dtype=np.uint8)
        self.generar()

    def generar(self):
        gen = OpenSimplex(seed=12345)
        nivel_mar = self.alto // 3

        for x in range(self.ancho):
            h  = gen.noise2(x * 0.008, 0) * 25
            h += gen.noise2(x * 0.03, 100) * 6
            superficie = int(nivel_mar + h)

            for y in range(self.alto):
                if y < superficie:
                    self.bloques[y, x] = AIRE
                elif y == superficie:
                    self.bloques[y, x] = HIERBA
                elif y < superficie + 5:
                    self.bloques[y, x] = TIERRA
                else:
                    cueva = gen.noise2(x * 0.05, y * 0.05)
                    if cueva > 0.38:
                        self.bloques[y, x] = AIRE
                    else:
                        veta = gen.noise2(x * 0.1 + 500, y * 0.1 + 500)
                        if veta > 0.65 and y > superficie + 30:
                            self.bloques[y, x] = ORO
                        elif veta > 0.55 and y > superficie + 20:
                            self.bloques[y, x] = HIERRO
                        elif veta > 0.45 and y > superficie + 10:
                            self.bloques[y, x] = COBRE
                        elif gen.noise2(x * 0.08 + 300, y * 0.08 + 300) > 0.5:
                            self.bloques[y, x] = ARENA
                        else:
                            self.bloques[y, x] = PIEDRA


# ══════════════════════════════════════════════════════════
# RENDERIZADO
# ══════════════════════════════════════════════════════════
def dibujar_mundo(surface, mundo):
    pixeles = np.zeros((mundo.alto, mundo.ancho, 3), dtype=np.uint8)

    for bloque_id, color in COLORES.items():
        mascara = mundo.bloques == bloque_id
        pixeles[mascara] = color

    superficie = pygame.surfarray.make_surface(pixeles.swapaxes(0, 1))
    surface.blit(superficie, (0, 0))


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Terraria Style")
    clock = pygame.time.Clock()

    mundo = Mundo(ANCHO, ALTO)
    dibujar_mundo(screen, mundo)

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_r:
                    mundo = Mundo(ANCHO, ALTO)
                    dibujar_mundo(screen, mundo)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()