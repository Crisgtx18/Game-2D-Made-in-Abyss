# ============================================================
# WORLD - Generacion procedural del Abismo
# ============================================================
import numpy as np
from opensimplex import OpenSimplex
from config import (
    TAM_TILE, ANCHO_MUNDO, ALTO_MUNDO,
    AIRE, CAPAS, BLOQUES_POR_CAPA, SOLIDOS, COLORES
)


def noise(gen, x, y):
    """Ruido scalar seguro."""
    return float(gen.noise2array(np.array([x]), np.array([y]))[0])


class Mundo:
    def __init__(self, ancho, alto, seed=12345):
        self.ancho = ancho
        self.alto = alto
        self.bloques = np.zeros((alto, ancho), dtype=np.uint8)
        self._generar(seed)

    def _generar(self, seed):
        gen = OpenSimplex(seed=seed)

        # Superficie pre-calculada
        xs = np.arange(self.ancho, dtype=np.float64)
        h = gen.noise2array(xs * 0.008, np.zeros(self.ancho)) * 25
        h += gen.noise2array(xs * 0.03, np.full(self.ancho, 100.0)) * 6
        sup = (50 + h).astype(int)

        for x in range(self.ancho):
            s = sup[x]
            for y in range(self.alto):
                capa = self._capa(y)

                if capa == 0:
                    if y < s:
                        self.bloques[y, x] = AIRE
                    elif y == s:
                        self.bloques[y, x] = 3
                    elif y < s + 5:
                        self.bloques[y, x] = 1
                    else:
                        c = noise(gen, x * 0.05, y * 0.05)
                        if c > 0.38:
                            self.bloques[y, x] = AIRE
                        elif noise(gen, x * 0.1 + 500, y * 0.1 + 500) > 0.55 and y > s + 20:
                            self.bloques[y, x] = 4
                        else:
                            self.bloques[y, x] = 2
                else:
                    bloques = BLOQUES_POR_CAPA[capa]
                    f = 0.03 + capa * 0.01
                    c = noise(gen, x * f, y * f + capa * 1000)
                    if c > 0.35 - capa * 0.02:
                        self.bloques[y, x] = AIRE
                    elif noise(gen, x * 0.08 + capa * 500, y * 0.08 + capa * 500) > 0.5:
                        self.bloques[y, x] = bloques[1]
                    elif len(bloques) > 2 and noise(gen, x * 0.12 + capa * 700, y * 0.12 + capa * 700) > 0.65:
                        self.bloques[y, x] = bloques[2]
                    else:
                        self.bloques[y, x] = bloques[0]

            # Estructuras
            if x % 25 == 0:
                sup_t = self.altura_superficie(x)
                if sup_t < 200:
                    for dy in range(10):
                        yy = sup_t - dy
                        if 0 <= yy < self.alto:
                            self.bloques[yy, x] = 4
            if x % 40 == 0:
                yy = CAPAS[3][0] + (x * 7) % (CAPAS[3][1] - CAPAS[3][0])
                if 0 <= yy < self.alto:
                    self.bloques[yy, x] = 11
            if x % 60 == 0:
                yy = CAPAS[5][0] + (x * 13) % (CAPAS[5][1] - CAPAS[5][0])
                if 0 <= yy < self.alto:
                    self.bloques[yy, x] = 16

    def _capa(self, y):
        for i, (ini, fin, _, _) in enumerate(CAPAS):
            if ini <= y < fin:
                return i
        return len(CAPAS) - 1

    def get(self, tx, ty):
        if 0 <= tx < self.ancho and 0 <= ty < self.alto:
            return self.bloques[ty, tx]
        return 2

    def set(self, tx, ty, tipo):
        if 0 <= tx < self.ancho and 0 <= ty < self.alto:
            self.bloques[ty, tx] = tipo

    def es_solido(self, tx, ty):
        return self.get(tx, ty) in SOLIDOS

    def altura_superficie(self, tx):
        for ty in range(self.alto):
            if self.es_solido(tx, ty):
                return ty
        return self.alto - 1
