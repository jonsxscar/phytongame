import pygame
import sys
import random




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

# Inicializar variables de salto
dino_jump = False
jump_count = 10

#score
score = 0
scored = False

# Cargar imágenes
dino_img = pygame.image.load("kivy_venv\dino.png")
dino_img = pygame.transform.scale(dino_img, (50, 50))
cactus_img = pygame.image.load("kivy_venv\cactus.png")
cactus_img = pygame.transform.scale(cactus_img, (50, 50))
bird_img = pygame.image.load("kivy_venv\pajabird.png")
bird_img = pygame.transform.scale(bird_img, (50, 50))

# Inicializar variables de posición
dino_x = 40
dino_y = screen_height - dino_img.get_height() - 30 #altura del piso
cactus_x = screen_width
cactus_y = screen_height - cactus_img.get_height() - 30 #altura del piso
bird_x = screen_width
bird_y = random.randint(200, 300)

# Variables para el tipo de obstáculo actual
current_obstacle = None

# Función para mostrar el mensaje de pérdida y salir del juego
def game_over():
    print("¡Has perdido!")
    pygame.quit()
    sys.exit()

# Bucle principal del juego
clock = pygame.time.Clock()
game_running = True

def test():
    bird_y = random.randint(200, 300)


while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Lógica de movimiento del dinosaurio
    keys = pygame.key.get_pressed()
    # Lógica de salto
    if not dino_jump:
        if keys[pygame.K_SPACE]:
            dino_jump = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            dino_y -= (jump_count ** 2) * 0.3 * neg
            jump_count -= 0.5
        else:
            dino_jump = False
            jump_count = 10

    # Actualiza la posición del cactus
    cactus_x -= 5
    if cactus_x < 0:
        cactus_x = screen_width
        current_obstacle = random.choice(["cactus", "bird"])
        scored = False

    # Actualiza la posición del ave
    bird_x -= 5
    test()
    #bird_y = random.randint(200, 300) #prueba
    if bird_x < 0:
        bird_x = screen_width
        current_obstacle = random.choice(["cactus", "bird"])
        scored = False
    print(bird_y) 

    # Colisiones con el obstáculo actual
    if current_obstacle == "cactus":
        if (
            dino_x < cactus_x + cactus_img.get_width()
            and dino_x + dino_img.get_width() > cactus_x
            and dino_y < cactus_y + cactus_img.get_height()
            and dino_y + dino_img.get_height() > cactus_y
        ):
            game_over()
        elif not scored:
            score += 10
            scored = True

    elif current_obstacle == "bird":
        if (
            dino_x < bird_x + bird_img.get_width()
            and dino_x + dino_img.get_width() > bird_x
            and dino_y < bird_y + bird_img.get_height()
            and dino_y + dino_img.get_height() > bird_y
        ):
            game_over()
        elif not scored:
            score += 10
            scored = True

        # Dibuja en la pantalla
    screen.fill(white)
    screen.blit(dino_img, (dino_x, dino_y))

    if current_obstacle == "cactus":
        screen.blit(cactus_img, (cactus_x, cactus_y))
    elif current_obstacle == "bird":
        screen.blit(bird_img, (bird_x, bird_y))

    # Mostrar puntaje
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Controla la velocidad del juego
    clock.tick(40)

# Cierra pygame al salir del bucle principal
pygame.quit()
sys.exit()