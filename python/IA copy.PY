import pygame
import sys
import random
import numpy as np
from tensorflow import keras

# Inicialização do Pygame
pygame.init()

gravity = 12.0

WIDTH, HEIGHT = 1000, 500
FPS = 120
MUTATION_RATE = 0.1  # Taxa de mutação para os pesos dos neurônios

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#fonte
font = pygame.font.Font(None, 36)

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
dino_jump_count = 11
jump_impulse = 0  # Ajuste este valor conforme necessário
jump = False

# Obstáculos
obstacle_width = 20
obstacle_height = 50
obstacle_speed = 20
obstacle_frequency = 500
obstacles = []
min_obstacle_distance = 50
last_obstacle_time = 0

# Pontuação
score = 300

# Função para reiniciar o jogo
def reset_game():
    global dino_y, obstacles, score
    obstacles = []
    score = 300
    dino_y = HEIGHT - dino_height

def generate_obstacle(obstacles, last_obstacle_time, obstacle_frequency, min_obstacle_distance, WIDTH, HEIGHT, obstacle_width, obstacle_height, seconds):
    current_time = pygame.time.get_ticks()
    if current_time - last_obstacle_time > seconds * 1000:  # Convertendo segundos para milissegundos
        if not obstacles or WIDTH - obstacles[-1].x > min_obstacle_distance:
            obstacle = pygame.Rect(WIDTH, HEIGHT - obstacle_height, obstacle_width, obstacle_height)
            obstacles.append(obstacle)
            last_obstacle_time = current_time
    return obstacles, last_obstacle_time

# Geração de conjunto de dados de treinamento
X_train = []
y_train = []

for _ in range(1000):
    # Gera um estado aleatório do jogo
    dino_y = HEIGHT - dino_height
    obstacle_x = WIDTH - obstacle_width
    obstacle_y = np.random.randint(0, HEIGHT - obstacle_height)

    # Gera a ação correta
    if dino_y < obstacle_y:
        action = 1  # Pular
    else:
        action = 0  # Não pular

    # Adiciona o estado e a ação ao conjunto de dados
    X_train.append([dino_y, obstacle_x, obstacle_y, obstacle_height])
    y_train.append(action)

# Inicialização do modelo
model = keras.models.Sequential([
    keras.layers.Dense(4, activation='relu', input_shape=(4,)),
    keras.layers.Dense(2, activation='sigmoid')  # Dois neurônios de saída
])

# Treinamento do modelo
model.compile(loss='mse', optimizer='sgd', metrics=['accuracy'])
model.fit(X_train, y_train, epochs= 450, steps_per_epoch=90)

# Taxa de aprendizado
learning_rate = 0.01  # Originalmente 0.1

# Tamanho do lote
batch_size = 10  # Originalmente 100


# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Atualizações do jogo
#    if dino_jump:
#            if dino_y >= 0:
#                dino_jump = True
#        else:
#            dino_jump = False
#            dino_jump_count -= 1

    """
    # Atualizações do jogo
    if dino_jump:
        if dino_jump_count >= -7:
            neg = 1
            if dino_jump_count < 0:
                neg = -1
            dino_y -= (dino_jump_count ** 2) * 0.5 * neg
            dino_jump_count -= 1
        else:
            dino_jump = False
            dino_jump_count = 7

    # Gera obstáculos

    if random.randrange(0, obstacle_frequency) == 1:
        if not obstacles or WIDTH - obstacles[-1].x > min_obstacle_distance:
            obstacle = pygame.Rect(WIDTH, HEIGHT - obstacle_height, obstacle_width, obstacle_height)
            obstacles.append(obstacle)
"""
    num = 1
    obstacles, last_obstacle_time = generate_obstacle(
        obstacles, last_obstacle_time, obstacle_frequency,
        min_obstacle_distance, WIDTH, HEIGHT,
        obstacle_width, obstacle_height, seconds=num  # Substitua 1 pelo número de segundos desejado
    )

    min_obstacle_distance = random.randint(50, 75)

    # Move obstáculos
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed

    # Remove obstáculos fora da tela
    obstacles = [obs for obs in obstacles if obs.x > 0]

    # Verifica colisão com obstáculos
    for obstacle in obstacles:
        if dino_x < obstacle.x + obstacle.width and dino_x + dino_width > obstacle.x:
            if dino_y + dino_height > obstacle.y:
                # Aumenta a pontuação com base no pulo do dinossauro
                score += 100 + int(100 * (dino_jump_count / 11))

                print(f"Game Over! Pontuação: {score}")
                reset_game()
    
    score -= 1.95


    # Atualiza pontuação

    #obstacle_height = np.random.randint(10, 50)
    #obstacle_width = np.random.randint(10, 50)
    obstacle_height = 50
    obstacle_width = 10
    # Obtém o estado do jogo
    game_state = np.array([dino_y, obstacles[0].x, obstacles[0].y, obstacles[0].height]) if obstacles else np.zeros(4)

    # Tomada de decisão da rede neural
    prediction = model.predict(np.array([game_state]))

    # Ação da rede neural (0: não pula, 1: pula, 2: para de pular)
    if prediction[0][0] > 0.5:
        if dino_y >= HEIGHT - dino_height and not dino_jump:
            dino_jump = True
    elif prediction[0][1] > 0.5:
        if dino_jump:
            dino_jump = False
            dino_jump_count = 11
            jump_impulse = 0

    # Atualizações do jogo
    if dino_jump:
        if dino_jump_count >= -11:
            neg = 1
            if dino_jump_count < 0:
                neg = -1
            jump_impulse += 1  # Aumenta o impulso com o tempo que a tecla é mantida pressionada
            dino_y -= ((dino_jump_count ** 2) * 0.5 * neg) + jump_impulse
            dino_jump_count -= 1
        else:
            dino_jump = False
            dino_jump_count = 11  # Ajustado para 11
            jump_impulse = 0

    # Aplica a gravidade para simular a queda
    if not dino_jump and dino_y < HEIGHT - dino_height:
        dino_y += gravity

    """
    if dino_x < obstacle.x + obstacle.width and dino_x + dino_width > obstacle.x:
        if dino_y >= obstacle.y and dino_x >= obstacle.x: 
            # Incrementa a pontuação de maneira mais significativa
            score += 1000

    if dino_x >= obstacle.x:
            # Incrementa a pontuação de maneira mais significativa
            score += 1000
    """
    # Desenha o fundo
    screen.fill(BLACK)
       

    # Desenha o dinossauro e obstáculos
    pygame.draw.rect(screen, WHITE, [dino_x, dino_y, dino_width, dino_height])
    # Atualizações do jogo
    for obstacle in obstacles:
        pygame.draw.rect(screen, WHITE, obstacle)
        # Verifica colisão com obstáculos
      # ou qualquer valor que você considere apropriado

# Renderiza os pesos na tela
    weights_text = f'Peso para pular: {prediction[0][0]:.2f} | Peso para não pular: {1 - prediction[0][0]:.2f} | Pontos: {score:.2f} '
    weights_render = font.render(weights_text, True, WHITE)
    screen.blit(weights_render, (10, 10))

    # Atualiza a tela
    pygame.display.flip()

    # Limita a taxa de quadros por segundo
    clock.tick(FPS)
