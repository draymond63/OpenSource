import pandas as pd
import requests
import json
from time import sleep
from tqdm import tqdm

def pull_json(link, redo=False):
    # Initiate the request
    r = requests.get(link)
    # Make sure data is okay
    if redo:
        timeout = 100
        while (not r.ok and timeout):
            r = requests.get(link)
            sleep(30)
            timeout -= 1
        # Check if the timeout failed
        if not timeout:
            raise RuntimeError(r.content)

    if (r.ok): 
        sleep(1)
        return json.loads(r.content)
    else:
        print(link)
        raise RuntimeError(r.content)


def get_contributors(repo_url, pause=0, ret_string=True):
    # Extract name from the url
    repo_name = repo_url.split('com/')[1]
    # Make the request
    repoItem = pull_json(f'https://api.github.com/repos/{repo_name}/contributors', redo=True)
    # Optional wait
    sleep(pause)
    # Get the user ids
    users = [x['login'] for x in repoItem]

    return ",".join(users) if ret_string else users


def append_contributors(repo_file='repos.csv', new_file='repos_cleaned.csv'):
    df = pd.read_csv(repo_file)
    # Iterate through the repos, getting the contributors
    contributors = [get_contributors(url, pause=2) for url in tqdm(df['repository_url'])]
    # Merge in the new data
    contributors = pd.Series(contributors, name='contributors')
    df = df.join(contributors)
    df.to_csv(new_file)
   

if __name__ == "__main__":
    append_contributors()