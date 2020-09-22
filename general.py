import requests
import json
from time import sleep

REPO_FILE = 'storage/pulled_repos.csv'
USER_LIST = 'storage/repo_users.csv'
USER_FILE = 'storage/pulled_users_info.csv'
SECRET_FILE = 'storage/secrets.json'

CONTRIBUTORS_COLUMN = 'contributors'

with open(SECRET_FILE) as f:
    secrets = json.load(f)

def pull_json(link, query=None, headers=None, redo=False, delay=30):
    # Initiate the request
    r = requests.get(link, query, headers=headers, auth=('user', secrets['token']))
    # Make sure data is okay
    if redo:
        # Try again a few times
        timeout = 3
        while (not r.ok and timeout):
            print(link)
            sleep(delay)
            r = requests.get(link, query, headers=headers, auth=('user', secrets['token']))
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


def git_api_status(stype='core'):
    response = pull_json('https://api.github.com/rate_limit')
    return response['resources'][stype]


if __name__ == '__main__':
    print(git_api_status())