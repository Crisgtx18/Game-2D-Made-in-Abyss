# ============================================================
# UI - HUD e interfaz
# ============================================================
import pygame
from config import TAM_TILE, CAPAS, ARTEFACTOS


class UI:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.font = pygame.font.SysFont("Consolas", 18)
        self.fg = pygame.font.SysFont("Consolas", 24)

    def dibujar(self, pantalla, j, curse, cam, en_zona, inv):
        # Barra vida
        pygame.draw.rect(pantalla, (50, 50, 50), (20, 20, 200, 20))
        pct = j.vida / j.vida_max
        c = (50, 205, 50) if pct > 0.3 else (205, 50, 50)
        pygame.draw.rect(pantalla, c, (20, 20, int(200 * pct), 20))
        pygame.draw.rect(pantalla, (150, 150, 150), (20, 20, 200, 20), 2)
        pantalla.blit(self.font.render(f"HP: {int(j.vida)}/{int(j.vida_max)}", True, (255, 255, 255)), (25, 22))

        # Profundidad
        prof = j.rect.y // TAM_TILE
        ci, cn = j.capa_actual()
        pantalla.blit(self.font.render(f"Prof: {prof}m | Capa {ci+1}: {cn}", True, (200, 200, 200)), (self.w - 350, 20))

        # Maldicion
        if curse.activa:
            s = curse.severidad()
            nombres = ["Seguro", "Nauseas", "Dolor", "Hemorragia", "Sentidos", "Extremo", "MUERTE"]
            colores = [(50,205,50),(200,200,50),(200,150,50),(200,50,50),(150,50,150),(200,30,30),(255,0,0)]
            pantalla.blit(self.font.render(f"Maldicion: {nombres[s]}", True, colores[s]), (20, 50))
            pygame.draw.rect(pantalla, (50, 50, 50), (20, 75, 150, 10))
            pygame.draw.rect(pantalla, colores[s], (20, 75, int(150 * curse.intensidad / 5), 10))
        else:
            pantalla.blit(self.font.render("Maldicion: Seguro", True, (50, 205, 50)), (20, 50))

        # Capa
        pantalla.blit(self.font.render(f"Capa {ci+1}: {cn}", True, (200, 200, 200)), (self.w // 2 - 100, 10))

        if en_zona:
            pantalla.blit(self.font.render("ZONA SEGURA", True, (100, 255, 100)), (self.w // 2 - 70, 80))

        if j.inv:
            pantalla.blit(self.font.render("CONTROLES INVERTIDOS", True, (255, 50, 50)), (self.w // 2 - 120, 55))

        inv.dibujar(pantalla, inv.activo)

    def muerte(self, pantalla):
        o = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        o.fill((0, 0, 0, 150))
        pantalla.blit(o, (0, 0))
        pantalla.blit(self.fg.render("Has perecido en el Abismo", True, (200, 30, 30)),
                      (self.w // 2 - 200, self.h // 2 - 30))
        pantalla.blit(self.font.render("Presiona R para renacer", True, (200, 200, 200)),
                      (self.w // 2 - 120, self.h // 2 + 10))
