import pandas as pd
from tqdm import tqdm
from OpenSource.general import REPO_FILE, REPO_TO_USER_FILE, CONTRIBUTORS_COLUMN

# Move from repo rows to user rows
def repos_to_users(repo_file=REPO_FILE, new_file=REPO_TO_USER_FILE, user_col=CONTRIBUTORS_COLUMN):
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
    # Normalize language strengths
    # for _, user in tqdm(user_data.iterrows()):
    #     nums = user.drop('repos')
    #     total = sum(user.drop('repos'))
    #     nums /= total
    
    user_data.to_csv(new_file)
    print(user_data.head())
    

if __name__ == "__main__":
    repos_to_users()