# ============================================================
# CAMERA - Con screen shake
# ============================================================
import random


class Camara:
    def __init__(self, ancho_mundo_px, alto_mundo_px):
        self.x = 0
        self.y = 0
        self.mundo_w = ancho_mundo_px
        self.mundo_h = alto_mundo_px
        self.shake_x = 0
        self.shake_y = 0
        self.shake_t = 0

    def seguir(self, obj, pantalla):
        self.x = max(0, min(obj.rect.centerx - pantalla.get_width() // 2,
                           self.mundo_w - pantalla.get_width()))
        self.y = max(0, min(obj.rect.centery - pantalla.get_height() // 2,
                           self.mundo_h - pantalla.get_height()))

    def shake(self, intensidad, duracion):
        self.shake_t = duracion
        self.shake_x = random.randint(-intensidad, intensidad)
        self.shake_y = random.randint(-intensidad, intensidad)

    def actualizar(self):
        if self.shake_t > 0:
            self.shake_t -= 1
            s = int(self.shake_t * 0.5)
            self.shake_x = random.randint(-s, s)
            self.shake_y = random.randint(-s, s)
        else:
            self.shake_x = self.shake_y = 0

    @property
    def xf(self):
        return self.x + self.shake_x

    @property
    def yf(self):
        return self.y + self.shake_y
