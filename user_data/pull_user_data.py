import pandas as pd
from tqdm import tqdm
from OpenSource.general import pull_json, USER_FILE, REPO_FILE, CONTRIBUTORS_COLUMN

# * Returns a list of users involved in the REPOs file
def get_users_list(df, user_col=CONTRIBUTORS_COLUMN):
    users = []
    # Iterate through the repos
    for _, repo in df.iterrows():
        # Iterate through contributors in repo
        repo_users = repo[user_col].split(',')
        for user in repo_users:
            if user not in users:
                users.append(user)
    return pd.Series(users, dtype=object)

# * Creates a new dataset from the users in the repo file
def pull_user_data(repo_file=REPO_FILE, new_file=USER_FILE):
    users = get_users_list(pd.read_csv(repo_file))
    user_data = {}
    # Get info on each user
    for user in tqdm(users):
        userItem = pull_json(f'https://api.github.com/user/{user}')
        user_data[user] = userItem
    # Save data
    user_data = pd.DataFrame(user_data)
    user_data.to_csv(new_file)


if __name__ == "__main__":
    pull_user_data()