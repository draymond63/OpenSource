import pandas as pd
from tqdm import tqdm
from math import log
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

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

# * A function analogous to tfidf (but for users and repos instead of terms and docs)
# tfidf ==> "user frequency inverse repo frequency"
# https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Definition
def ufirf(df, user, repo, num_repos=None):
    # Only useful data in the dataframe
    user_commits = df[df['author'] == user]
    # Raw count of a term (user) in a document (repo)
    user_repo_commits = user_commits['repo_name'][user_commits['repo_name'] == repo]
    # --> Number of documents (repos) where the term (user) appears
    user_docs = user_commits['repo_name'].nunique()
    # Calculate it if is isn't given
    if not num_repos:
        # Total number of documents (repos) in the corpus
        num_repos = df['repo_name'].nunique()
    # Log normalization term (user) frequency
    user_freq = log(1+len(user_repo_commits))
    # Smooth inverse document (repo) frequency
    inv_repo_freq = log(num_repos/(1+user_docs)) + 1
    return user_freq*inv_repo_freq

# ! Takes 17 minutes
# * Calculate ufirf for every user/repo pair
def freq_repos(df='commits_cleaned.csv', new_file='repo_vects.csv'):
    print('\nTFIDF REPOSITORIES ("user frequency inverse repo frequency")')
    # Read file in if it is a file name
    if isinstance(df, str):
        df = pd.read_csv(df)

    # Calculate ahead of time to increase speed
    num_repos = df['author'].nunique()
    vects = {}
    # Iterate through each repo
    repo_groups = df.groupby('author')
    for name, user in tqdm(repo_groups):
        # Make a list of user frequencies
        vects[name] = {}
        for repo in user['repo_name']:
            # Calculate the ufirf for the term/doc pair (user/repo)
            result = ufirf(df, repo, name, num_repos)
            if result:
                print(name, repo, result)
                vects[name][repo] = result
            if name == 'Stéphane Brunner' and repo == 'tsauerwein/c2cgeoportal':
                print(result)
    # Shape and save
    vects = pd.DataFrame(vects)
    vects.to_csv(new_file, index=False)
    print(vects.head())


if __name__ == "__main__":
    # pop_repos = find_popular_repos()
    # map_repos()
    freq_repos()
