import numpy as np
from tensorflow import keras
#from tensorflow.keras import layers

# Criar dados de treinamento (exemplo fictício)
# Os dados incluem a posição y do dinossauro, a posição x do obstáculo, a posição y do obstáculo e a altura do obstáculo
# 0 representa "não pular" e 1 representa "pular"
X_train = np.array([[100, 300, 200, 50], [150, 500, 180, 60], [120, 400, 220, 40]])
y_train = np.array([[0], [1], [0]])

# Normalizar os dados
X_train = X_train / np.max(X_train, axis=0)

# Criar modelo simples
model = keras.Sequential([
    keras.layers.Dense(4, activation='relu', input_shape=(4,)),  # Camada de entrada com ativação ReLU
    keras.layers.Dense(1, activation='sigmoid')  # Camada de saída com ativação sigmoide
])

# Compilar o modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Treinar o modelo
model.fit(X_train, y_train, epochs=100)

# Salvar o modelo
model.save('dino_model', save_format='tf')
