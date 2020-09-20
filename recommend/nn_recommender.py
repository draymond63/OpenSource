import pandas as pd
from OpenSource.general import pull_json, REPO_TO_USER_FILE, NN_OUTPUT

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
        self.model.fit(i.tolist(), o.tolist(), batch_size=64, epochs=epochs)

def create_model(inp=REPO_TO_USER_FILE, out=NN_OUTPUT):
    # Input training data
    inp = pd.read_csv(inp, index_col='Unnamed: 0')
    inp = inp.drop('repos', axis=1)
    # Output training data
    out = pd.read_csv(out, index_col='Unnamed: 0', squeeze=True)
    # convert outputs from string to list
    out = out.apply(lambda x: [int(i) for i in x.split(',')])
    # Build the model and train it!
    rec = NeuralRecommender()
    rec.train(inp, out)

if __name__ == "__main__":
    create_model()
    
