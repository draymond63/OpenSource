import pandas as pd
import requests
from tqdm import tqdm
from general import pull_json, url_to_repo, DUMP_REPO_FILE, REPO_FILE

def init_clean(repo_file=DUMP_REPO_FILE, new_file=REPO_FILE):
    df = pd.read_csv(repo_file)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.to_csv(new_file, index=False)

def append_activity(repo_file=REPO_FILE):
    df = pd.read_csv(repo_file)

    # Check each repo for activity
    last_active = []
    for url in tqdm(df['repository_url']):
        # Extract the name from the url
        name = url_to_repo(url)
        if name:
            # Pull in the data and append it
            repoItem = pull_json(f'https://api.github.com/repos/{name}')
            if repoItem:
                last_active.append(repoItem['updated_at'])
            else:
                last_active.append(None)
    # Append and save data
    last_active = pd.Series(last_active, name='last_active')
    df = df.join(last_active)
    df.to_csv(repo_file, index=False)
    print(df.head())

def remove_inactive(repo_file=REPO_FILE, cutoff=(2020, 5)):
    df = pd.read_csv(repo_file)
    print(df.shape)
    # Keep only viable entries
    df = df[df['last_active'].map(type) == str]

    # Keep only year and month form last-active column
    df['last_active'] = df['last_active'].apply(lambda x: x[:7])
    # Last update must be at least May 2020 (x[:4] == year and x[5:] == month)
    df = df[[(int(x[:4]) == cutoff[0] and int(x[5:]) > cutoff[1]) for x in df['last_active']]]
    print(df.head(2))
    print(df.shape)
    df.to_csv(repo_file)

if __name__ == "__main__":
    init_clean()
    append_activity()
    remove_inactive()