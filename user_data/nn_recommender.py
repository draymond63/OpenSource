from OpenSource.general import pull_json

r = pull_json(f'https://api.github.com/rate_limit')
print(r)