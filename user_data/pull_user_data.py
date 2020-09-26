import pandas as pd
from tqdm import tqdm
from os.path import isfile
from OpenSource.general import pull_json, USER_FILE, USER_LIST, CONTRIBUTORS_COLUMN, NAME_COLUMN

# * Get wanted data from user repo request
def extract_wanted(repos: list, langs: list) -> list:
    data = {l: 0 for l in langs}
    for repo in repos:
        if not repo['fork'] and repo['language'] in langs:
            # Add the number of kilobytes (rough approximation for how much they've coded)
            data[repo['language']] += repo['size']
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
def pull_user_data(repo_info=USER_LIST, user_file=USER_FILE, overwrite=False):
    # Get list of users and languages
    df = pd.read_csv(repo_info)
    users = pd.Series(df['user'].unique(), name='user')
    langs = list(df['language'].unique())
    # Append the current file instead of overwritting it, if possible
    if isfile(user_file) and not overwrite:
        data = pd.read_csv(user_file)
        # Keep only entries where user is not already
        users = users[~users.isin(data['user'])]
    # Pull all the data
    new_data = get_users(users, langs)
    new_data = pd.DataFrame.from_dict(new_data, orient='index')
    # Turn users into a regular column
    new_data.reset_index(inplace=True)
    new_data.rename(columns={'index': 'user'}, inplace=True)
    # Create list of repos for each user
    user_repos = df.groupby('user')[NAME_COLUMN].apply(lambda x: ','.join(x))
    user_repos.rename('repos', inplace=True)
    new_data = pd.merge(new_data, user_repos, left_on='user', right_index=True)
    # Append the data if possible
    if isfile(user_file): 
        new_data = pd.concat([data, new_data])
    # Save the data
    print(new_data.head())
    new_data.to_csv(user_file, index=False)

def seriesSum(s):
    total = 0
    for element in s:
        if isinstance(element, float):
            total += element
    return total

def normalize_user_data(user_file=USER_FILE):
    df = pd.read_csv(user_file)
    # Drop all rows that have no data on the user
    df = df[df.apply(lambda x: True if seriesSum(x) else False, axis=1)]
    # * Normalize language strengths
    # ! user name is now a column, so it needs to be dropped
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
    # normalize_user_data()

    s = pd.Series([1, 2, 3])
    s.sum(numeric_only=True)

    # MESSED UP https://api.github.com/repos/AArnott/Clue/commits