import pandas as pd
import ast

def clean_data(df='../commits.csv', new_file='commits_cleaned.csv', repo_freq=3):
    print('\nCLEANING THE DATA FROM GITHUB')
    # Read file in if it is a file name
    if isinstance(df, str):
        df = pd.read_csv(df)
    print(df.shape)

    # * Break apart the author dict into its keys:
    # name, email, time_sec, tz_ffset, date{seconds, nanos}
    author_commits = {
        'author': [],
        'time_stamp': []
    }
    for entry in df['author']:
        # Each entry has been pickled!
        try:
            entry = ast.literal_eval(entry)
            # Copy over the name
            author_commits['author'].append(entry['name'])
            # Copy over the date
            ts = entry['date']['seconds']
            author_commits['time_stamp'].append(ts)                
        except:
            author_commits['author'].append(None)
            author_commits['time_stamp'].append(None)
            print("Bad author dict: ", entry)
    # Convert dict to df
    ac = pd.DataFrame(author_commits)
    # Replace the author column in the og df
    df.drop(['author', 'Unnamed: 0'], axis=1, inplace=True)
    df = df.join(ac)

    # * Convert the repo_name from a list to a single repo
    def convert_list(x):
        try: 
            return ast.literal_eval(x)[0]
        except: 
            print("Bad repo_name: ", x)
            return None
    df['repo_name'] = df['repo_name'].apply(convert_list)

    # * Last touches
    df.dropna(inplace=True)
    # Fix the date
    # Convert the days-seconds to date-days
    DATE_SHRINK_CONSTANT = 86400
    df['time_stamp'] = df['time_stamp'] / DATE_SHRINK_CONSTANT
    # Fix the date type and sort
    df = df.astype({'time_stamp': int})
    df.sort_values('time_stamp', ascending=False, inplace=True)
    # Remove repos that don't appear the often
    df = df[df.groupby('repo_name')['repo_name'].transform('count') >= repo_freq] 
    # Save the data
    df.to_csv(new_file, index=False)
    print(df.head())
    print(df.shape)

if __name__ == "__main__":
    clean_data()