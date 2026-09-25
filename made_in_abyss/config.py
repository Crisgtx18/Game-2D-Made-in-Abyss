# ============================================================
# MADE IN ABYSS - CONFIGURACION
# ============================================================

# --- DISPLAY ---
TAM_TILE = 16
ANCHO_MUNDO = 800
ALTO_MUNDO = 2200
ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
FPS = 60

# --- FISICA ---
GRAVEDAD = 0.5
VEL_MAX_CAIDA = 15
VELOCIDAD_JUGADOR = 3.0
FUERZA_SALTO = -9.0
ALCANCE_EDICION = 6

# --- CAPAS DEL ABISMO ---
# (inicio_tiles, fin_tiles, nombre, color_cielo)
CAPAS = [
    (0, 200, "Bosque de Oracion", (90, 150, 220)),
    (200, 450, "Trampa de los Bosques", (40, 80, 50)),
    (450, 700, "Puentes del Desecho", (80, 60, 50)),
    (700, 1000, "Grande de los Bosques", (20, 50, 30)),
    (1000, 1400, "Campo de las Bestias", (60, 20, 15)),
    (1400, 1800, "Ilustracion del Capricornio", (30, 30, 60)),
    (1800, 2200, "El Milagro", (10, 5, 15)),
]

NUM_CAPAS = len(CAPAS)

# --- ILUMINACION POR CAPA (0.0 = negro, 1.0 = dia completo) ---
LUZ_POR_CAPA = [1.0, 0.85, 0.7, 0.5, 0.3, 0.15, 0.05]

# --- MALDICION ---
# Daño por segundo al ascender, escala con severidad
DANO_BASE_MALDICION = 3.0
DANO_POR_INTENSIDAD = 2.0
# Umbral de ascenso para activar maldición por capa (en tiles)
UMBRAL_ASCENSO = 50

# --- IDs DE BLOQUES ---
AIRE = 0

# Capa 1 - Bosque de Oracion
TIERRA = 1
PIEDRA = 2
HIERBA = 3

# Capa 2 - Trampa de los Bosques
MADERA = 4
RAIZ = 5
MOHO = 6

# Capa 3 - Puentes del Desecho
METAL = 7
LADRILLO = 8
ESCORIA = 9

# Capa 4 - Grande de los Bosques
BARK = 10
HONGOS = 11
LUMINISCENTE = 12

# Capa 5 - Campo de las Bestias
CARNE = 13
HUESO = 14
VENA_ROJA = 15

# Capa 6 - Ilustracion del Capricornio
CRISTAL = 16
HIELO = 17
FUEGO = 18

# Capa 7 - El Milagro
ESMERALDA = 19
ANOMALIA = 20
VACIO = 21

# --- COLORES DE BLOQUES ---
COLORES = {
    TIERRA:      (110, 70, 40),
    PIEDRA:      (110, 110, 120),
    HIERBA:      (60, 160, 60),
    MADERA:      (140, 90, 50),
    RAIZ:        (90, 60, 30),
    MOHO:        (50, 100, 40),
    METAL:       (150, 150, 160),
    LADRILLO:    (160, 80, 60),
    ESCORIA:     (80, 60, 50),
    BARK:        (80, 50, 25),
    HONGOS:      (180, 160, 60),
    LUMINISCENTE:(100, 255, 150),
    CARNE:       (160, 50, 50),
    HUESO:       (200, 200, 180),
    VENA_ROJA:   (180, 30, 30),
    CRISTAL:     (100, 150, 255),
    HIELO:       (180, 220, 255),
    FUEGO:       (255, 120, 30),
    ESMERALDA:   (50, 220, 120),
    ANOMALIA:    (200, 50, 255),
    VACIO:       (30, 10, 40),
}

# --- BLOQUES SOLIDOS ---
SOLIDOS = set(COLORES.keys())

# --- BLOQUES POR CAPA (para generacion) ---
BLOQUES_POR_CAPA = [
    [TIERRA, PIEDRA, HIERBA],                  # Capa 1
    [MADERA, RAIZ, MOHO, PIEDRA],              # Capa 2
    [METAL, LADRILLO, ESCORIA, PIEDRA],        # Capa 3
    [BARK, HONGOS, LUMINISCENTE, PIEDRA],      # Capa 4
    [CARNE, HUESO, VENA_ROJA, PIEDRA],         # Capa 5
    [CRISTAL, HIELO, FUEGO, PIEDRA],           # Capa 6
    [ESMERALDA, ANOMALIA, VACIO, PIEDRA],      # Capa 7
]

# --- ARTEFACTOS ---
ARTEFACTOS = [
    {"id": 0, "nombre": "Semilla del Bosque",    "capa": 0, "color": (80, 180, 80),  "efecto": "cura_maldicion",   "valor": 0.1},
    {"id": 1, "nombre": "Raiz Ancestral",        "capa": 1, "color": (120, 80, 40),  "efecto": "vida",             "valor": 15},
    {"id": 2, "nombre": "Fragmento Metalico",    "capa": 2, "color": (180, 180, 190),"efecto": "resistencia",      "valor": 0.8},
    {"id": 3, "nombre": "Hongo Luminoso",        "capa": 3, "color": (200, 255, 100),"efecto": "linterna",          "valor": 50},
    {"id": 4, "nombre": "Hueso de Bestia",       "capa": 4, "color": (220, 220, 200),"efecto": "fuerza",           "valor": 2},
    {"id": 5, "nombre": "Cristal del Capricornio","capa": 5, "color": (120, 180, 255),"efecto": "cura_maldicion",   "valor": 0.3},
    {"id": 6, "nombre": "Fragmento del Milagro", "capa": 6, "color": (180, 80, 255), "efecto": "vida_max",         "valor": 25},
]

# --- CRIATURAS ---
# (nombre, color, ancho, alto, velocidad, agresiva, capa_min, capa_max)
CRIATURAS_CONFIG = [
    {"nombre": "Ardilla",       "color": (160, 120, 60),  "w": 8,  "h": 8,  "vel": 1.0, "agresiva": False, "capa": 0},
    {"nombre": "Araña",         "color": (40, 40, 40),    "w": 10, "h": 8,  "vel": 1.5, "agresiva": True,  "capa": 1},
    {"nombre": "Golem",         "color": (120, 110, 100), "w": 16, "h": 20, "vel": 0.5, "agresiva": True,  "capa": 2},
    {"nombre": "Orcedron",      "color": (80, 140, 60),   "w": 12, "h": 12, "vel": 2.0, "agresiva": True,  "capa": 3},
    {"nombre": "Bestia",        "color": (140, 30, 30),   "w": 18, "h": 14, "vel": 2.5, "agresiva": True,  "capa": 4},
    {"nombre": "Hacedor",       "color": (80, 60, 140),   "w": 14, "h": 18, "vel": 1.8, "agresiva": True,  "capa": 5},
    {"nombre": "Navegador",     "color": (200, 50, 255),  "w": 20, "h": 20, "vel": 1.2, "agresiva": True,  "capa": 6},
]

# --- ZONAS DE DESCANSO ---
DISTANCIA_ZONAS_DESCANSO = 200  # tiles entre zonas
VIDA_ZONA_DESCANSO = 20         # vida que restaura
REDUCCION_MALDICION = 0.15      # reduccion de maldicion por tick en zona segura
