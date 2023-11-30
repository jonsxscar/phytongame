import pygame
import sys
import random
import pygame.gfxdraw

# Inicializar pygame
pygame.init()

# Definir colores
white = (255, 255, 255)
black = (0, 0, 0)

# Configuración de la pantalla
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("T-Rex Dino Run")

dino_jump = False
jump_count = 10

#score
score = 0
font = pygame.font.Font(None, 36)

# Estado del juego
game_over = False
start_screen = True  # Nuevo estado para la pantalla de inicio

# Cargar imágenes
dino_img = pygame.image.load("dino.png")
dino_img = pygame.transform.scale(dino_img, (50, 50))
cactus_img = pygame.image.load("kivy_venv\cactus.png")
cactus_img = pygame.transform.scale(cactus_img, (50, 50))
bird_img = pygame.image.load("kivy_venv\pajabird.png")
bird_img = pygame.transform.scale(bird_img, (50, 50))

# Cargar imágenes de fondo
game_bg_img = pygame.image.load("city.jpg")  # Ajusta la ruta según tu caso
game_bg_img = pygame.transform.scale(game_bg_img, (screen_width, screen_height))

start_screen_bg_img = pygame.image.load("fondo.jpg")  # Ajusta la ruta según tu caso
start_screen_bg_img = pygame.transform.scale(start_screen_bg_img, (screen_width, screen_height))

restart_bg_img = pygame.image.load("city.jpg")  # Ajusta la ruta según tu caso
restart_bg_img = pygame.transform.scale(restart_bg_img, (screen_width, screen_height))

# Inicializar variables de posición
dino_x = 40
dino_y = screen_height - dino_img.get_height() - 30 #altura del piso
cactus_x = screen_width
cactus_y = screen_height - cactus_img.get_height() - 30 #altura del piso
bird_x = screen_width
bird_y = random.randint(200, 300)

# Función para mostrar la puntuación
def show_score():
    score_text = font.render("Puntuación: " + str(score), True, black)
    screen.blit(score_text, (10, 10))

#prueba
def show_start_screen():
    start_text = font.render("¡T-Rex Dino Run!", True, black)
    screen.blit(start_text, (screen_width // 2 - 100, screen_height // 2 - 50))

    start_button = pygame.Rect(screen_width // 2 - 60, screen_height // 2 + 20, 120, 40)
    pygame.draw.rect(screen, (200, 200, 200), start_button)
    start_text = font.render("Start", True, black)
    screen.blit(start_text, (screen_width // 2 - 30, screen_height // 2 + 30))

# Función para manejar eventos del ratón #prueba tambien
def handle_mouse_events():
    global start_screen, game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if start_screen:
                start_button = pygame.Rect(screen_width // 2 - 60, screen_height // 2 + 20, 120, 40)
                if start_button.collidepoint(mouse_x, mouse_y):
                    start_screen = False
                    game_over = False
                    start_game()
            elif game_over:
                restart_button = pygame.Rect(screen_width // 2 - 60, screen_height // 2 + 20, 120, 40)
                if restart_button.collidepoint(mouse_x, mouse_y):
                    game_over = False
                    start_game()

# Función para mostrar el mensaje de "perdiste"
def show_game_over():
    game_over_text = font.render("¡Perdiste!", True, black)
    screen.blit(game_over_text, (screen_width // 2 - 50, screen_height // 2 - 20))

def start_game():
    global dino_x, dino_y, cactus_x, cactus_y, bird_x, bird_y, score, game_over, current_obstacle
    dino_x = 40
    dino_y = screen_height - dino_img.get_height() - 30 #altura del piso
    cactus_x = screen_width
    cactus_y = screen_height - cactus_img.get_height() - 30 #altura del piso
    bird_x = screen_width
    bird_y = random.randint(200, 300)
    score = 0
    game_over = False
    current_obstacle = "cactus"

def restart_game():
    global dino_x, dino_y, cactus_x, cactus_y, bird_x, bird_y, score, game_over
    dino_x = 40
    dino_y = screen_height - dino_img.get_height() - 30 #altura del piso
    cactus_x = screen_width
    cactus_y = screen_height - cactus_img.get_height() - 30 #altura del piso
    bird_x = screen_width
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

# Función para manejar la lógica del movimiento del cactus
def move_cactus():
    global cactus_x, score, current_obstacle
    if not game_over:
        cactus_x -= 5
        if cactus_x < 0:
            cactus_x = screen_width
            current_obstacle = random.choice(["cactus", "bird"])
            score += 10

# Función para manejar el movimiento del pájaro
def move_bird():
    global bird_x, bird_y, current_obstacle, bird_y
    if not game_over:
        bird_x -= 5
        if bird_x < 0:
            bird_x = screen_width
            current_obstacle = random.choice(["cactus", "bird"])
            bird_y = random.randint(200, 300) #prueba
        #scored = False
        print(bird_y) 

# Función para manejar la detección de colisiones
def check_collision():
    global game_over
    if current_obstacle == "cactus":
        if (
            dino_x < cactus_x + cactus_img.get_width()
            and dino_x + dino_img.get_width() > cactus_x
            and dino_y < cactus_y + cactus_img.get_height()
            and dino_y + dino_img.get_height() > cactus_y
        ):
            game_over = True

    elif current_obstacle == "bird":
        if (
            dino_x < bird_x + bird_img.get_width()
            and dino_x + dino_img.get_width() > bird_x
            and dino_y < bird_y + bird_img.get_height()
            and dino_y + dino_img.get_height() > bird_y
        ):
            game_over = True

# Función para aplicar desenfoque a una superficie
def apply_blur(surface, factor):
    scaled_surface = pygame.transform.smoothscale(surface, (int(surface.get_width() / factor), int(surface.get_height() / factor)))
    return pygame.transform.smoothscale(scaled_surface, (surface.get_width(), surface.get_height()))


# Bucle principal del juego
clock = pygame.time.Clock()
game_running = True

while True:
    handle_mouse_events()
    
    if start_screen:
        screen.blit(start_screen_bg_img, (0, 0))
        show_start_screen()
        pygame.display.flip()
        continue  # Salta el resto del bucle y vuelve al principio si estamos en la pantalla de inicio

    move_cactus()
    move_bird() 
    check_collision()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not dino_jump:
        dino_jump = True

    if dino_jump:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            dino_y -= (jump_count ** 2) * 0.3 * neg
            jump_count -= 0.5
        else:
            dino_jump = False
            jump_count = 10

    # Dibuja en la pantalla
    screen.fill(white)
    screen.blit(game_bg_img, (0, 0))
    screen.blit(dino_img, (dino_x, dino_y))

    if current_obstacle == "cactus":
        screen.blit(cactus_img, (cactus_x, cactus_y))
    elif current_obstacle == "bird":
        screen.blit(bird_img, (bird_x, bird_y))

    # Mostrar puntaje
    show_score()

    if game_over:
        restart_bg_img_blur = apply_blur(restart_bg_img, 5)  # Ajusta el factor según tus preferencias
        screen.blit(restart_bg_img_blur, (0, 0))
        show_game_over()
        restart_button = pygame.Rect(screen_width // 2 - 60, screen_height // 2 + 20, 120, 40)
        pygame.draw.rect(screen, (200, 200, 200), restart_button)
        restart_text = font.render("Reiniciar", True, black)
        screen.blit(restart_text, (screen_width // 2 - 50, screen_height // 2 + 30))

    pygame.display.flip()

    # Controla la velocidad del juego
    clock.tick(40)