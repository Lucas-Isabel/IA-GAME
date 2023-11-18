import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
WIDTH, HEIGHT = 1000, 500
FPS = 40

# Velocidade de queda
gravity = 5

# Diminui a velocidade de queda
#gravity = -10



# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuração da janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner")
clock = pygame.time.Clock()

# Jogador (Dinossauro)
dino_width = 30
dino_height = 30
dino_x = 50
dino_y = HEIGHT - dino_height
dino_jump = False
dino_jump_count = 10
jump_impulse = 0  # Ajuste este valor conforme necessário
jump = False


# Obstáculos
obstacle_width = 15
obstacle_height = 50
obstacle_speed = 5
obstacle_frequency = 70
obstacles = []
min_obstacle_distance = 15           
last_obstacle_time = 0

# Pontuação
score = 0

def reset_game():
    global dino_y, obstacles, score
    dino_y = HEIGHT - dino_height
    obstacles = []
    score = 0

# Função para desenhar o dinossauro
def draw_dino(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, dino_width, dino_height])

# Função para desenhar obstáculos
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, WHITE, obstacle)

def generate_obstacle(obstacles, last_obstacle_time, obstacle_frequency, min_obstacle_distance, WIDTH, HEIGHT, obstacle_width, obstacle_height, seconds):
    current_time = pygame.time.get_ticks()
    if current_time - last_obstacle_time > seconds * 1000:  # Convertendo segundos para milissegundos
        if not obstacles or WIDTH - obstacles[-1].x > min_obstacle_distance:
            obstacle = pygame.Rect(WIDTH, HEIGHT - obstacle_height, obstacle_width, obstacle_height)
            obstacles.append(obstacle)
            last_obstacle_time = current_time
    return obstacles, last_obstacle_time

# Loop principal do jogo
while True:
    obstacle_width = random.randint(15, 30)
    obstacle_height =  random.randint(10, 60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not dino_jump and dino_y >= 0:
            dino_jump = True

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and dino_jump:
            dino_jump = False
            dino_jump_count = 10
            jump_impulse = 0


        if dino_jump:
            if dino_jump_count >= -10:
                neg = 1
                if dino_jump_count < 0:
                    neg = -1
                jump_impulse += 1  # Aumenta o impulso com o tempo que a tecla é mantida pressionada
                dino_y -= ((dino_jump_count ** 2) * 0.5 * neg) + jump_impulse
                dino_jump_count -= 1
            else:
                dino_jump = False
                dino_jump_count = 10
                jump_impulse = 0

        if dino_y < 0:
            dino_y += gravity

    


        """

            # Atualizações do jogo
    if dino_jump:
        if dino_jump_count >= -10:
            neg = 1
            if dino_jump_count < 0:
                neg = -1
            dino_y -= ((dino_jump_count ** 2) * 0.5 * neg) #+ jump_impulse # Ajuste este valor conforme necessário
            dino_jump_count -= 1
            jump_impulse = 0 
        else:
            dino_jump = False
            dino_jump_count = 10


    # Gera obstáculos

    if random.randrange(0, obstacle_frequency) == 1:
        if not obstacles or WIDTH - obstacles[-1].x > min_obstacle_distance:
            obstacle = pygame.Rect(WIDTH, HEIGHT - obstacle_height, obstacle_width, obstacle_height)
            obstacles.append(obstacle)
        """
        num = float(random.randint(50, 100) / 100)
        obstacles, last_obstacle_time = generate_obstacle(
            obstacles, last_obstacle_time, obstacle_frequency,
            min_obstacle_distance, WIDTH, HEIGHT,
            obstacle_width, obstacle_height, seconds=num  # Substitua 1 pelo número de segundos desejado
        )

    # Move obstáculos
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed

    # Remove obstáculos fora da tela
    obstacles = [obs for obs in obstacles if obs.x > 0]

    # Verifica colisão com obstáculos
    
    for obstacle in obstacles:
        if dino_x < obstacle.x + obstacle.width and dino_x + dino_width > obstacle.x:
            if dino_y + dino_height > obstacle.y:
                print(f"Game Over! Pontuação: {score}")
                reset_game()
                

    # Atualiza pontuação
    score += 1

    # Atualiza pontuação
         

    # Desenha o fundo
    screen.fill(BLACK)

    # Desenha o dinossauro e obstáculos
    draw_dino(dino_x, dino_y)
    draw_obstacles(obstacles)

    # Atualiza a tela
    pygame.display.flip()

    # Limita a taxa de quadros por segundo
    clock.tick(FPS)
        