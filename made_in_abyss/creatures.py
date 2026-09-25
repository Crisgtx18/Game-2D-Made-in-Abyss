# ============================================================
# CREATURES - Criaturas por capa
# ============================================================
import pygame
import random
from config import CAPAS, CRIATURAS_CONFIG, TAM_TILE


class Criatura:
    def __init__(self, cfg, x, y):
        self.color = cfg["color"]
        self.rect = pygame.Rect(x, y, cfg["w"], cfg["h"])
        self.vel = cfg["vel"]
        self.agresiva = cfg["agresiva"]
        self.capa = cfg["capa"]
        self.dir = 1
        self.t = 0
        self.activa = False

    def actualizar(self, pr, py, mundo):
        capa_p = 0
        for i, (ini, fin, _, _) in enumerate(CAPAS):
            if ini <= py // TAM_TILE < fin:
                capa_p = i
                break
        self.activa = capa_p == self.capa
        if not self.activa: return

        dx = pr.centerx - self.rect.centerx
        dy = pr.centery - self.rect.centery
        dist = (dx**2 + dy**2)**0.5

        if self.agresiva and dist < 150:
            if abs(dx) > abs(dy):
                self.rect.x += self.vel * (1 if dx > 0 else -1)
            else:
                self.rect.y += self.vel * (1 if dy > 0 else -1)
        elif not self.agresiva and abs(dx) < 100:
            self.rect.x -= self.vel * (1 if dx > 0 else -1)
        else:
            self.t += 1
            if self.t > 60:
                self.dir *= -1
                self.t = 0
            self.rect.x += self.vel * 0.5 * self.dir

        if not mundo.es_solido(self.rect.centerx // TAM_TILE, self.rect.bottom // TAM_TILE + 1):
            self.rect.y += 2

    def dibujar(self, pantalla, camara):
        if not self.activa: return
        pygame.draw.rect(pantalla, self.color,
                        (self.rect.x - camara.x, self.rect.y - camara.y, self.rect.w, self.rect.h))


class CreatureManager:
    def __init__(self):
        self.criaturas = []
        for cfg in CRIATURAS_CONFIG:
            capa = CAPAS[cfg["capa"]]
            for _ in range(5 + cfg["capa"] * 2):
                x = random.randint(0, 799 * TAM_TILE)
                y = random.randint(capa[0] * TAM_TILE, (capa[1] - 1) * TAM_TILE)
                self.criaturas.append(Criatura(cfg, x, y))

    def actualizar(self, pr, py, mundo):
        for c in self.criaturas: c.actualizar(pr, py, mundo)

    def dibujar(self, pantalla, camara):
        for c in self.criaturas: c.dibujar(pantalla, camara)

    def colision(self, pr):
        for c in self.criaturas:
            if c.activa and pr.colliderect(c.rect): return c
        return None
