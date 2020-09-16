from pull_users import append_contributors
from data_cleaning import init_clean, append_activity, remove_inactive


if __name__ == "__main__":
    init_clean()
    append_activity()
    remove_inactive()
    append_contributors()