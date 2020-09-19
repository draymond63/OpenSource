import pandas as pd
from tqdm import tqdm
from os.path import isfile
from OpenSource.general import pull_json, USER_FILE, REPO_TO_USER_FILE, CONTRIBUTORS_COLUMN

# * Get wanted data from user repo request
def extract_wanted(repos: list, langs: list) -> list:
    data = {l: 0 for l in langs}
    for repo in repos:
        if not repo['fork'] and repo['language'] in langs:
            # Pull in the number of commits for that repo
            commits = len(pull_json(f'https://api.github.com/repos/{repo["full_name"]}/commits'))
            data[repo['language']] += commits
    return data

def get_users(users, langs):
    user_data = {}
    # Get info on each user
    for user in tqdm(users):
        try:
            userItem = pull_json(f'https://api.github.com/users/{user}/repos') 
            user_data[user] = extract_wanted(userItem, langs)
        # Drop out early if there's an error
        except:
            print("SAVING EARLY")
            break
    return user_data

# * Creates a new dataset from the users in the repo file
def pull_user_data(repo_file=REPO_TO_USER_FILE, user_file=USER_FILE):
    # Get list of users and languages
    df = pd.read_csv(repo_file, index_col='Unnamed: 0')
    # Append the current file instead of overwritting it, if possible
    if isfile(user_file):
        data = pd.read_csv(user_file, index_col='Unnamed: 0')
        users = [x for x in list(df.index) if x not in list(data.index)]
    else:
        users = list(df.index)
    langs = list(df.drop('repos', axis=1).columns)
    # Pull all the data
    new_data = get_users(users, langs)
    # Add the user's repos
    new_data = pd.DataFrame.from_dict(new_data, orient='index')
    new_data = new_data.join(df['repos'])
    # Append the data if possible
    if isfile(user_file): 
        new_data = pd.concat([data, new_data])
    # Save the data
    new_data.to_csv(user_file)

if __name__ == "__main__":
    # pull_user_data()
    data = pd.read_csv(USER_FILE, index_col='Unnamed: 0')
    print(data.head())
    print(data.shape)