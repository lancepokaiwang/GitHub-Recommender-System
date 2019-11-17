import datetime

import Basic_Functions as bfs

# GitHub API oAuth
CLIENT_ID = "6aca4b66775c629cbafd"
CLIENT_SECRET = "2349a0a9266e81f9f4d7df62ca49a98ca357b20c"

OWNER = "symfony"
REPO = "symfony"

users = bfs.readJsonFile(name="users_{}".format(REPO), folder="data")
issues = bfs.readJsonFile(name="all_issues_{}".format(REPO), folder="data")


def get_user_earliest_time(user_row=None):
    earliest = datetime.datetime.strptime("2100-12-31", '%Y-%m-%d')

    # search commit comments
    for item in user_row["commit_comments"]:
        if "{}/{}".format(OWNER, REPO) in item["url"]:
            time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
            if (time - earliest).days < 0:
                earliest = time

    # search commits
    for item in user_row["commits"]:
        if "{}/{}".format(OWNER, REPO) in item["url"]:
            time = datetime.datetime.strptime(str(item["commit"]["committer"]["date"])[0:10], '%Y-%m-%d')
            if (time - earliest).days < 0:
                earliest = time

    # search issue comments
    for item in user_row["issue_comments"]:
        if item["repo"] == REPO and item["owner"] == OWNER:
            time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
            if (time - earliest).days < 0:
                earliest = time

    # search issue events
    for item in user_row["issue_events"]:
        if item["repo"] == REPO and item["owner"] == OWNER:
            time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
            if (time - earliest).days < 0:
                earliest = time

    # search issues
    for item in user_row["issues"]:
        if item["repo"] == REPO and item["owner"] == OWNER:
            time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
            if (time - earliest).days < 0:
                earliest = time

    # search pr comments
    for item in user_row["pr_comments"]:
        if item["repo"] == REPO and item["owner"] == OWNER:
            time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
            if (time - earliest).days < 0:
                earliest = time

    # search prs
    for item in user_row["prs"]:
        if item["repo"] == REPO and item["owner"] == OWNER:
            time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
            if (time - earliest).days < 0:
                earliest = time

    return earliest


def generate_user_columns(user_row=None, issue_create_date=None, earliest_date=None):
    issue_create_date = datetime.datetime.strptime(issue_create_date, '%Y-%m-%d')
    # earliest_date = datetime.datetime.strptime(earliest_date, '%Y-%m-%d')

    user = {"age": (issue_create_date - earliest_date).days, "repos": 0, "commit_comments": 0, "commits": 0,
            "issue_comments": 0, "issue_events": 0, "issues": 0, "pr_comments": 0, "prs": 0}

    # search repos
    for item in user_row["repos"]:
        time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
        if time < issue_create_date:
            user["repos"] += 1

    # search commit comments
    for item in user_row["commit_comments"]:
        time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
        if time < issue_create_date:
            user["commit_comments"] += 1

    # search commits
    for item in user_row["commits"]:
        time = datetime.datetime.strptime(str(item["commit"]["committer"]["date"])[0:10], '%Y-%m-%d')
        if time < issue_create_date:
            user["commits"] += 1

    # search issue comments
    for item in user_row["issue_comments"]:
        time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
        if time < issue_create_date:
            user["issue_comments"] += 1

    # search issue events
    for item in user_row["issue_events"]:
        time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
        if time < issue_create_date:
            user["issue_events"] += 1

    # search issues
    for item in user_row["issues"]:
        time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
        if time < issue_create_date:
            user["issues"] += 1

    # search pr comments
    for item in user_row["pr_comments"]:
        time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
        if time < issue_create_date:
            user["pr_comments"] += 1

    # search prs
    for item in user_row["prs"]:
        time = datetime.datetime.strptime(str(item["created_at"])[0:10], '%Y-%m-%d')
        if time < issue_create_date:
            user["prs"] += 1

    return user


# Search all issues
filtered_users = []
for issue in issues:

    create_date = str(issue["issue"]["created_at"])[0:10]
    # If issue has pull request
    if issue["pull_request"] is not None:
        earliest_time = get_user_earliest_time(users[str(issue["pull_request"]["user"]["id"])])
        print(earliest_time)
        filtered_users.append(generate_user_columns(user_row=users[str(issue["pull_request"]["user"]["id"])], issue_create_date=create_date, earliest_date=earliest_time))
    # If issue has commits
    if issue["pull_commits"]:
        for pull_commit in issue["pull_commits"]:
            earliest_time = get_user_earliest_time(users[str(pull_commit["committer"]["id"])])
            print(earliest_time)
            filtered_users.append(generate_user_columns(user_row=users[str(pull_commit["committer"]["id"])], issue_create_date=create_date, earliest_date=earliest_time))

bfs.writeJsonFile(data=filtered_users, name="users_{}_filtered".format(REPO), folder="data")
