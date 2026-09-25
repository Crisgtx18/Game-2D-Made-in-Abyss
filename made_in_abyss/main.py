# ============================================================
# MAIN - Made in Abyss
# ============================================================
import pygame
import sys
from config import TAM_TILE, ANCHO_MUNDO, ALTO_MUNDO, ANCHO_PANTALLA, ALTO_PANTALLA, FPS, AIRE, CAPAS
from world import Mundo
from chunks import CacheChunks
from player import Jugador
from camera import Camara
from curse_system import CurseSystem
from creatures import CreatureManager
from inventory import Inventario
from lighting import Lighting
from rest_zones import RestZoneManager
from ui import UI


def mouse_tile(cam):
    mx, my = pygame.mouse.get_pos()
    return int((mx + cam.xf) // TAM_TILE), int((my + cam.yf) // TAM_TILE)


def en_alcance(j, tx, ty):
    return abs(j.rect.centerx // TAM_TILE - tx) <= 6 and abs(j.rect.centery // TAM_TILE - ty) <= 6


def main():
    pygame.init()
    pan = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Made in Abyss")
    clock = pygame.time.Clock()

    mundo = Mundo(ANCHO_MUNDO, ALTO_MUNDO)
    cam = Camara(ANCHO_MUNDO * TAM_TILE, ALTO_MUNDO * TAM_TILE)
    spawn_tx = ANCHO_MUNDO // 2
    j = Jugador(spawn_tx * TAM_TILE, (mundo.altura_superficie(spawn_tx) - 2) * TAM_TILE)
    cache = CacheChunks(mundo)
    curse = CurseSystem()
    criaturas = CreatureManager()
    inv = Inventario()
    light = Lighting(ANCHO_PANTALLA, ALTO_PANTALLA)
    zones = RestZoneManager()
    ui = UI(ANCHO_PANTALLA, ALTO_PANTALLA)
    bloque = 1
    muerto = False

    while True:
        dt = clock.tick(FPS) / 1000.0
        teclas = pygame.key.get_pressed()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if ev.key == pygame.K_r and muerto:
                    j.rect.x = spawn_tx * TAM_TILE
                    j.rect.y = (mundo.altura_superficie(spawn_tx) - 2) * TAM_TILE
                    j.vida = j.vida_max
                    curse.reiniciar()
                    muerto = False
                if pygame.K_1 <= ev.key <= pygame.K_9:
                    inv.activo = ev.key - pygame.K_1
                if ev.key == pygame.K_e:
                    inv.usar(j, curse)
            if ev.type == pygame.MOUSEWHEEL:
                inv.activo = (inv.activo + ev.y) % 9
            if ev.type == pygame.MOUSEBUTTONDOWN and not muerto:
                tx, ty = mouse_tile(cam)
                if en_alcance(j, tx, ty):
                    if ev.button == 1:
                        t = mundo.get(tx, ty)
                        if t != AIRE: mundo.set(tx, ty, AIRE); cache.marcar_sucio(tx, ty)
                    elif ev.button == 3:
                        tr = pygame.Rect(tx * TAM_TILE, ty * TAM_TILE, TAM_TILE, TAM_TILE)
                        if not j.rect.colliderect(tr):
                            mundo.set(tx, ty, bloque); cache.marcar_sucio(tx, ty)

        if not muerto:
            j.actualizar(mundo, teclas, curse, dt)
            cam.seguir(j, pan)
            cam.actualizar()
            curse.actualizar(j.rect.y, dt)
            if curse.activa and curse.severidad() >= 2:
                cam.shake(int(curse.severidad() * 1.5), 5)
            criaturas.actualizar(j.rect, j.rect.y, mundo)
            if criaturas.colision(j.rect): j.vida -= 5 * dt
            en_zona = zones.actualizar(j.rect, j, curse)
            light.radio = 225 if inv.linterna else 150
            if j.vida <= 0: muerto = True

        # Color de fondo por capa
        ci = 0
        for i, (ini, fin, _, c) in enumerate(CAPAS):
            if ini <= j.rect.y // TAM_TILE < fin: ci = i; break
        pan.fill(CAPAS[ci][3])

        zones.dibujar(pan, cam)
        cache.dibujar(pan, cam)
        criaturas.dibujar(pan, cam)
        if not muerto: j.dibujar(pan, cam)
        light.dibujar(pan, cam, j.rect.y, inv.linterna)

        if not muerto:
            tx, ty = mouse_tile(cam)
            if en_alcance(j, tx, ty):
                pygame.draw.rect(pan, (255, 255, 255),
                               (tx * TAM_TILE - cam.xf, ty * TAM_TILE - cam.yf, TAM_TILE, TAM_TILE), 1)

        ui.dibujar(pan, j, curse, cam, en_zona, inv)
        if muerto: ui.muerte(pan)
        pygame.display.flip()


if __name__ == "__main__":
    main()
