from OpenSource.general import pull_json
from tqdm import tqdm
import pandas as pd

def get_repo_query(key, language=None, forks='>=200', sort='stars', pushed='>=2020-09-01', help_wanted_issues='>=5', good_first_issues='>=5', per_page=100):    
    q = {
        'q': key,
        'language': language,
        'sort': sort,
        'forks': forks,
        'fork': False,
        'archived': False,
        'pushed': pushed,
        'help-wanted-issues': help_wanted_issues,
        'good-first-issues': good_first_issues,
        'per_page': per_page
    }
    response = pull_json('https://api.github.com/search/repositories', query=q, headers={'Accept': 'application/vnd.github.v3+json'})
    # Extract useful info
    if response:
        data = {}
        for repo in response['items']:
            data[repo['full_name']] = {
                'html_url': repo['html_url'],
                'language': language,
                'collaborators_url': repo['collaborators_url'].split('{')[0],
                'last_active': repo['pushed_at']
            }
        return data
    else:
        raise Warning(f'response was faulty: {response}')

def get_repo_data():
    langs = [
        'JavaScript', 'Python', 'HTML', 'CSS', 'C++', 
        'TypeScript', 'Rust', 'Scheme', 'Java',  
        'Kotlin', 'C#', 'Perl', 'PHP', 'Scala', 
        'Swift', 'MATLAB', 'SQL', 'R', 'Go', 'Ruby'
    ]

    data = {}
    for lang in tqdm(langs):
        r = get_repo_query(lang)
        data.update(r)

    data = pd.DataFrame.from_dict(data, orient='index')
    print(data.head())
    data.to_csv('storage/new_repos.csv')

if __name__ == "__main__":
    # get_repo_data()
    data = pd.read_csv('storage/new_repos.csv')
    print(data.head())
    print(data.shape)
