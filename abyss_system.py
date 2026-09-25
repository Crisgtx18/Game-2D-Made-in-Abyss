import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mecánica de Ascenso - Made in Abyss Style")
clock = pygame.time.Clock()

# --- CONSTANTES Y CONFIGURACIÓN ---
# En PyGame, 10 metros equivalen a N píxeles (ej. 1 metro = 20 píxeles -> 10m = 200px)
PIXELS_PER_METER = 20
LIMIT_METERS = 10.0
LIMIT_PIXELS = LIMIT_METERS * PIXELS_PER_METER

# Colors
COLOR_BG = (20, 20, 25)
COLOR_PLAYER = (50, 205, 50)
COLOR_SAFE_ZONE = (70, 70, 90)
COLOR_TEXT = (240, 240, 240)
COLOR_CURSE = (220, 20, 60)

# Player Properties
player_size = 30
player_x = WIDTH // 2 - player_size // 2
player_y = 500  # Empieza abajo
speed = 4

# --- VARIABLES DE LA MECÁNICA ---
# Como Y aumenta hacia abajo, la cota "más profunda" es el Y MÁXIMO alcanzado.
min_y_reached = player_y  # El punto más bajo (mayor Y) alcanzado
curse_active = False
curse_intensity = 0.0     # Cuántos metros se ha superado el límite (0 a N)
player_health = 100.0

# Generar plataformas de descanso
platforms = [
    pygame.Rect(100, 450, 600, 15),
    pygame.Rect(200, 300, 400, 15),
    pygame.Rect(100, 150, 600, 15)
]

font = pygame.font.SysFont("Consolas", 18)

# --- BUCLE PRINCIPAL ---
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time en segundos

    # 1. Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Input
    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= speed  # Subir (Y disminuye)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += speed  # Bajar (Y aumenta)

    # Actualizar posición
    player_x += dx
    player_y += dy

    # Límites de pantalla simples
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    # --- 3. LÓGICA DE LA MALDICIÓN ---
    
    # SI BAJAS (tu Y actual es mayor que el Y máximo registrado):
    if player_y > min_y_reached:
        min_y_reached = player_y
        curse_active = False
        curse_intensity = 0.0

    # SI SUBES (tu Y actual es menor que min_y_reached):
    ascent_distance_pixels = min_y_reached - player_y
    ascent_meters = ascent_distance_pixels / PIXELS_PER_METER

    if ascent_meters >= LIMIT_METERS:
        curse_active = True
        curse_intensity = ascent_meters - LIMIT_METERS
        
        # Daño continuo acumulativo según cuánto sobrepases el límite
        damage_per_second = 5.0 + (curse_intensity * 2.0)
        player_health -= damage_per_second * dt
        player_health = max(0, player_health)
    else:
        curse_active = False
        curse_intensity = 0.0

    # --- 4. RENDERIZADO ---
    screen.fill(COLOR_BG)

    # Dibujar plataformas
    for plat in platforms:
        pygame.draw.rect(screen, COLOR_SAFE_ZONE, plat)

    # Jugador (Rectángulo)
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    # Dibujar indicador de "Punto más profundo" (Línea fantasma)
    pygame.draw.line(screen, (100, 100, 100), (0, min_y_reached + player_size), (WIDTH, min_y_reached + player_size), 1)

    # Render del Jugador
    current_player_color = COLOR_CURSE if curse_active else COLOR_PLAYER
    pygame.draw.rect(screen, current_player_color, player_rect)

    # EFECTO VISUAL: Tremor / Agitación en pantalla si la maldición está activa
    camera_offset_x = 0
    camera_offset_y = 0
    if curse_active:
        shake = int(min(curse_intensity * 2, 8))
        camera_offset_x = random.randint(-shake, shake)
        camera_offset_y = random.randint(-shake, shake)

    # --- 5. INTERFAZ DE USUARIO (HUD) ---
    txt_health = font.render(f"Salud: {int(player_health)}%", True, COLOR_TEXT)
    txt_depth = font.render(f"Profundidad actual: {int(player_y / PIXELS_PER_METER)}m", True, COLOR_TEXT)
    txt_ascent = font.render(f"Ascenso acumulado: {ascent_meters:.1f}m / {LIMIT_METERS}m", True, COLOR_TEXT)
    
    status_color = COLOR_CURSE if curse_active else (50, 205, 50)
    txt_status = font.render(f"Maldición: {'¡ACTIVA!' if curse_active else 'Seguro'}", True, status_color)

    screen.blit(txt_health, (20 + camera_offset_x, 20 + camera_offset_y))
    screen.blit(txt_depth, (20 + camera_offset_x, 45 + camera_offset_y))
    screen.blit(txt_ascent, (20 + camera_offset_x, 70 + camera_offset_y))
    screen.blit(txt_status, (20 + camera_offset_x, 95 + camera_offset_y))

    pygame.display.flip()

pygame.quit()
sys.exit()