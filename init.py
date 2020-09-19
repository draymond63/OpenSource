from repo_data.data_cleaning import init_clean, append_activity, remove_inactive
from repo_data.pull_users import append_contributors
from user_data.repo_to_users import repos_to_users
from user_data.pull_user_data import pull_user_data

GATHER_REPO_INFO = True
REPO_TO_USER_INFO = True
GATHER_USER_INFO = True

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