import pygame
import sys
import random
import numpy as np
from tensorflow import keras

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
WIDTH, HEIGHT = 1000, 500
FPS = 120
POPULATION_SIZE = 4  # Número de jogadores na população
MUTATION_RATE = 0.1  # Taxa de mutação para os pesos dos neurônios

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cores dos jogadores
PLAYER_COLORS = [(255, 0, 0)] #(0, 255, 0), (0, 0, 255), (255, 255, 0)]

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

# Obstáculos
obstacle_width = 20
obstacle_height = 50
obstacle_speed = 20
obstacle_frequency = 20
obstacles = []
min_obstacle_distance = 50

# Pontuação
score = 0

# Função para reiniciar o jogo
def reset_game():
    global dino_y, obstacles, score
    dino_y = HEIGHT - dino_height
    obstacles = []
    score = 0

# Carrega o modelo da rede neural treinada
model = keras.models.load_model('dino_model.h5')

# Função para inicializar jogadores com variações nos pesos dos neurônios
def initialize_population():
    population = []
    for _ in range(POPULATION_SIZE):
        model = keras.Sequential([
            keras.layers.Dense(4, activation='relu', input_shape=(4,)),  # Camada de entrada com ativação ReLU
            keras.layers.Dense(1, activation='sigmoid')  # Camada de saída com ativação sigmoide
        ])
        # Adiciona variações nos pesos dos neurônios
        for layer in model.layers:
            if isinstance(layer, keras.layers.Dense):
                weights = layer.get_weights()
                weights[0] += np.random.normal(0, 0.1, weights[0].shape)  # Variação nos pesos
                layer.set_weights(weights)
        population.append((model, PLAYER_COLORS[len(population) % len(PLAYER_COLORS)]))
    return population

# Função para desenhar o dinossauro
def draw_dino(x, y, color):
    pygame.draw.rect(screen, color, [x, y, dino_width, dino_height])

# Função para desenhar obstáculos
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, WHITE, obstacle)

# Função para obter o estado do jogo
def get_game_state():
    if obstacles:
        return np.array([dino_y, obstacles[0].x, obstacles[0].y, obstacles[0].height])
    else:
        return np.array([dino_y, 0, 0, 0])

def select_players(population, scores):
    if len(scores) < POPULATION_SIZE:
        raise ValueError("Not enough scores for the population size.")
    
    sorted_indices = np.argsort(scores)[::-1]  # Índices ordenados em ordem decrescente de pontuação
    selected_indices = sorted_indices[:POPULATION_SIZE // 2]  # Seleciona os melhores jogadores
    selected_population = [population[i] for i in selected_indices]
    return selected_population

# Inicializa a população
population = initialize_population()

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Atualizações do jogo
    if dino_jump:
        if dino_jump_count >= -10:
            neg = 1
            if dino_jump_count < 0:
                neg = -1
            dino_y -= (dino_jump_count ** 2) * 0.5 * neg
            dino_jump_count -= 1
        else:
            dino_jump = False
            dino_jump_count = 10

    # Gera obstáculos
    if random.randrange(0, obstacle_frequency) == 1:
        if not obstacles or WIDTH - obstacles[-1].x > min_obstacle_distance:
            obstacle = pygame.Rect(WIDTH, HEIGHT - obstacle_height, obstacle_width, obstacle_height)
            obstacles.append(obstacle)

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

    # Atualiza pontuação para cada jogador
    scores = [score] * POPULATION_SIZE

    # Seleciona os jogadores mais aptos
    selected_population = select_players(population, scores)

    # Inicializa nova população com cruzamento e mutação
    new_population = []
    for i in range(POPULATION_SIZE):
        parent1, parent2 = random.sample(selected_population, 2)

        # Obtém os pesos de ambas as camadas das duas redes parentais
        weights1_layer1, weights1_layer2 = parent1[0].layers[0].get_weights(), parent1[0].layers[1].get_weights()
        weights2_layer1, weights2_layer2 = parent2[0].layers[0].get_weights(), parent2[0].layers[1].get_weights()

        # Cria novos pesos misturando os pesos dos pais
        mixed_weights_layer1 = (weights1_layer1[0] + weights2_layer1[0]) / 2.0
        mixed_weights_layer2 = (weights1_layer2[0] + weights2_layer2[0]) / 2.0

        # Aplica mutação aos pesos
        mixed_weights_layer1 += np.random.normal(0, MUTATION_RATE, mixed_weights_layer1.shape)
        mixed_weights_layer2 += np.random.normal(0, MUTATION_RATE, mixed_weights_layer2.shape)

        # Inicializa um novo modelo filho com os pesos misturados e mutados
        child_model = keras.Sequential([
            keras.layers.Dense(4, activation='relu', input_shape=(4,), weights=[mixed_weights_layer1, np.zeros(4)]),
            keras.layers.Dense(1, activation='sigmoid', weights=[mixed_weights_layer2, np.zeros(1)])
        ])

        # Adiciona o modelo filho à nova população
        new_population.append((child_model, PLAYER_COLORS[i % len(PLAYER_COLORS)]))

    # Atualiza a população
    population = new_population

    # Loop para cada jogador
    for player, color in population:
        # Obtém o estado do jogo
        game_state = get_game_state()

        # Tomada de decisão da rede neural
        prediction = player.predict(np.array([game_state]))

        # Ação da rede neural (0: não pula, 1: pula)
        if prediction[0][0] > 0.5:
            dino_jump = True

        # Desenha o fundo
        screen.fill(BLACK)

        # Desenha o dinossauro e obstáculos
        draw_dino(dino_x, dino_y, color)
        draw_obstacles(obstacles)

        # Atualiza a tela
        pygame.display.flip()

        # Limita a taxa de quadros por segundo
        clock.tick(FPS)
