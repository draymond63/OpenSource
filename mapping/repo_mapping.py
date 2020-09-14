import pandas as pd

def find_popular_repos(df='commits_cleaned.csv'):
    print('\nMOST POPULAR REPOSITORIES BY THE NUMBER OF USERS')
    # Read file in if it is a file name
    if isinstance(df, str):
        df = pd.read_csv(df)

    print(df['repo_name'].nunique())
    # Group the data by repo
    repos = df.groupby('repo_name')
    count = {
        'repo_name': [],
        'users': []
    }
    # Count the users involved in each repo
    for name, repo in repos:
        count['repo_name'].append(name)
        count['users'].append(repo['author'].nunique())
    
    count = pd.DataFrame(count)
    count.sort_values('users', ascending=False, inplace=True)

    print(count['repo_name'].head(15))
    print(count.shape)
    return count

def map_repos(df='commits_cleaned.csv'):
    pass


if __name__ == "__main__":
    pop_repos = find_popular_repos()