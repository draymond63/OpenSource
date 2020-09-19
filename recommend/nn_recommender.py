import pandas as pd
from OpenSource.general import pull_json, NN_INPUT

from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import keras
environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


class NeuralRecommender():
    def __init__(self, weights=None):
        self.model = keras.Sequential([
            keras.layers.Dense(50, activation='relu'),
            keras.layers.Dense(50, activation='softmax'),
        ])

        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

    def train(self, i, o, epochs=50):
        self.model.fit(i, o, batch_size=64, epochs=epochs)

def create_model(data=NN_INPUT):
    data = pd.read_csv(data)

    rec = NeuralRecommender()
    # rec.train(data)

if __name__ == "__main__":
    create_model()
    
