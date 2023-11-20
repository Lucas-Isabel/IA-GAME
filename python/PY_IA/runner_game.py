import pygame
import random
from player_keras import RunnerKeras
import numpy as np
import sys
import os

class RunnerGame:
    def __init__(self):
        # Inicialização do Pygame
        pygame.init()
        current_dir = os.path.dirname(__file__)

        # Configuração da janela
        self.WIDTH, self.HEIGHT = 1000, 500
        self.FPS = 60
        self.background_image = pygame.image.load(os.path.join(current_dir, "View", "background.png"))
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        self.background_rect1 = self.background_image.get_rect(topleft=(0, 0))
        self.background_rect2 = self.background_image.get_rect(topleft=(self.WIDTH, 0))
        self.scroll_speed = 5

        self.gravity = 7.0


        # Cores
        self.WHITE = (255, 255, 255)
        self.Black = (0, 0, 0)
        self.Bk_color = (0, 0, 121)

        # Fonte
        self.font = pygame.font.Font(None, 36)

        # Jogador (Dinossauro)
        self.dino_width = 50
        self.dino_height = 50
        self.dino_x = 50
        self.dino_y = self.HEIGHT - self.dino_height
        self.dino_jump = False
        self.dino_jump_count = 11
        self.jump_impulse = 0  
        self.jump = False
        self.player_color = (255, 0, 255)
        self.player_image = pygame.image.load(os.path.join(current_dir, "View", "caique1.png"))
        self.player_image = pygame.transform.scale(self.player_image, (50, 50))
        self.player_image2 = pygame.image.load(os.path.join(current_dir, "View", "caique2.png"))
        self.player_image2 = pygame.transform.scale(self.player_image2, (50, 50))
        self.player_sprite_state = 1

        self.array_caique = [self.player_image, self.player_image2]

        # Obstáculos
        self.obstacle_width = random.randint(40, 60)
        self.obstacle_height = random.randint(100, 150)
        self.obstacle_speed = 20
        self.obstacle_frequency = 500
        self.obstacles = []
        self.min_obstacle_distance = 50
        self.last_obstacle_time = 0
        self.seconds = 1.5
        self.obstacle_color = (0,0,205)
        self.obstacle_image = pygame.image.load(os.path.join(current_dir, "View", "lixeira.png"))
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (self.obstacle_width, self.obstacle_height))

        # Pontuação
        self.score = 130

        
        

        # Especifique o caminho para o arquivo de fonte desejado (substitua 'caminho/para/sua/fonte.ttf' pelo caminho real)
        self.font_path = os.path.join(current_dir, 'Consolas-Font', 'CONSOLAS.ttf')

        # Defina o tamanho da fonte desejado
        self.font_size = 18


        
        # Inicialização do modelo Keras
        self.keras_model = RunnerKeras()

    def reset_game(self):
        self.obstacles = []
        self.score = 0
        self.obstacle_speed = 20
        self.dino_y = 470#self.dino_height

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

    """
    def generate_obstacle(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_time > self.seconds * 1000:
            if not self.obstacles or self.WIDTH - self.obstacles[-1].x > self.min_obstacle_distance:
                obstacle = pygame.Rect(self.WIDTH, self.HEIGHT - self.obstacle_height, self.obstacle_width, self.obstacle_height)
                self.obstacles.append(obstacle)
                self.last_obstacle_time = current_time
    """
    def generate_obstacle(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_time > self.seconds * 1000:
            if not self.obstacles or self.WIDTH - self.obstacles[-1].x > self.min_obstacle_distance:
                obstacle_rect = self.obstacle_image.get_rect()
                obstacle_rect.x = self.WIDTH
                obstacle_rect.y = self.HEIGHT - self.obstacle_height
                self.obstacles.append(obstacle_rect)
                self.last_obstacle_time = current_time

    def draw_obstacles(self, screen):
        for obstacle in self.obstacles:
            screen.blit(self.obstacle_image, obstacle)
            if self.dino_x < obstacle.x + obstacle.width and self.dino_x + self.dino_width > obstacle.x:
                if self.dino_y >= obstacle.y:
                    print("Dino pulou sobre um obstáculo!")
                    self.score += 10
                    if self.dino_y >= obstacle.y:
                        print("Dino pulou sobre um obstáculo!")
                        self.score += 200

    def draw_player(self, screen):
        if self.player_sprite_state % 2 == 0: 
            screen.blit(self.player_image, (self.dino_x, self.dino_y))
            self.player_sprite_state += 1
        else: 
            screen.blit(self.player_image2, (self.dino_x, self.dino_y))
            self.player_sprite_state += 1


    def run(self):
        pygame.display.set_caption("Dino Runner")
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        custom_font = pygame.font.Font(self.font_path, self.font_size)
    



        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Move a imagem para a esquerda
            self.background_rect1.x -= self.scroll_speed
            self.background_rect2.x -= self.scroll_speed

            # Se a primeira imagem ultrapassar a largura da tela, reinicie a posição
            if self.background_rect1.right <= 0:
                self.background_rect1.x = self.WIDTH

            # Se a segunda imagem ultrapassar a largura da tela, reinicie a posição
            if self.background_rect2.right <= 0:
                self.background_rect2.x = self.WIDTH


            # Atualizações do jogo
            self.dino_state()

            self.generate_obstacle()

            obstacle_width_changer = random.randint(40, 60)
            obstacle_heitght_changer = random.randint(100, 150)
            self.obstacle_width = obstacle_width_changer
            self.obstacle_height = obstacle_heitght_changer

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

            #Desenha tela
            screen.blit(self.background_image, self.background_rect1)
            screen.blit(self.background_image, self.background_rect2)

            # Desenha o dinossauro e obstáculos
            #pygame.draw.rect(screen, self.player_color, [self.dino_x, self.dino_y, self.dino_width, self.dino_height])
            self.draw_player(screen)
            self.draw_obstacles(screen)
            """"
            for obstacle in self.obstacles:
                pygame.draw.rect(screen, self.obstacle_color, obstacle)
                if self.dino_x < obstacle.x + obstacle.width and self.dino_x + self.dino_width > obstacle.x:
                    print("Dino pulou sobre um obstáculo!")
                    self.score += 10
                    if self.dino_y >= obstacle.y:
                        print("Dino pulou sobre um obstáculo!")
                        self.score += 200
            """
                

            # Renderiza os pesos na tela
            weights_text  = f'pular: {prediction:.2f} | '
            weights_text += f'Não pular: {1 - prediction:.2f} |' 
            weights_text += f'Pontos: {self.score:.2f} |'
            weights_text += f'Velocidade: {self.obstacle_speed:.2f} {self.player_sprite_state} |'
            weights_render = custom_font.render(weights_text, True, self.WHITE)
            screen.blit(weights_render, (10, 10))
            n = float(random.randint(20,40))/10
            self.seconds = n 
            self.obstacle_speed += 0.01
            # Atualiza a tela
            pygame.display.flip()

            # Limita a taxa de quadros por segundo
            clock.tick(self.FPS)
