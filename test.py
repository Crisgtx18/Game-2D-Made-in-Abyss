# ============================================================
# TERRARIA-LIKE EN PYGAME - TODO EN UN ARCHIVO
# Controles:
#   A/D o Flechas  -> mover
#   ESPACIO/W      -> saltar
#   Click izq      -> romper bloque
#   Click der      -> colocar bloque
#   1-5            -> elegir bloque
#   Rueda mouse    -> cambiar bloque
#   ESC            -> salir
# ============================================================

# ------------------- IMPORTS -------------------
import pygame
import numpy as np
from opensimplex import OpenSimplex
import sys


# ------------------- CONFIG -------------------
TAM_TILE = 16

ANCHO_MUNDO = 800
ALTO_MUNDO  = 300

ANCHO_PANTALLA = 1280
ALTO_PANTALLA  = 720

FPS = 60
GRAVEDAD = 0.5
VEL_MAX_CAIDA = 15
ALCANCE_EDICION = 6   # en tiles


# ------------------- IDs DE BLOQUES -------------------
AIRE   = 0
TIERRA = 1
PIEDRA = 2
HIERBA = 3
ARENA  = 4
MADERA = 5

COLORES = {
    TIERRA: (110, 70, 40),
    PIEDRA: (110, 110, 120),
    HIERBA: (60, 160, 60),
    ARENA:  (220, 200, 120),
    MADERA: (140, 90, 50),
}

SOLIDOS = {TIERRA, PIEDRA, HIERBA, ARENA, MADERA}


# ------------------- CLASE MUNDO -------------------
class Mundo:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto  = alto
        self.bloques = np.zeros((alto, ancho), dtype=np.uint8)
        self.generar()

    # -------- GENERACIÓN --------
    def generar(self):
        gen = OpenSimplex(seed=12345)
        nivel_mar = self.alto // 3

        for x in range(self.ancho):
            # Ruido para la superficie
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
                    # Cuevas con ruido 2D
                    cueva = gen.noise2(x * 0.05, y * 0.05)
                    if cueva > 0.38:
                        self.bloques[y, x] = AIRE
                    else:
                        # Vetas de arena dentro de la piedra (decorativo)
                        veta = gen.noise2(x * 0.1 + 500, y * 0.1 + 500)
                        if veta > 0.55 and y > superficie + 20:
                            self.bloques[y, x] = ARENA
                        else:
                            self.bloques[y, x] = PIEDRA

    # -------- ACCESO --------
    def get(self, tx, ty):
        if 0 <= tx < self.ancho and 0 <= ty < self.alto:
            return self.bloques[ty, tx]
        return PIEDRA  # fuera del mundo = sólido

    def set(self, tx, ty, tipo):
        if 0 <= tx < self.ancho and 0 <= ty < self.alto:
            self.bloques[ty, tx] = tipo

    def es_solido(self, tx, ty):
        return self.get(tx, ty) in SOLIDOS

    def altura_superficie(self, tx):
        """Primer tile sólido hacia abajo en esa columna."""
        for ty in range(self.alto):
            if self.es_solido(tx, ty):
                return ty
        return self.alto - 1


# ------------------- CLASE CAMARA -------------------
class Camara:
    def __init__(self, ancho_mundo_px, alto_mundo_px):
        self.x = 0
        self.y = 0
        self.ancho_mundo = ancho_mundo_px
        self.alto_mundo  = alto_mundo_px

    def seguir(self, objetivo, pantalla):
        self.x = objetivo.rect.centerx - pantalla.get_width() // 2
        self.y = objetivo.rect.centery - pantalla.get_height() // 2
        # Clamp al mundo
        self.x = max(0, min(self.x, self.ancho_mundo - pantalla.get_width()))
        self.y = max(0, min(self.y, self.alto_mundo  - pantalla.get_height()))


