import pandas as pd
from tqdm import tqdm
from OpenSource.general import REPO_FILE, USER_LIST, CONTRIBUTORS_COLUMN, NAME_COLUMN

# * Make a list of users and repos 
def repos_to_users(repo_file=REPO_FILE, new_file=USER_LIST, user_col=CONTRIBUTORS_COLUMN, name_col=NAME_COLUMN):
    df = pd.read_csv(repo_file)

    user_data = {'user': [], name_col: [], 'language': []}
    for _, repo in df.iterrows():
        repo_lang = repo['language']
        repo_name = repo[name_col]
        repo_users = repo[user_col].split(',')
        # Add a row that with the user and the repo
        for user in repo_users:
            user_data['user'].append(user)
            user_data[name_col].append(repo_name)
            user_data['language'].append(repo_lang)
    # Create and store dataframe
    user_data = pd.DataFrame(user_data)
    user_data.drop_duplicates(inplace=True)
    
    user_data.to_csv(new_file)
    print(user_data.head())
    
    # Create a string of repos for each user
    # user_repos = user_data.groupby('user')['repo_name'].apply(lambda x: ','.join(x))

if __name__ == "__main__":
    repos_to_users()