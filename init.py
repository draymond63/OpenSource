from repo_data.pull_repos import get_repo_data
from repo_data.data_cleaning import remove_inactive
from repo_data.pull_users import append_contributors

from user_data.repo_to_users import repos_to_users
from user_data.pull_user_data import pull_user_data
from user_data.nn_compilation import encode_NN_output
from recommend.nn_recommender import create_model

GATHER_REPO_INFO = True
REPO_TO_USER_INFO = True
GATHER_USER_INFO = True
TRAIN_NN = False

if __name__ == "__main__":
    if GATHER_REPO_INFO:
        print('\nGET REPOS')
        get_repo_data()
        print('\nREMOVE INACTIVE')
        remove_inactive()
        print('\nGET CONTRIBUTORS')
        append_contributors()
    if REPO_TO_USER_INFO:
        print('\nMAKE USER LIST')
        repos_to_users()
    if GATHER_USER_INFO:
        print('\nPULL USER DATA')
        pull_user_data()
    if TRAIN_NN:
        encode_NN_output()
        create_model()
