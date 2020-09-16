import pandas as pd
from general import REPO_FILE, CONTRIBUTORS_COLUMN

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

# Move from repo rows to user rows
def repos_to_users(repo_file=REPO_FILE, user_col=CONTRIBUTORS_COLUMN):
    df = pd.read_csv(repo_file)
    
    user_data = {}
    for _, repo in df.iterrows():
        lang = repo['language']
        repo_name = repo['repo_name']
        repo_users = repo[user_col].split(',')
        for user in repo_users:
            # Add a user to the database
            if user not in user_data:
                user_data[user] = {
                    'languages': {},
                    'repos': '',
                }
            c_user = user_data[user] # Reference for ease of use
            # Increase the strength of the language for the user
            if lang not in c_user['languages']:
                c_user['languages'][lang] = 1
            else:
                c_user['languages'][lang] += 1
            # Add the repo to the user's list
            if repo_name not in c_user['repos']:
                c_user['repos'] += repo_name + ','

    # Normalize language strengths
    for user in user_data.values():
        total = sum(user['languages'].values())
        # Divide by total contribution
        for lang in user['languages']:
            user['languages'][lang] /= total

    user_data = pd.DataFrame.from_dict(user_data, orient='index')
    user_data.to_json('user_info.json')
    print(user_data.head())
    # Print some notable statistics
    count = 0
    for l in user_data['languages']:
        count += len(l)
    print('Average # of Languages', count/len(user_data))
    count = 0
    for r in user_data['repos']:
        repos = r.split(',')
        count += len(repos)
    print('Average # of Repos', count/len(user_data))
    

if __name__ == "__main__":
    repos_to_users()