import pandas as pd
from OpenSource.general import pull_json, REPO_FILE

def remove_inactive(repo_file=REPO_FILE, cutoff=(2020, 9)):
    df = pd.read_csv(repo_file)
    print(df.shape)
    # Keep only viable entries
    df = df[df['last_active'].map(type) == str]

    # Keep only year and month form last-active column
    df['last_active'] = df['last_active'].apply(lambda x: x[:7])
    # Last update must be at least May 2020 (x[:4] == year and x[5:] == month)
    df = df[[(int(x[:4]) >= cutoff[0] and int(x[5:]) >= cutoff[1]) for x in df['last_active']]]
    print(df.head(2))
    print(df.shape)
    df.to_csv(repo_file, index=False)

if __name__ == "__main__":
    remove_inactive()