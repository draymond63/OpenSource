import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

from OpenSource.general import USER_LIST, USER_FILE, NN_OUTPUT, NN_WEIGHTS, LANG_MAXS
from OpenSource.general import REPO_NAME_COLUMN, USER_NAME_COLUMN, USER_REPOS_COLUMN
from OpenSource.user_data.pull_user_data import get_user

from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Hush the warnings
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense
from tensorflow.keras import Sequential
environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


class NeuralRecommender():
    # * TRAINING FUNCTIONS
    def __init__(self, input_size=50, output_size=100, metric='accuracy'):
        self.metric = metric
        # MODEL SHAPE
        self.model = Sequential([
            Dense(200, activation='tanh', input_shape=(input_size,)),
            Dense(1000, activation='tanh'),
            Dense(output_size, activation='sigmoid'),
        ])
        # MODEL PARAMS
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=[metric]
        )
        # SUMMARIZATION
        self.model.build()
        # self.model.summary()

    def train(self, i, o, epochs=100):
        callbacks = (
            EarlyStopping(patience=5, monitor=self.metric, restore_best_weights=True),
        )
        self.model.fit(i, o, 
            batch_size=64, 
            shuffle=True, 
            epochs=epochs,
            callbacks=callbacks
        )
    
    def test(self, i, o):
        self.model.evaluate(i, o)

    def save(self, file_name=NN_WEIGHTS):
        self.model.save_weights(file_name)

    # * USING FUNCTIONS
    def load(self, languages, repo_translation, maxs=LANG_MAXS, weights=NN_WEIGHTS):
        self.model.load_weights(weights)
        self.lang_maxs = pd.read_csv(maxs, index_col='Unnamed: 0', squeeze=True)
        self.langs = languages
        self.translate = repo_translation

    def suggest(self, user, top_n=5):
        assert not isinstance(self.langs, type(None)), 'Languages must be given in order to suggest'
        # Grab the data
        user_data = pd.Series(get_user(user, self.langs))
        # Normalize it
        user_data = user_data.divide(self.lang_maxs)
        # Get the probability vector
        result = self.model(user_data) # ! THIS IS BROKEN
        # sort by value and return the indices
        rankings = sorted(range(len(result)), key=lambda k: result[k])
        # Go from asc to desc
        rankings = rankings[::-1]
        # Take top N suggestions
        rankings = rankings[:top_n]
        # Get the indices, sorted from best to worst
        repos = [self.translate[rank] for rank in rankings]
        return repos


def create_model(inp=USER_FILE, out=NN_OUTPUT, split=2000):
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
    # Split into training set and testing set
    x_train = inp[:-split].values
    y_train = out[:-split]
    x_test = inp[-split:]
    y_test = out[-split:]

    # Build the model and train it!
    print('TRAINING')
    rec = NeuralRecommender(input_size=num_inputs, output_size=num_repos)
    rec.train(x_train, y_train)
    rec.test(x_test, y_test)
    # Save the weights
    rec.save()


def use_model(user_list=USER_LIST):
    # Get languages
    data = pd.read_csv(user_list)
    langs = data['language'].unique()
    # Get repo translation
    unique_repos = data[REPO_NAME_COLUMN].unique()  # ! This gives len == 1059 instead of 1055

    rec = NeuralRecommender(input_size=len(langs) + 1, output_size=1055) # len(unique_repos)
    rec.load(langs, unique_repos)

    repos = rec.suggest('draymond63')
    print(repos)



if __name__ == "__main__":
    # create_model()
    use_model()
    
