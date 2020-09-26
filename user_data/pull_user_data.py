import pandas as pd
from tqdm import tqdm
from os.path import isfile
from OpenSource.general import pull_json, USER_FILE, USER_LIST, CONTRIBUTORS_COLUMN, REPO_NAME_COLUMN, USER_REPOS_COLUMN, USER_NAME_COLUMN

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
    users = pd.Series(df[USER_NAME_COLUMN].unique(), name=USER_NAME_COLUMN)
    langs = list(df['language'].unique())
    # Append the current file instead of overwritting it, if possible
    if isfile(user_file) and not overwrite:
        data = pd.read_csv(user_file)
        # Keep only entries where user is not already
        users = users[~users.isin(data[USER_NAME_COLUMN])]
    # Pull all the data
    new_data = get_users(users, langs)
    new_data = pd.DataFrame.from_dict(new_data, orient='index')
    # Turn users into a regular column
    new_data.reset_index(inplace=True)
    new_data.rename(columns={'index': USER_NAME_COLUMN}, inplace=True)
    # Create list of repos for each user
    user_repos = df.groupby(USER_NAME_COLUMN)[REPO_NAME_COLUMN].apply(lambda x: ','.join(x))
    user_repos.rename(USER_REPOS_COLUMN, inplace=True)
    new_data = pd.merge(new_data, user_repos, left_on=USER_NAME_COLUMN, right_index=True)
    # Append the data if possible
    if isfile(user_file): 
        new_data = pd.concat([data, new_data])
    # Save the data
    print(new_data.head())
    new_data.to_csv(user_file, index=False)


# * Normalization of data
def normalize_user_data(user_file=USER_FILE):
    df = pd.read_csv(user_file)
    data = df.drop([USER_REPOS_COLUMN, USER_NAME_COLUMN], axis=1)
    # Drop all rows that have no data on the user
    df = df[data.sum(axis=1) != 0]

    # Normalize language strengths
    count = {}
    for i, user in data.iterrows():
        count[i] = user.sum()
        data.loc[i] = user.div(count[i])
    # Normalize total repo across users
    count = pd.Series(count, name='repo_total')
    print("Repo Max:", count.max()) # 12594379 KB
    count /= count.max()

    # Reattach the repos and counts
    data = data.join(count)
    data = data.join(df[USER_REPOS_COLUMN])
    print(data.head())
    data.to_csv(USER_FILE, index=False)

if __name__ == "__main__":
    # pull_user_data()
    normalize_user_data()