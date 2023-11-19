import pygame
import random
from player_keras import RunnerKeras
import numpy as np
import sys

class RunnerGame:
    def __init__(self):
        # Inicialização do Pygame
        pygame.init()

        # Configuração da janela
        self.WIDTH, self.HEIGHT = 1000, 500
        self.FPS = 120
        self.gravity = 7.0

        # Cores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Fonte
        self.font = pygame.font.Font(None, 36)

        # Jogador (Dinossauro)
        self.dino_width = 30
        self.dino_height = 30
        self.dino_x = 50
        self.dino_y = self.HEIGHT - self.dino_height
        self.dino_jump = False
        self.dino_jump_count = 11
        self.jump_impulse = 0  # Ajuste este valor conforme necessário
        self.jump = False

        # Obstáculos
        self.obstacle_width = 20
        self.obstacle_height = 50
        self.obstacle_speed = 20
        self.obstacle_frequency = 500
        self.obstacles = []
        self.min_obstacle_distance = 50
        self.last_obstacle_time = 0
        self.seconds = 1.5

        # Pontuação
        self.score = 130

        # Inicialização do modelo Keras
        self.keras_model = RunnerKeras()

    def reset_game(self):
        self.obstacles = []
        self.score = 0
        self.dino_y = self.HEIGHT - self.dino_height

    def dino_state(self):
        if self.dino_jump:
            if self.dino_jump_count >= -10:
                neg = 1
                if self.dino_jump_count < 0:
                    neg = -1
                self.jump_impulse += 1
                self.dino_y -= ((self.dino_jump_count ** 2) * 0.5 * neg) + self.jump_impulse
                self.dino_jump_count -= 1
            else:
                self.dino_jump = False
                self.dino_jump_count = 10
                self.jump_impulse = 0

        # Aplica a gravidade para simular a queda
        if self.dino_y < self.HEIGHT - self.dino_height:
            self.dino_y += self.gravity


    def generate_obstacle(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_time > self.seconds * 1000:
            if not self.obstacles or self.WIDTH - self.obstacles[-1].x > self.min_obstacle_distance:
                obstacle = pygame.Rect(self.WIDTH, self.HEIGHT - self.obstacle_height, self.obstacle_width, self.obstacle_height)
                self.obstacles.append(obstacle)
                self.last_obstacle_time = current_time

    def run(self):
        pygame.display.set_caption("Dino Runner")
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Atualizações do jogo
            self.dino_state()

            self.generate_obstacle()

            # Move obstáculos
            for obstacle in self.obstacles:
                obstacle.x -= self.obstacle_speed

            # Remove obstáculos fora da tela
            self.obstacles = [obs for obs in self.obstacles if obs.x > 0]

            # Verifica colisão com obstáculos
            for obstacle in self.obstacles:
                if self.dino_x < obstacle.x + obstacle.width and self.dino_x + self.dino_width > obstacle.x:
                    if self.dino_y + self.dino_height > obstacle.y:
                        print(f"Game Over! Pontuação: {self.score}")
                        self.reset_game()

            # Atualiza pontuação
            self.score -= 0.5
            obstacle_height = 50
            obstacle_width = 10
            obstacle_x = self.WIDTH - self.obstacle_width
            distance_to_obstacle = obstacle_x - self.dino_x
            # Obtém o estado do jogo
            game_state = np.array([self.dino_y, self.obstacles[0].x, self.obstacles[0].y, self.obstacles[0].height, distance_to_obstacle]) if self.obstacles else np.zeros(5)

            # Tomada de decisão da rede neural
            prediction = self.keras_model.make_prediction(game_state)

            # Ação da rede neural (0: não pula, 1: pula)
            if prediction:
                if self.dino_y >= self.HEIGHT - self.dino_height and not self.dino_jump:
                    self.dino_jump = True

            # Desenha o fundo
            screen.fill(self.BLACK)

            # Desenha o dinossauro e obstáculos
            pygame.draw.rect(screen, self.WHITE, [self.dino_x, self.dino_y, self.dino_width, self.dino_height])

            for obstacle in self.obstacles:
                pygame.draw.rect(screen, self.WHITE, obstacle)
                if self.dino_x < obstacle.x + obstacle.width and self.dino_x + self.dino_width > obstacle.x:
                    print("Dino pulou sobre um obstáculo!")
                    self.score += 10
                    if self.dino_y >= obstacle.y:
                        print("Dino pulou sobre um obstáculo!")
                        self.score += 200
                

            # Renderiza os pesos na tela
            weights_text = f'Peso para pular: {prediction:.2f} | Peso para não pular: {1 - prediction:.2f} | Pontos: {self.score:.2f} '
            weights_render = self.font.render(weights_text, True, self.WHITE)
            screen.blit(weights_render, (10, 10))
            n = float(random.randint(20,40))/10
            self.seconds = n 
            # Atualiza a tela
            pygame.display.flip()

            # Limita a taxa de quadros por segundo
            clock.tick(self.FPS)
