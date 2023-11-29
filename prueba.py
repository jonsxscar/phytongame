import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
width, height = 800, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego del Dinosaurio")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

# Configuración del dinosaurio
dino_width, dino_height = 50, 50
dino_x, dino_y = 50, height - dino_height - 10
dino_velocity = 7

# Configuración del cactus
cactus_width, cactus_height = 20, 50
cactus_x, cactus_y = width, height - cactus_height - 10
cactus_velocity = 7

# Nuevos obstáculos
bird_width, bird_height = 40, 30
bird_velocity = 8

# Power-ups
power_up_width, power_up_height = 30, 30
power_up_x, power_up_y = -100, -100  # Inicialmente fuera de la pantalla
power_up_active = False

# Configuración de niveles
current_level = 1
max_levels = 3  # Puedes ajustar según lo deseado

# Puntuación
score = 0
font = pygame.font.Font(None, 36)

# Estado del juego
game_over = False

# Constantes
DINO_JUMP_HEIGHT = 100
DINO_START_Y = height - dino_height - 10
CLOCK_TICK_RATE = 30

# Inicializar coordenadas del pájaro fuera del bucle principal
bird_x, bird_y = width, height - bird_height - 10 - random.randint(50, 150)

# Crear un reloj fuera del bucle principal
clock = pygame.time.Clock()

# Función para mostrar la puntuación
def show_score():
    score_text = font.render("Puntuación: " + str(score), True, black)
    screen.blit(score_text, (10, 10))

# Función para mostrar el mensaje de "perdiste"
def show_game_over():
    game_over_text = font.render("¡Perdiste!", True, black)
    screen.blit(game_over_text, (width // 2 - 70, height // 2 - 20))

# Función para reiniciar el juego
def restart_game():
    global dino_y, cactus_x, bird_x, bird_y, score, game_over
    dino_y = height - dino_height - 10
    cactus_x = width
    bird_x, bird_y = width, height - bird_height - 10 - random.randint(50, 150)
    score = 0
    game_over = False

# Función para manejar eventos
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            restart_game()

# Función para manejar la lógica del salto del dinosaurio
def handle_dino_jump():
    global dino_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and dino_y == DINO_START_Y and not game_over:
        dino_y -= DINO_JUMP_HEIGHT
    elif dino_y < DINO_START_Y:
        dino_y += 4

# Función para manejar la lógica del movimiento del cactus
def move_cactus():
    global cactus_x, score
    if not game_over:
        cactus_x -= cactus_velocity
        if cactus_x < 0:
            cactus_x = width
            score += 1

# Función para manejar el movimiento del pájaro
def move_bird():
    global bird_x, bird_y, bird_velocity
    bird_x -= bird_velocity
    if bird_x < 0:
        bird_x = width
        bird_y = height - bird_height - 10 - random.randint(50, 150)

# Función para manejar la detección de colisiones
def check_collision():
    global game_over
    if (dino_x < cactus_x + cactus_width and
        dino_x + dino_width > cactus_x and
        dino_y < cactus_y + cactus_height and
        dino_y + dino_height > cactus_y) or \
       (dino_x < bird_x + bird_width and
        dino_x + dino_width > bird_x and
        dino_y < bird_y + bird_height and
        dino_y + dino_height > bird_y):
        game_over = True

# Función para generar un nuevo obstáculo
def generate_obstacle():
    obstacle_type = random.choice(["cactus", "bird"])
    if obstacle_type == "cactus":
        return pygame.Rect(width, height - cactus_height - 10, cactus_width, cactus_height)
    elif obstacle_type == "bird":
        min_distance = 200  # Distancia mínima entre el cactus y el pájaro

        # Asegurar que el pájaro esté al menos min_distance a la derecha del cactus
        cactus_x_pos = cactus_x if cactus_x > 0 else width
        bird_x = max(cactus_x_pos + min_distance, width)
        bird_y = height - bird_height - 10 - random.randint(50, 150)
        return pygame.Rect(bird_x, bird_y, bird_width, bird_height)


# Función para manejar los power-ups
def handle_power_up():
    global power_up_x, power_up_y, power_up_active
    if not power_up_active and random.randint(1, 500) == 1:  # Probabilidad de activación
        power_up_x = width
        power_up_y = height - power_up_height - 10 - random.randint(50, 150)
        power_up_active = True

# Bucle principal del juego
while True:
    handle_events()
    handle_dino_jump()
    move_cactus()
    move_bird() 
    check_collision()
    handle_power_up()

    # Generar nuevos obstáculos según el nivel
    if current_level == 1:
        obstacles = [generate_obstacle() for _ in range(1)]
    elif current_level == 2:
        obstacles = [generate_obstacle() for _ in range(2)]
    elif current_level == 3:
        obstacles = [generate_obstacle() for _ in range(3)]

    # Dibujar fondo
    screen.fill(white)

    # Dibujar el dinosaurio
    pygame.draw.rect(screen, green, (dino_x, dino_y, dino_width, dino_height))

    # Dibujar el cactus
    if not game_over:
        pygame.draw.rect(screen, black, (cactus_x, cactus_y, cactus_width, cactus_height))

    # Dibujar el pájaro
    if not game_over:
        pygame.draw.rect(screen, (255, 0, 0), (bird_x, bird_y, bird_width, bird_height))

    # Mostrar la puntuación
    show_score()

    # Si el juego ha terminado, mostrar mensaje y botón de reinicio
    if game_over:
        show_game_over()
        restart_button = pygame.Rect(width // 2 - 50, height // 2 + 20, 100, 40)
        pygame.draw.rect(screen, (200, 200, 200), restart_button)
        restart_text = font.render("Reiniciar", True, black)
        screen.blit(restart_text, (width // 2 - 35, height // 2 + 30))

    # Actualizar pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    clock.tick(CLOCK_TICK_RATE)
