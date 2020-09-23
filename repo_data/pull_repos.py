from OpenSource.general import pull_json, REPO_FILE, NAME_COLUMN
from tqdm import tqdm
import pandas as pd

# https://docs.github.com/en/github/searching-fnformation-on-github/searching-for-repositories
# https://docs.github.com/en/rest/reference/search#search-repositories
def get_repo_query(key, language=None, forks='>=200', sort='forks', pushed='>=2020-09-01', help_wanted_issues='>=5', good_first_issues='>=5', per_page=1000):   
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
                'language': repo['language'] if repo['language'] else (language if language else key),
                'last_active': repo['pushed_at']
            }
        return data
    else:
        raise Warning(f'response was faulty: {response}')

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
    data.rename(columns={'index': NAME_COLUMN}, inplace=True)
    print(data.head())
    data.to_csv(repo_file, index=False)

if __name__ == "__main__":
    get_repo_data()
