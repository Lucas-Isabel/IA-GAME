import numpy as np
from tensorflow import keras

class RunnerKeras:
    def __init__(self):
        # Inicialização do modelo
        self.model = keras.models.Sequential([
            keras.layers.Dense(5, activation='relu', input_shape=(5,)),
            keras.layers.Dense(1, activation='sigmoid')
        ])

        # Taxa de aprendizado
        self.learning_rate = 0.01

        # Tamanho do lote
        self.batch_size = 10

    def train_model(self, X_train, y_train):
        # Treinamento do modelo
        self.model.compile(loss='mse', optimizer='sgd', metrics=['accuracy'])
        self.model.fit(X_train, y_train, epochs=222, batch_size=self.batch_size, steps_per_epoch=21)

    def load_model(self, filename):
        # Carrega um modelo pré-existente
        self.model = keras.models.load_model(filename)

    def make_prediction(self, game_state):
        # Tomada de decisão da rede neural
        prediction = self.model.predict(np.array([game_state]))

        # Ação da rede neural (0: não pula, 1: pula)
        return prediction[0][0] > 0.5
