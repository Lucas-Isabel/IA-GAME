# game.py
import os
import pygame
import numpy as np
from runner_game import RunnerGame

def main():
    pygame.init()
    game = RunnerGame()

    X_train = []
    y_train = []

    # Verifica se o modelo "best_runner.h5" já existe
    if os.path.exists("best_runner.h5"):
        game.keras_model.load_model("best_runner.h5")
        exploration_rate = 0.1  # Diminui a taxa de exploração se carregar um modelo pré-existente

    for _ in range(1999):
        # Gera um estado aleatório do jogo
        dino_y = game.HEIGHT - game.dino_height
        obstacle_x = game.WIDTH - game.obstacle_width
        obstacle_y = np.random.randint(0, game.HEIGHT - game.obstacle_height)

        # Calcula a distância entre o dino e o obstáculo
        distance_to_obstacle = obstacle_x - game.dino_x

        # Gera a ação correta
        if dino_y < obstacle_y:
            action = 1  # Pular
        else:
            action = 0  # Não pular

        # Adiciona o estado, a ação e a distância ao conjunto de dados
        X_train.append([dino_y, obstacle_x, obstacle_y, game.obstacle_height, distance_to_obstacle])
        y_train.append(action)

    game.keras_model.train_model(np.array(X_train), np.array(y_train))

    # Salvando o modelo treinado ao final dos episódios
    game.keras_model.model.save("runner_model.h5")

    # Verifica se o modelo é melhor e, se for, salva como "best_runner.h5"
    """if os.path.exists("best_runner.h5"):
        best_model_score = game.keras_model.evaluate_best_model()
        current_model_score = game.keras_model.evaluate_current_model()

        if current_model_score > best_model_score:
            os.remove("best_runner.h5")
            os.rename("runner_model.h5", "best_runner.h5")"""

    game.run()



if __name__ == "__main__":
    main()
