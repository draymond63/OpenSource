import pandas as pd
from OpenSource.general import NN_OUTPUT, REPO_FILE, USER_FILE, USER_LIST
from OpenSource.general import REPO_NAME_COLUMN, USER_NAME_COLUMN, USER_REPOS_COLUMN

def encode_indices(indices: iter) -> list:
    vect = str(indices.pop(0))
    for index in indices:
        vect += f',{index}'
    return vect

def encode_NN_output(user_file=USER_LIST, new_file=NN_OUTPUT):
    data = pd.read_csv(user_file)
    unique_repos = data[REPO_NAME_COLUMN].unique()

    # Encoded repos into indices
    repo_translation = {repo: i for i, repo in enumerate(unique_repos)}

    repos_encoded = {USER_NAME_COLUMN: [], USER_REPOS_COLUMN: []}
    # Iterate through the users
    for user, user_repos in data.groupby(USER_NAME_COLUMN):
        # Convert the repos to indices
        user_repos = user_repos[REPO_NAME_COLUMN] # Extract wanted column
        user_repos = [repo_translation[r] for r in user_repos] # Convert to indices
        user_repos = encode_indices(user_repos) # Stringify
        # Add the data
        repos_encoded[USER_NAME_COLUMN].append(user)
        repos_encoded[USER_REPOS_COLUMN].append(user_repos)

    # Save the data
    final_df = pd.DataFrame(repos_encoded)
    print(final_df.head())
    final_df.to_csv(new_file, index=False)


if __name__ == "__main__":
    encode_NN_output()