# ------------------- CLASE JUGADOR -------------------
class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 12, 24)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.en_suelo = False
        self.color = (230, 200, 60)
        self.velocidad = 3.0
        self.fuerza_salto = -9.0

    def actualizar(self, mundo, teclas):
        # -------- INPUT --------
        self.vel_x = 0.0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.vel_x = -self.velocidad
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.vel_x = self.velocidad

        # -------- GRAVEDAD --------
        self.vel_y += GRAVEDAD
        if self.vel_y > VEL_MAX_CAIDA:
            self.vel_y = VEL_MAX_CAIDA

        # -------- SALTO --------
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_w]) and self.en_suelo:
            self.vel_y = self.fuerza_salto
            self.en_suelo = False

        # -------- MOVER X --------
        self.rect.x += int(round(self.vel_x))
        self._resolver_colision(mundo, eje="x")

        # -------- MOVER Y --------
        self.rect.y += int(round(self.vel_y))
        self.en_suelo = False
        self._resolver_colision(mundo, eje="y")

    def _resolver_colision(self, mundo, eje):
        x0 = self.rect.left   // TAM_TILE
        x1 = self.rect.right  // TAM_TILE
        y0 = self.rect.top    // TAM_TILE
        y1 = self.rect.bottom // TAM_TILE

        for ty in range(y0, y1 + 1):
            for tx in range(x0, x1 + 1):
                if not mundo.es_solido(tx, ty):
                    continue
                tile_rect = pygame.Rect(
                    tx * TAM_TILE, ty * TAM_TILE, TAM_TILE, TAM_TILE
                )
                if not self.rect.colliderect(tile_rect):
                    continue

                if eje == "x":
                    if self.vel_x > 0:
                        self.rect.right = tile_rect.left
                    elif self.vel_x < 0:
                        self.rect.left = tile_rect.right
                    self.vel_x = 0
                else:
                    if self.vel_y > 0:
                        self.rect.bottom = tile_rect.top
                        self.en_suelo = True
                    elif self.vel_y < 0:
                        self.rect.top = tile_rect.bottom
                    self.vel_y = 0

    def dibujar(self, pantalla, camara):
        pygame.draw.rect(
            pantalla,
            self.color,
            (self.rect.x - camara.x, self.rect.y - camara.y,
             self.rect.w, self.rect.h)
        )
        # "ojos" para saber hacia dónde mira
        ojos_y = self.rect.y - camara.y + 6
        if self.vel_x < 0:
            pygame.draw.rect(pantalla, (0,0,0), (self.rect.x - camara.x + 2, ojos_y, 2, 2))
        else:
            pygame.draw.rect(pantalla, (0,0,0), (self.rect.x - camara.x + 8, ojos_y, 2, 2))


# ------------------- SISTEMA DE CHUNKS (cache) -------------------
class CacheChunks:
    """
    Pre-renderiza bloques en superficies por chunk.
    Cuando editas un tile, marcas el chunk como 'sucio' y se re-renderiza.
    """
    TAM_CHUNK = 16  # tiles por lado

    def __init__(self, mundo):
        self.mundo = mundo
        self.cache = {}          # (cx, cy) -> Surface
        self.sucios = set()      # chunks a re-renderizar
        self.superficies_tile = self._pre_render_tiles()

    def _pre_render_tiles(self):
        sups = {}
        for tipo, color in COLORES.items():
            s = pygame.Surface((TAM_TILE, TAM_TILE))
            s.fill(color)
            # borde sutil para separar tiles
            pygame.draw.rect(s, (0, 0, 0), s.get_rect(), 1)
            sups[tipo] = s
        return sups

    def marcar_sucio(self, tx, ty):
        cx = tx // self.TAM_CHUNK
        cy = ty // self.TAM_CHUNK
        self.sucios.add((cx, cy))

    def _render_chunk(self, cx, cy):
        size_px = self.TAM_CHUNK * TAM_TILE
        surf = pygame.Surface((size_px, size_px), pygame.SRCALPHA)
        base_x = cx * self.TAM_CHUNK
        base_y = cy * self.TAM_CHUNK

        for ty in range(self.TAM_CHUNK):
            for tx in range(self.TAM_CHUNK):
                wt_x = base_x + tx
                wt_y = base_y + ty
                tipo = self.mundo.get(wt_x, wt_y)
                if tipo == AIRE:
                    continue
                surf.blit(
                    self.superficies_tile[tipo],
                    (tx * TAM_TILE, ty * TAM_TILE)
                )
        return surf

    def dibujar(self, pantalla, camara):
        # Qué chunks son visibles
        cx0 = camara.x // (self.TAM_CHUNK * TAM_TILE)
        cx1 = (camara.x + pantalla.get_width())  // (self.TAM_CHUNK * TAM_TILE) + 1
        cy0 = camara.y // (self.TAM_CHUNK * TAM_TILE)
        cy1 = (camara.y + pantalla.get_height()) // (self.TAM_CHUNK * TAM_TILE) + 1

        for cy in range(int(cy0), int(cy1) + 1):
            for cx in range(int(cx0), int(cx1) + 1):
                key = (cx, cy)

                # Actualizar si está sucio o no existe
                if key in self.sucios:
                    self.cache[key] = self._render_chunk(cx, cy)
                    self.sucios.discard(key)
                elif key not in self.cache:
                    self.cache[key] = self._render_chunk(cx, cy)

                surf = self.cache[key]
                pantalla.blit(
                    surf,
                    (cx * self.TAM_CHUNK * TAM_TILE - camara.x,
                     cy * self.TAM_CHUNK * TAM_TILE - camara.y)
                )


