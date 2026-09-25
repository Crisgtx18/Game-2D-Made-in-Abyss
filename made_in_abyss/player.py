# ============================================================
# PLAYER - Jugador con fisica
# ============================================================
import pygame
from config import TAM_TILE, GRAVEDAD, VEL_MAX_CAIDA, VELOCIDAD_JUGADOR, FUERZA_SALTO, CAPAS


class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 12, 24)
        self.vx = 0.0
        self.vy = 0.0
        self.en_suelo = False
        self.vida = 100.0
        self.vida_max = 100.0
        self.inv = False  # controles invertidos
        self._curse = None

    def actualizar(self, mundo, teclas, curse, dt):
        self._curse = curse
        inv = -1 if self.inv else 1

        self.vx = 0.0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]: self.vx = -VELOCIDAD_JUGADOR * inv
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]: self.vx = VELOCIDAD_JUGADOR * inv

        self.vy += GRAVEDAD
        if self.vy > VEL_MAX_CAIDA: self.vy = VEL_MAX_CAIDA

        if (teclas[pygame.K_SPACE] or teclas[pygame.K_w]) and self.en_suelo:
            self.vy = FUERZA_SALTO
            self.en_suelo = False

        self.rect.x += int(round(self.vx))
        self._colision(mundo, "x")
        self.rect.y += int(round(self.vy))
        self.en_suelo = False
        self._colision(mundo, "y")

        if curse.activa:
            self.vida -= curse.dano_seg * dt

        self.inv = curse.severidad() >= 4

    def _colision(self, mundo, eje):
        for ty in range(self.rect.top // TAM_TILE, self.rect.bottom // TAM_TILE + 1):
            for tx in range(self.rect.left // TAM_TILE, self.rect.right // TAM_TILE + 1):
                if not mundo.es_solido(tx, ty): continue
                tr = pygame.Rect(tx * TAM_TILE, ty * TAM_TILE, TAM_TILE, TAM_TILE)
                if not self.rect.colliderect(tr): continue
                if eje == "x":
                    self.rect.right = tr.left if self.vx > 0 else tr.right
                    self.vx = 0
                else:
                    if self.vy > 0:
                        self.rect.bottom = tr.top
                        self.en_suelo = True
                    else:
                        self.rect.top = tr.bottom
                    self.vy = 0

    def dibujar(self, pantalla, camara):
        color = (200, 50, 50) if self._curse and self._curse.activa and self._curse.severidad() >= 3 else (230, 200, 60)
        pygame.draw.rect(pantalla, color, (self.rect.x - camara.xf, self.rect.y - camara.yf, self.rect.w, self.rect.h))
        ox = 2 if self.vx < 0 else 8
        pygame.draw.rect(pantalla, (0, 0, 0), (self.rect.x - camara.xf + ox, self.rect.y - camara.yf + 6, 2, 2))

    def capa_actual(self):
        for i, (ini, fin, nombre, _) in enumerate(CAPAS):
            if ini <= self.rect.y // TAM_TILE < fin:
                return i, nombre
        return 0, CAPAS[0][2]
