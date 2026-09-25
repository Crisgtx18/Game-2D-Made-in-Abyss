# ============================================================
# LIGHTING - Oscuridad por capas
# ============================================================
import pygame
from config import CAPAS, LUZ_POR_CAPA, TAM_TILE


class Lighting:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.radio = 150

    def dibujar(self, pantalla, camara, player_y, linterna=False):
        capa = 0
        for i, (ini, fin, _, _) in enumerate(CAPAS):
            if ini <= player_y // TAM_TILE < fin:
                capa = i
                break

        luz = LUZ_POR_CAPA[capa]
        if luz >= 0.9: return

        radio = int(self.radio * 1.5) if linterna else self.radio
        cx, cy = self.w // 2, self.h // 2

        oscuro = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        for r in range(radio, 0, -3):
            alpha = int(255 * (1 - r / radio) * (1 - luz))
            pygame.draw.circle(oscuro, (0, 0, 0, max(0, min(255, alpha))), (cx, cy), r)

        capa_oscura = pygame.Surface((self.w, self.h))
        capa_oscura.fill((0, 0, 0))
        capa_oscura.set_alpha(min(255, int(255 * (1 - luz) * 0.3)))

        pantalla.blit(oscuro, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        pantalla.blit(capa_oscura, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
