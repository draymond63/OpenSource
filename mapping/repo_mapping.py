import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from tqdm import tqdm
from math import log

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

# (Positive) Pointwise mutual information --> log(p(a,b) / ( p(a) * p(b) ))
# * Standardizes the data in the matrix so that prevalence of a job doesn't affect things
def pmi_matrix(df: pd.DataFrame, positive=False) -> pd.DataFrame:
    # Convert matrix into probablities
    col_totals = df.sum(axis=0)
    total = col_totals.sum()
    row_totals = df.sum(axis=1)
    expected = np.outer(row_totals, col_totals) / total
    df = df / expected
    # Silence distracting warnings about log(0):
    with np.errstate(divide='ignore'):
        df = np.log(df)
    df[np.isinf(df)] = 0.0  # log(0) = 0
    # Set minimum to 0's
    if positive:
        df[df < 0] = 0.0
    return df

def map_repos(df='commits_cleaned.csv', new_file='mapping/repo_map.csv', space_dim=50):
    print('\nMAPPING REPOSITORIES')
    # Read file in if it is a file name
    if isinstance(df, str):
        df = pd.read_csv(df)

    # * Creating a huge matrix where each row is a job and each column is a coordinate
    # Initially each coordinate is the number of people that had both of those jobs
    repo_array = df['repo_name'].unique()
    repos = {key:i for i, key in enumerate(repo_array)}
    # Creat the initial 2D Matrix
    init_dim = len(repos)
    co_occerrence = np.zeros((init_dim, init_dim))

    # Iterate through each person in the group
    users = df.groupby('author')
    for _, user in tqdm(users):
        # Make sure they at least have two different jobs
        if user['repo_name'].nunique() > 1:
            # Make sure each job is in the cmap
            for repo1 in user['repo_name']:
                for repo2 in user['repo_name']:
                    coords = (repos[repo1], repos[repo2])
                    co_occerrence[coords] += 1
    co_occerrence = pd.DataFrame(co_occerrence)
    # Use PMI normalize the data
    rmap = pmi_matrix(co_occerrence)
    # Remove useless rows and columns
    rmap.dropna(how='all', axis=0, inplace=True)
    rmap.dropna(how='all', axis=1, inplace=True)

    # Join the title keys
    repo_array = pd.Series(repo_array, name='repo_name')
    # Drop the index before the merge because the indexing has changed
    rmap.reset_index(inplace=True, drop=True)
    rmap = rmap.join(repo_array)
    # Collapse matrix if requested
    if space_dim:
        # PCA works for higher dimensions than TSNE
        pca = PCA(n_components=space_dim, random_state=0)
        collapsed = pca.fit_transform(rmap.drop('repo_name', axis=1))
        # Use the new data as the columns
        collapsed = pd.DataFrame(collapsed)
        rmap = pd.merge(rmap['repo_name'], collapsed, left_index=True, right_index=True)

    # Save the data if requested
    if new_file:
        rmap.to_csv(new_file, index=False)    
    print(rmap.head())
    return rmap

# * Visualize the data
def display_map(rmap, html_file=None):
    # Read in the data if a filename is given
    if isinstance(rmap, str):
        rmap = pd.read_csv(rmap)
    print(f'{rmap.memory_usage(deep=True).sum() / 2**20} MB')

    # Slice data to be TSNE'd
    data = rmap.drop('repo_name', axis=1)
    # Reducing dimensions
    if len(data.columns) != 2:
        # Calculate new points
        tsne = TSNE(n_components=2, random_state=0, verbose=1)
        vecs = tsne.fit_transform(data)
        # Replace n-dimensional data with the 2D data
        data = pd.DataFrame(vecs)
        rmap = data.join(rmap['repo_name'])

    print(rmap.head())
    fig = px.scatter(rmap, 
        x=0, y=1,
        hover_name='repo_name',
        range_x=[-35, 35],
        range_y=[-30, 30],
        title='Careers Mapped in a 50-D Space and Clustered (Collapsed into 2-D)',
    )
    fig.show()
    if html_file:
        fig.write_html(html_file)

if __name__ == "__main__":
    # pop_repos = find_popular_repos()
    # rmap = map_repos()
    display_map('mapping/repo_map.csv')
    # freq_repos()
