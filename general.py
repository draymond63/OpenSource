import requests
import json
from time import sleep

STR_PATH = './storage/'
REPO_FILE = STR_PATH + 'pulled_repos.csv'
USER_LIST = STR_PATH + 'repo_users.csv'
USER_FILE = STR_PATH + 'pulled_users_info-2.0.csv'
NN_OUTPUT = STR_PATH + 'nn_compl_output.csv'
SECRET_FILE = STR_PATH + 'secrets.json'

REPO_NAME_COLUMN = 'repo_name'
CONTRIBUTORS_COLUMN = 'contributors'
USER_REPOS_COLUMN = 'repos'
USER_NAME_COLUMN = 'user'

with open(SECRET_FILE) as f:
    secrets = json.load(f)

def pull_json(link, headers=None, redo=False, delay=30):
    # Initiate the request
    r = requests.get(link, headers=headers, auth=('user', secrets['token']))
    # Make sure data is okay
    if redo:
        # Try again a few times
        timeout = 3
        while (not r.ok and timeout):
            print(link)
            sleep(delay)
            r = requests.get(link, headers=headers, auth=('user', secrets['token']))
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