import pygame
import sys
import random
import numpy as np
from tensorflow import keras

# Configurações do jogo
WIDTH, HEIGHT = 1000, 500
FPS = 120
MUTATION_RATE = 0.1  # Taxa de mutação para os pesos dos neurônios
POPULATION_SIZE = 10  # Tamanho da população
PLAYER_COLORS = [(255, 0, 0), (0, 255, 0)]

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# fonte
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

# Obstáculos
obstacle_width = 20
obstacle_height = 50
obstacle_speed = 20
obstacle_frequency = 2000
obstacles = []
min_obstacle_distance = 50
last_obstacle_time = 0

# Pontuação
score = 0


# Função para reiniciar o jogo
def reset_game():
    global dino_y, obstacles, score
    dino_y = HEIGHT - dino_height
    obstacles = []
    score = 0


def generate_obstacle(obstacles, last_obstacle_time, obstacle_frequency, min_obstacle_distance, WIDTH, HEIGHT, obstacle_width, obstacle_height, seconds):
    current_time = pygame.time.get_ticks()
    if current_time - last_obstacle_time > seconds * 1000:  # Convertendo segundos para milissegundos
        if not obstacles or WIDTH - obstacles[-1].x > min_obstacle_distance:
            obstacle = pygame.Rect(WIDTH, HEIGHT - obstacle_height, obstacle_width, obstacle_height)
            obstacles.append(obstacle)
            last_obstacle_time = current_time
    return obstacles, last_obstacle_time


# Função para avaliar o desempenho dos jogadores
def evaluate_population(population, scores):
    if len(scores) < POPULATION_SIZE:
        raise ValueError("Not enough scores for the population size.")

    # Adiciona as pontuações aos modelos e as cores
    population_with_scores = list(zip(population, scores))

    # Ordena a população com base nas pontuações, do maior para o menor
    evaluated_population = sorted(population_with_scores, key=lambda x: x[1], reverse=True)

    return evaluated_population


# Função para realizar o cruzamento para criar um novo modelo combinando pesos de dois modelos pai
def crossover(parent1_weights, parent2_weights):
    # Obtém os pesos dos modelos dos pais
    parent1_weights = list(parent1_weights)
    parent2_weights = list(parent2_weights)

    # Realiza o cruzamento
    child_weights = []
    for weights1, weights2 in zip(parent1_weights, parent2_weights):
        crossover_point = np.random.randint(0, len(weights1))
        child_weights.append(np.concatenate((weights1[:crossover_point], weights2[crossover_point:])))

    # Retorna o modelo filho com os pesos cruzados
    child_model = keras.Sequential([
        keras.layers.Dense(4, activation='relu', input_shape=(4,)),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    set_weights(child_model, child_weights)

    return child_model


# Função para aplicar mutação
def mutate(weights, mutation_rate):
    # Implemente
