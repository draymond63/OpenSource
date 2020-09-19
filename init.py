from repo_data.data_cleaning import init_clean, append_activity, remove_inactive
from repo_data.pull_users import append_contributors

from user_data.repo_to_users import repos_to_users
from user_data.pull_user_data import pull_user_data
from user_data.nn_compilation import encode_NN_output
from recommend.nn_recommender import create_model

GATHER_REPO_INFO = True
REPO_TO_USER_INFO = True
GATHER_USER_INFO = False
TRAIN_NN = True

if __name__ == "__main__":
    if GATHER_REPO_INFO:
        init_clean()
        append_activity()
        remove_inactive()
        append_contributors()
    if REPO_TO_USER_INFO:
        repos_to_users()
        # nn_recommender
    if GATHER_USER_INFO:
        pull_user_data()
    if TRAIN_NN:
        encode_NN_output()
        create_model()
