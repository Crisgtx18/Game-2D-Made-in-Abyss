# ============================================================
# INVENTORY - Inventario y artefactos
# ============================================================
import pygame
from config import ARTEFACTOS


class Inventario:
    def __init__(self):
        self.slots = [None] * 9
        self.activo = 0
        self.linterna = False
        self.resistencia = 1.0

    def agregar(self, art_id):
        for i in range(9):
            if self.slots[i] is None:
                self.slots[i] = art_id
                e = ARTEFACTOS[art_id]["efecto"]
                v = ARTEFACTOS[art_id]["valor"]
                if e == "linterna": self.linterna = True
                elif e == "resistencia": self.resistencia = min(1.0, v)
                return True
        return False

    def usar(self, player, curse):
        aid = self.slots[self.activo]
        if aid is None: return False
        a = ARTEFACTOS[aid]
        if a["efecto"] == "cura_maldicion":
            curse.intensidad = max(0, curse.intensidad - a["valor"])
        elif a["efecto"] == "vida":
            player.vida = min(player.vida_max, player.vida + a["valor"])
        return True

    def dibujar(self, pantalla, sel):
        xo = pantalla.get_width() // 2 - 180
        y = pantalla.get_height() - 50
        font = pygame.font.SysFont("Consolas", 12)
        for i in range(9):
            x = xo + i * 40
            c = (100, 100, 100) if i == sel else (50, 50, 50)
            pygame.draw.rect(pantalla, c, (x, y, 36, 36))
            pygame.draw.rect(pantalla, (150, 150, 150), (x, y, 36, 36), 2)
            if self.slots[i] is not None:
                pygame.draw.rect(pantalla, ARTEFACTOS[self.slots[i]]["color"], (x + 4, y + 4, 28, 28))
            pantalla.blit(font.render(str(i + 1), True, (200, 200, 200)), (x + 2, y + 2))
