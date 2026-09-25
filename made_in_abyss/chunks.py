# ============================================================
# CHUNKS - Cache de chunks pre-renderizados
# ============================================================
import pygame
from config import TAM_TILE, AIRE, COLORES


class CacheChunks:
    TAM_CHUNK = 16

    def __init__(self, mundo):
        self.mundo = mundo
        self.cache = {}
        self.sucios = set()
        self.superficies_tile = self._pre_render_tiles()

    def _pre_render_tiles(self):
        sups = {}
        for tipo, color in COLORES.items():
            s = pygame.Surface((TAM_TILE, TAM_TILE))
            s.fill(color)
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
        cx0 = camara.x // (self.TAM_CHUNK * TAM_TILE)
        cx1 = (camara.x + pantalla.get_width()) // (self.TAM_CHUNK * TAM_TILE) + 1
        cy0 = camara.y // (self.TAM_CHUNK * TAM_TILE)
        cy1 = (camara.y + pantalla.get_height()) // (self.TAM_CHUNK * TAM_TILE) + 1

        for cy in range(int(cy0), int(cy1) + 1):
            for cx in range(int(cx0), int(cx1) + 1):
                key = (cx, cy)
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
