import pandas as pd
import requests
import json

def pull_json(link):
    r = requests.get(link)
    if (r.ok): 
        return json.loads(r.content)
    raise RuntimeWarning(f'Link was not okay: {link}')

def get_info(repo):
    repoItem = pull_json(f'https://api.github.com/repos/{repo}')
    user_url = repoItem['html_url']
    desc = repoItem['description']
    watchers = repoItem['watchers']

    tags = pull_json(repoItem['tags_url'].split('{')[0])
    labels = pull_json(repoItem['labels_url'].split('{')[0])
    labels = [x['name'] for x in labels]

    langs = pull_json(repoItem['languages_url'])
    langs = list(langs.keys())


    # labels_url, clone_url, watchers, language, has_issues, has_wiki, archived, 

    return {
        'page': user_url,
        'description': desc,
        'tags': tags,
        'languages': langs,
        'watchers': watchers,
        'labels': labels
    }


def test():
    test_repos = [
        # 'chromium/chromium',
        # 'apple/llvm-project',
        # 'jrfastab/hardware_maps',
        # 'Pingmin/linux',
        # 'dwindsor/linux-next',
        # 'xorware/android_frameworks_base',
        # 'jrobhoward/SCADAbase',
        'linux-rockchip/linux-rockchip',
        # 'GuoqingJiang/SLE12-clustermd',
    ]

    for repo in test_repos:
        data = get_info(repo)
        print(data)

def append_repo_info(df='../commits_cleaned.csv'):
    if isinstance(df, str):
        df = pd.read_csv(df)


if __name__ == "__main__":
    test()

