import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Cargar y reproducir música de fondo
pygame.mixer.music.load("BorgAtacan.mp3")  # Cambia esto por el nombre de tu archivo de música

pygame.mixer.music.play(-1)  # -1 para reproducir en bucle

# Configuración de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("VOYAGER EN EL ESPACIO BORG")

# Cargar la imagen de fondo
background_image = pygame.image.load("FONDO.GIF")
background_image = pygame.transform.scale(background_image, (width, height))

# Cargar la imagen que se mueve
image = pygame.image.load("Voyager.png")
image = pygame.transform.scale(image, (50, 50))

# Cargar la imagen del obstáculo
obstacle_image = pygame.image.load("CuboBorg.png")
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))

# Obtener el rectángulo de la imagen que se mueve
image_rect = image.get_rect()
image_rect.x = 100
image_rect.y = 100
rect_speed = 5

# Configuración de los obstáculos
obstacles = []

# Inicializar balas
bullets = []

bullet_speed = 10


# Inicializar la fuente
font = pygame.font.SysFont(None, 30)

# Inicializar vidas
lives = 3

# Función para crear un nuevo obstáculo
def create_obstacle():
    x_position = random.randint(0, width - 50)
    new_obstacle = pygame.Rect(x_position, 0, 50, 50)
    obstacles.append(new_obstacle)

# Función para disparar
def shoot_bullet():
    bullet = pygame.Rect(image_rect.centerx, image_rect.y, 5, 10)  # Bala pequeña
    bullets.append(bullet)

# Función para mostrar el mensaje de Game Over
def show_game_over():
    text = font.render("FUISTE ASIMILADO!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

# Función para mostrar el número de vidas restantes
def show_lives():
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detectar si se dispara con la barra espaciadora
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot_bullet()  # Disparar una bala

    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        image_rect.x -= rect_speed
    if keys[pygame.K_RIGHT]:
        image_rect.x += rect_speed
    if keys[pygame.K_UP]:
        image_rect.y -= rect_speed
    if keys[pygame.K_DOWN]:
        image_rect.y += rect_speed

    # Limitar el movimiento dentro de la ventana
    image_rect.x = max(0, min(image_rect.x, width - image_rect.width))
    image_rect.y = max(0, min(image_rect.y, height - image_rect.height))

    # Crear un nuevo obstáculo aleatoriamente
    if random.randint(1, 30) == 1:
        create_obstacle()

    # Mover los obstáculos hacia abajo
    for obstacle in obstacles:
        obstacle.y += 5
        if image_rect.colliderect(obstacle):
            lives -= 1
            obstacles.remove(obstacle)
            if lives == 0:
                show_game_over()
                pygame.quit()
                sys.exit()

    # Mover las balas hacia arriba
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Eliminar obstáculos si son alcanzados por una bala
    for bullet in bullets:
        for obstacle in obstacles:
            if bullet.colliderect(obstacle):
                obstacles.remove(obstacle)
                if bullet in bullets:
                    bullets.remove(bullet)  # Eliminar la bala si golpea el obstáculo

    # Eliminar obstáculos que salieron de la pantalla
    obstacles = [obstacle for obstacle in obstacles if obstacle.y < height]

    # Dibujar el fondo
    screen.blit(background_image, (0, 0))

    # Dibujar la imagen que se mueve
    screen.blit(image, image_rect)

    # Dibujar los obstáculos como imágenes
    for obstacle in obstacles:
        screen.blit(obstacle_image, obstacle.topleft)

    # Dibujar las balas
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet)  # Bala amarilla

    # Mostrar vidas restantes
    show_lives()

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    pygame.time.Clock().tick(60)
