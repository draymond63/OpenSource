import pandas as pd
from tqdm import tqdm
from OpenSource.general import REPO_FILE, USER_LIST, CONTRIBUTORS_COLUMN

# * Move from repo rows to user rows
def repos_to_users(repo_file=REPO_FILE, new_file=USER_LIST, user_col=CONTRIBUTORS_COLUMN):
    df = pd.read_csv(repo_file)

    # Gather list of languages
    languages = df['language'].unique()
    
    user_data = {}
    for _, repo in df.iterrows():
        lang = repo['language']
        repo_name = repo['repo_name']
        repo_users = repo[user_col].split(',')
        for user in repo_users:
            # Add a user to the database
            if user not in user_data:
                user_data[user] = {l: 0 for l in languages}
                user_data[user]['repos'] = repo_name
            # Add the repo to the user's list
            elif repo_name not in user_data[user]['repos']:
                user_data[user]['repos'] += ',' + repo_name
            # Increase the strength of the language for the user
            user_data[user][lang] += 1
    user_data = pd.DataFrame.from_dict(user_data, orient='index')
    
    # * Normalize language strengths
    data = user_data.drop('repos', axis=1)
    count = {}
    for i, user in data.iterrows():
        count[i] = user.sum()
        data.loc[i] = user.div(count[i])
    # Reattach the repos and counts
    count = pd.Series(count, name='repo_count')
    data = data.join(count)
    data = data.join(user_data['repos'])

    # data.to_csv(new_file)
    print(data.head())
    

if __name__ == "__main__":
    repos_to_users()