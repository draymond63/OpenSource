import pandas as pd
import requests
import json
from time import sleep
from tqdm import tqdm

def pull_json(link, split=True):
    # Split on { because the url has a template bit at the end that we don't want
    if split:
        link = link.split('{')[0]
    # Initiate the request
    r = requests.get(link)
    if (r.ok): 
        sleep(1)
        return json.loads(r.content)
    else:
        print(link)
        raise RuntimeError(r.content)

def get_repo_info(repo):
    try:
        # Main request that gathers most of the info
        repoItem = pull_json(f'https://api.github.com/repos/{repo}')
        # Pull the issues if possible
        if repoItem['has_issues']:
            issues = pull_json(repoItem['issues_url'])
        else:
            issues = None
        # Labels has lots of useless info, we just want the names
        labels = pull_json(repoItem['labels_url'])
        labels = [x['name'] for x in labels]
        # Languages are in the json's keys
        langs = pull_json(repoItem['languages_url'], split=False)
        langs = list(langs.keys())

        return {
            'page': repoItem['html_url'],
            'description': repoItem['description'],
            'watchers': repoItem['watchers'],
            'main_lang': repoItem['language'],
            'languages': langs,
            'labels': labels,
            'issues': issues
        }
    except RuntimeError as e:
        print(e)
        return False

def get_user_info(user):
    try:
        # Main request that gathers most of the info
        userItem = pull_json(f'https://api.github.com/users')
        # # Pull the issues if possible
        print(userItem)
        
    except RuntimeError as e:
        print(e)
        return False


if __name__ == "__main__":
    # append_repo_info()
    # df = pd.read_csv('commits_cleaned.csv')
    get_user_info('Matthew Martin')

