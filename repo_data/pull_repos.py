from OpenSource.general import pull_json, REPO_FILE, REPO_NAME_COLUMN
from tqdm import tqdm
import pandas as pd

# * Example
# https://api.github.com/search/repositories?q=Python+good-first-issues:>=50&per_page:1&sort:forks
# * Info
# https://docs.github.com/en/github/searching-fnformation-on-github/searching-for-repositories
# https://docs.github.com/en/rest/reference/search#search-repositories
def get_repo_query(key, language=None, forks='>=200', pushed='>=2020-09-01', help_wanted_issues='>=0', good_first_issues='>=1', sort='forks', per_page=1000):
    q_args = {
        'good-first-issues': good_first_issues,
        'help-wanted-issues': help_wanted_issues,
        'forks': forks,
        'archived': 'false', # This should be in quotes so it's included in the body
        'pushed': pushed,
        'language': language,
    }
    q_req = f'q={key}'

    for arg in q_args:
        if q_args[arg]:
            q_req += f'+{arg}:{q_args[arg]}'
    
    body = f'{q_req}&per_page:{per_page}&sort:{sort}'
    response = pull_json(f"https://api.github.com/search/repositories?{body}", headers={'Accept': 'application/vnd.github.v3+json'})

    # Extract useful info
    if response:
        data = {}
        for repo in response['items']:
            data[repo['full_name']] = {
                'html_url': repo['html_url'],
                'language': repo['language'] if repo['language'] else (language if language else key),
                'last_active': repo['pushed_at']
            }
        return data
    else:
        raise Warning(f'response was faulty - "{response}"')

def get_repo_data(repo_file=REPO_FILE):
    langs = [
        'JavaScript', 'Python', 'HTML', 'CSS', 'C++', 
        'TypeScript', 'Rust', 'Scheme', 'Java',  
        'Kotlin', 'C#', 'Perl', 'PHP', 'Scala', 
        'Swift', 'MATLAB', 'SQL', 'R', 'Go', 'Ruby',
        'Hascal'
    ]
    # Iterate through the languages, pulling in the data
    data = {}
    for lang in tqdm(langs):
        r = get_repo_query(lang)
        data.update(r)

    data = pd.DataFrame.from_dict(data, orient='index')
    # Shift the index to a regular column
    data.reset_index(inplace=True)
    data.rename(columns={'index': REPO_NAME_COLUMN}, inplace=True)
    print(data.head())
    data.to_csv(repo_file, index=False)

if __name__ == "__main__":
    get_repo_data()

    r = get_repo_query('Python', help_wanted_issues=None)
    print(r)
