# Pulls data from the BigQuery 4TB dataset of GitHub at https://www.kaggle.com/github/github-repos
# * Create a kernel at https://www.kaggle.com/mrisdal/safely-analyzing-github-projects-popular-licenses
# ! Don't run this code here! Do it at the kernel!

import pandas as pd
from bq_helper import BigQueryHelper
bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")

QUERY = """
        SELECT author, subject, repo_name
        FROM `bigquery-public-data.github_repos.commits`
        LIMIT 250000
        """

print(f"Using {bq_assistant.estimate_query_size(QUERY)} GB / 5 TB Limit")

df = bq_assistant.query_to_pandas_safe(QUERY, max_gb_scanned=125)
print(df.head())
print(f'Size of dataframe: {int(df.memory_usage(index=True, deep=True).sum()) / 2**20} MB')

df.to_csv('commits.csv')