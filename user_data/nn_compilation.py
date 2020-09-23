import pandas as pd
from OpenSource.general import NN_OUTPUT, REPO_FILE, USER_FILE, USER_LIST, NAME_COLUMN

def encode_indices(indices: iter) -> list:
    vect = str(indices.pop(0))
    for index in indices:
        vect += f',{index}'
    return vect

def encode_NN_output(user_file=USER_LIST, repo_file=REPO_FILE, new_file=NN_OUTPUT):
    user_data = pd.read_csv(user_file)['user']
    repos = pd.read_csv(repo_file)[NAME_COLUMN].unique()

    # Encoded repos into indices
    repo_translation = {repo: i for i, repo in enumerate(repos)}

    repos_encoded = {}
    for user, user_repos in zip(user_data.index, user_data['repos']):
        user_repos = user_repos.split(',')
        # Convert the repos to indices
        user_repos = [repo_translation[r] for r in user_repos]
        user_repos = encode_indices(user_repos)
        repos_encoded[user] = user_repos

    final_df = pd.DataFrame.from_dict(repos_encoded, orient='index')
    # Rename the column
    final_df.columns = ['repo_encoded'] 
    # Save
    final_df.to_csv(new_file)
    print(final_df.head())




if __name__ == "__main__":
    encode_NN_output()