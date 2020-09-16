import pandas as pd
from time import sleep
from tqdm import tqdm
from general import pull_json, REPO_FILE, CONTRIBUTORS_COLUMN

def get_contributors(repo_name, pause=0, ret_string=True):
    if not repo_name:
        return None
    # Make the request
    try: repoItem = pull_json(f'https://api.github.com/repos/{repo_name}/contributors')
    except: return None
    # Optional wait
    sleep(pause)
    # Make sure there is actually data to parse
    if repoItem:
        # Get the user ids
        users = [x['login'] for x in repoItem]
        return ",".join(users) if ret_string else users
    else:
        return None

# * Takes approximately 7-8 minutes
def append_contributors(repo_file=REPO_FILE):
    df = pd.read_csv(repo_file)
    # Iterate through the repos, getting the contributors
    contributors = [get_contributors(url) for url in tqdm(df['repository_url'])]
    # Merge in the new data
    contributors = pd.Series(contributors, name=CONTRIBUTORS_COLUMN)
    df = df.join(contributors)
    df.dropna(subset=[CONTRIBUTORS_COLUMN], inplace=True)
    df.to_csv(repo_file, index=False)
    print(df.head())

if __name__ == "__main__":
    append_contributors()
