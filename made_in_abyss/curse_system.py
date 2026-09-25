# ============================================================
# CURSE SYSTEM - Maldicion por ascenso
# ============================================================
from config import CAPAS, UMBRAL_ASCENSO, DANO_BASE_MALDICION, DANO_POR_INTENSIDAD


class CurseSystem:
    def __init__(self):
        self.prof_max = 0
        self.activa = False
        self.intensidad = 0.0
        self.dano_seg = 0.0

    def actualizar(self, player_y, dt):
        if player_y > self.prof_max:
            self.prof_max = player_y
            self.activa = False
            self.intensidad = 0.0

        ascenso = self.prof_max - player_y
        if ascenso > UMBRAL_ASCENSO:
            self.activa = True
            self.intensidad = min(5.0, ascenso / 100.0)
            self.dano_seg = DANO_BASE_MALDICION + self.intensidad * DANO_POR_INTENSIDAD
        else:
            self.activa = False
            self.intensidad = 0.0
            self.dano_seg = 0.0

        return self.dano_seg * dt

    def en_zona_segura(self):
        if self.activa:
            self.intensidad = max(0.0, self.intensidad - 0.01)
            if self.intensidad <= 0:
                self.activa = False

    def reiniciar(self):
        self.__init__()

    def severidad(self):
        if not self.activa:
            return 0
        if self.intensidad < 1: return 1
        if self.intensidad < 2: return 2
        if self.intensidad < 3: return 3
        if self.intensidad < 4: return 4
        if self.intensidad < 4.5: return 5
        return 6
