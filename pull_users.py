import pandas as pd
from time import sleep
from tqdm import tqdm
from general import pull_json, url_to_repo, REPO_FILE

def get_contributors(repo_url, pause=0, ret_string=True):
    name = url_to_repo(repo_url)
    if not name:
        return None
    # Make the request
    repoItem = pull_json(f'https://api.github.com/repos/{name}/contributors')
    # Optional wait
    sleep(pause)
    # Make sure there is actually data to parse
    if repoItem:
        # Get the user ids
        users = [x['login'] for x in repoItem]
        return ",".join(users) if ret_string else users
    else:
        return None

# * Takes approximately seven minutes
def append_contributors(repo_file=REPO_FILE):
    df = pd.read_csv(repo_file)
    # Iterate through the repos, getting the contributors
    contributors = [get_contributors(url) for url in tqdm(df['repository_url'])]
    # Merge in the new data
    contributors = pd.Series(contributors, name='contributors')
    df = df.join(contributors)
    df.to_csv(repo_file, index=False)
   

if __name__ == "__main__":
    append_contributors()