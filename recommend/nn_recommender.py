import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

from OpenSource.general import USER_FILE, NN_OUTPUT, NN_WEIGHTS
from OpenSource.general import REPO_NAME_COLUMN, USER_NAME_COLUMN, USER_REPOS_COLUMN

from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Hush the warnings
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense
from tensorflow.keras import Sequential
environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


class NeuralRecommender():
    def __init__(self, input_size=50, output_size=100, metric='accuracy'):
        self.metric = metric
        # MODEL SHAPE
        self.model = Sequential([
            Dense(200, activation='tanh', input_shape=(input_size,)),
            Dense(1000, activation='tanh'),
            Dense(output_size, activation='softmax'),
        ])
        # MODEL PARAMS
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=[metric]
        )
        # SUMMARIZATION
        self.model.build()
        self.model.summary()

    def train(self, i, o, epochs=5000):
        callbacks = (
            EarlyStopping(patience=epochs//10, monitor=self.metric, restore_best_weights=True),
        )
        self.model.fit(i, o, 
            batch_size=64, 
            shuffle=True, 
            epochs=epochs,
            callbacks=callbacks,
            verbose=0
        )

    def save(self, file_name=NN_WEIGHTS):
        self.model.save_weights(file_name)

def create_model(inp=USER_FILE, out=NN_OUTPUT):
    # Input training data
    inp = pd.read_csv(inp)
    inp = inp.drop(USER_REPOS_COLUMN, axis=1) # Need to drop this early so it won't conflict in the merge
    # Output training data
    out = pd.read_csv(out)
    # Sort so the datasets are aligned
    data = pd.merge(inp, out, on=USER_NAME_COLUMN)
    data.dropna(inplace=True) # Drop all bad rows
    inp = data.filter(inp.columns)
    out = data.filter(out.columns)

    # Remove data that isn't being fed into the model
    inp = inp.drop(USER_NAME_COLUMN, axis=1)
    out = out[USER_REPOS_COLUMN]
    # Convert the indices to multi hot-encoded vectors
    out = out.apply(lambda x: [int(i) for i in x.split(',')])
    out = MultiLabelBinarizer().fit_transform(out)

    # convert outputs from string to list
    print('INPUT')
    print(inp.shape)
    print('OUTPUT')
    print((len(out), len(out[0])))
    # Get input and output sizes
    num_inputs = len(inp.columns)
    num_repos = len(out[0])
    # Build the model and train it!
    print('TRAINING')
    rec = NeuralRecommender(input_size=num_inputs, output_size=num_repos)
    rec.train(inp.values, out)
    # Save the weights
    rec.save()

if __name__ == "__main__":
    create_model()
    