# ------------------- UTILIDADES -------------------
def mouse_a_tile(camara):
    mx, my = pygame.mouse.get_pos()
    tx = (mx + camara.x) // TAM_TILE
    ty = (my + camara.y) // TAM_TILE
    return int(tx), int(ty)


def en_alcance(jugador, tx, ty):
    jx = jugador.rect.centerx // TAM_TILE
    jy = jugador.rect.centery // TAM_TILE
    return abs(jx - tx) <= ALCANCE_EDICION and abs(jy - ty) <= ALCANCE_EDICION


# ------------------- MAIN -------------------
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Terraria-like")
    clock = pygame.time.Clock()

    # Mundo
    mundo = Mundo(ANCHO_MUNDO, ALTO_MUNDO)
    camara = Camara(ANCHO_MUNDO * TAM_TILE, ALTO_MUNDO * TAM_TILE)

    # Jugador en el spawn
    spawn_tx = ANCHO_MUNDO // 2
    spawn_ty = mundo.altura_superficie(spawn_tx) - 2
    jugador = Jugador(spawn_tx * TAM_TILE, spawn_ty * TAM_TILE)

    # Cache de chunks
    cache = CacheChunks(mundo)

    # Bloque actual para colocar
    bloque_actual = TIERRA

    # Arrancar el loop
    corriendo = True
    while corriendo:
        clock.tick(FPS)
        teclas = pygame.key.get_pressed()

        # -------- EVENTOS --------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False
                if pygame.K_1 <= evento.key <= pygame.K_5:
                    bloque_actual = evento.key - pygame.K_0

            if evento.type == pygame.MOUSEWHEEL:
                bloque_actual = (bloque_actual + evento.y) % 6
                if bloque_actual == AIRE:
                    bloque_actual = TIERRA

            if evento.type == pygame.MOUSEBUTTONDOWN:
                tx, ty = mouse_a_tile(camara)
                if en_alcance(jugador, tx, ty):
                    if evento.button == 1:  # romper
                        mundo.set(tx, ty, AIRE)
                        cache.marcar_sucio(tx, ty)
                    elif evento.button == 3:  # colocar
                        tile_rect = pygame.Rect(
                            tx * TAM_TILE, ty * TAM_TILE, TAM_TILE, TAM_TILE
                        )
                        # No colocar encima del jugador
                        if not jugador.rect.colliderect(tile_rect):
                            mundo.set(tx, ty, bloque_actual)
                            cache.marcar_sucio(tx, ty)

        # -------- UPDATE --------
        jugador.actualizar(mundo, teclas)
        camara.seguir(jugador, pantalla)

        # -------- DIBUJO --------
        pantalla.fill((90, 150, 220))  # cielo

        cache.dibujar(pantalla, camara)
        jugador.dibujar(pantalla, camara)

        # Resaltar tile bajo el mouse (si está en alcance)
        tx, ty = mouse_a_tile(camara)
        if en_alcance(jugador, tx, ty):
            pygame.draw.rect(
                pantalla, (255, 255, 255),
                (tx * TAM_TILE - camara.x, ty * TAM_TILE - camara.y,
                 TAM_TILE, TAM_TILE),
                1
            )

        # HUD: bloque seleccionado
        pygame.draw.rect(pantalla, COLORES[bloque_actual], (10, 10, 32, 32))
        pygame.draw.rect(pantalla, (255, 255, 255), (10, 10, 32, 32), 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# ------------------- PUNTO DE ENTRADA -------------------
if __name__ == "__main__":
    main()