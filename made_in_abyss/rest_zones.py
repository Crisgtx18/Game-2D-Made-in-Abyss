# ============================================================
# REST ZONES - Zonas de descanso
# ============================================================
import pygame
from config import TAM_TILE, CAPAS, VIDA_ZONA_DESCANSO, REDUCCION_MALDICION


class ZonaDescanso:
    def __init__(self, x, y, ancho=10):
        self.rect = pygame.Rect(x, y, ancho * TAM_TILE, TAM_TILE * 2)

    def toca(self, pr):
        return self.rect.colliderect(pr)

    def dibujar(self, pantalla, cam):
        pygame.draw.rect(pantalla, (100, 100, 120),
                        (self.rect.x - cam.x, self.rect.y - cam.y, self.rect.w, self.rect.h))
        pygame.draw.rect(pantalla, (150, 150, 200),
                        (self.rect.x - cam.x, self.rect.y - cam.y, self.rect.w, self.rect.h), 2)


class RestZoneManager:
    def __init__(self):
        self.zonas = []
        # Zonas en transiciones entre capas
        for i in range(len(CAPAS) - 1):
            y = CAPAS[i][1] * TAM_TILE
            for x in range(0, 800 * TAM_TILE, 200 * TAM_TILE):
                self.zonas.append(ZonaDescanso(x, y))
        # Zonas internas
        for capa in CAPAS:
            for y in range(capa[0], capa[1], 200):
                for x in range(0, 800 * TAM_TILE, 300 * TAM_TILE):
                    self.zonas.append(ZonaDescanso(x, y * TAM_TILE, 8))

    def actualizar(self, pr, player, curse):
        en_zona = False
        for z in self.zonas:
            if z.toca(pr):
                en_zona = True
                if player.vida < player.vida_max:
                    player.vida = min(player.vida_max, player.vida + VIDA_ZONA_DESCANSO * 0.016)
                curse.en_zona_segura()
        return en_zona

    def dibujar(self, pantalla, cam):
        for z in self.zonas: z.dibujar(pantalla, cam)
