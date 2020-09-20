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
            try:
                commits = len(pull_json(f'https://api.github.com/repos/{repo["full_name"]}/commits'))
                data[repo['language']] += commits
            except: pass
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
def pull_user_data(repo_file=REPO_TO_USER_FILE, user_file=USER_FILE, overwrite=False):
    # Get list of users and languages
    df = pd.read_csv(repo_file, index_col='Unnamed: 0')
    # Append the current file instead of overwritting it, if possible
    if isfile(user_file) and not overwrite:
        data = pd.read_csv(user_file, index_col='Unnamed: 0')
        users = [x for x in list(df.index) if x not in list(data.index)]
    else:
        users = list(df.index)
    langs = list(df.drop('repos', axis=1).columns)
    # Pull all the data
    new_data = get_users(users, langs)
    # Add the user's repos
    new_data = pd.DataFrame.from_dict(new_data, orient='index')
    new_data = new_data.join(df.loc[:, 'repos'])
    # Append the data if possible
    if isfile(user_file): 
        new_data = pd.concat([data, new_data])
    # Save the data
    new_data.to_csv(user_file)

def seriesSum(s):
    total = 0
    for element in s:
        if isinstance(element, float):
            total += element
    return total

def normalize_user_data(user_file=USER_FILE):
    df = pd.read_csv(user_file, index_col='Unnamed: 0')
    # * Normalize language strengths
    df = df[df.apply(lambda x: True if seriesSum(x) else False, axis=1)]
    data = df.drop('repos', axis=1)
    count = {}
    for i, user in data.iterrows():
        count[i] = user.sum()
        data.loc[i] = user.div(count[i])
    # Reattach the repos and counts
    count = pd.Series(count, name='repo_count')
    data = data.join(count)
    data = data.join(df['repos'])
    print(data.head())


if __name__ == "__main__":
    # pull_user_data()
    normalize_user_data()

    # MESSED UP https://api.github.com/repos/AArnott/Clue/commits