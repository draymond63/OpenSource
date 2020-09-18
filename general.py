import requests
import json
from time import sleep

DUMP_REPO_FILE = 'repos.csv'
REPO_FILE = 'repos_cleaned.csv'
REPO_TO_USER_FILE ='user_info.json'
USER_FILE = 'user_info.csv'
CONTRIBUTORS_COLUMN = 'contributors'

with open('secrets.json') as f:
    secrets = json.load(f)

def pull_json(link, redo=False, delay=30):
    # Initiate the request
    r = requests.get(link, auth=('user', secrets['token']))
    # Make sure data is okay
    if redo:
        # Try again a few times
        timeout = 3
        while (not r.ok and timeout):
            print(link)
            sleep(delay)
            r = requests.get(link, auth=('user', secrets['token']))
            timeout -= 1
        # Check if the timeout failed
        if timeout == 0:
            return None
    if r.ok:
        return json.loads(r.content)
    else:
        # Check the status
        status = git_api_status()
        if status['remaining'] == 0:
            raise AssertionError(f'Run out of requests, {status}')
        # If something else is wrong, then just return None
        print(link)
        return None

def url_to_repo(repo_url):
    # Extract name from the url
    if not isinstance(repo_url, str):
        return None
    # Try and take the ur-end, if not possible it's bad data
    try: name = repo_url.split('com/')[1]
    except: return None
    name = name.split('.git')[0]
    # Make sure there's only two values: user & repo
    if len(name.split('/')) != 2:
        print(name)
        return None
    return name

def git_api_status():
    response = pull_json('https://api.github.com/rate_limit')
    return response['resources']['core']


if __name__ == '__main__':
    print(git_api_status())