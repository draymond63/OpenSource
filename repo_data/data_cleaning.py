import pandas as pd
import requests
from tqdm import tqdm
from OpenSource.general import pull_json, url_to_repo, DUMP_REPO_FILE, REPO_FILE

def init_clean(repo_file=DUMP_REPO_FILE, new_file=REPO_FILE):
    df = pd.read_csv(repo_file)
    if 'Unnamed: 0' in df:
        df.drop('Unnamed: 0', axis=1, inplace=True)
    df.to_csv(new_file, index=False)


def append_name(repo_file=REPO_FILE):
    df = pd.read_csv(repo_file)
    names = []
    for url in df['repository_url']:
        names.append(url_to_repo(url))
    # Append and save data
    names = pd.Series(names, name='repo_name')
    print(df.head())
    print(names.head())
    df = df.join(names)
    df.to_csv(repo_file, index=False)


def append_activity(repo_file=REPO_FILE):
    df = pd.read_csv(repo_file, index_col='Unnamed: 0')
    print(df['repo_name'].unique().shape)
    # Check each repo for activity
    last_active = {}
    for name in tqdm(df['repo_name'].unique()):
        if name:
            # Pull in the data and append it
            repoItem = pull_json(f'https://api.github.com/repos/{name}')
            if repoItem:
                # print('hello')
                last_active[name] = repoItem['pushed_at']
            else:
                last_active[name] = None
    # Append and save data
    last_active = pd.Series(last_active, name='last_active')
    df = pd.merge(df, last_active, left_on='repo_name', right_index=True)
    df.to_csv(repo_file, index=False)
    print(df.head())

def remove_inactive(repo_file=REPO_FILE, cutoff=(2020, 9)):
    df = pd.read_csv(repo_file)
    print(df.shape)
    # Keep only viable entries
    df = df[df['last_active'].map(type) == str]

    # Keep only year and month form last-active column
    df['last_active'] = df['last_active'].apply(lambda x: x[:7])
    # Last update must be at least May 2020 (x[:4] == year and x[5:] == month)
    df = df[[(int(x[:4]) >= cutoff[0] and int(x[5:]) >= cutoff[1]) for x in df['last_active']]]
    print(df.head(2))
    print(df.shape)
    df.to_csv(repo_file, index=False)

if __name__ == "__main__":
    init_clean()
    append_name()
    append_activity()
    remove_inactive()