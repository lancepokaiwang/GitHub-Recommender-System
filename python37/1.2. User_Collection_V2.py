import pymongo
import requests
import urllib3
import Basic_Functions as bfs

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# MongoDB construction
mg_client = pymongo.MongoClient("mongodb://localhost:27017/")
mg_db = mg_client["msr14"]
mg_db.set_profiling_level(1)

# GitHub API oAuth
CLIENT_ID = "6aca4b66775c629cbafd"
CLIENT_SECRET = "2349a0a9266e81f9f4d7df62ca49a98ca357b20c"

OWNER = "symfony"
REPO = "symfony"


############## The difference between author and committer in commit ##############
# The author is the person who originally wrote the code. The committer,
# on the other hand, is assumed to be the person who committed the code
# on behalf of the original author. This is important in Git because Git
# allows you to rewrite history, or apply patches on behalf of another person.

# ==============Functions==============
def issue_analysis(issue_dataset=[]):
    users = {}
    for data in issue_dataset:
        if data["pull_request"] is not None:
            if data["pull_request"]["user"]["id"] not in users:
                users[data["pull_request"]["user"]["id"]] = get_user_full_data(
                    user_id=data["pull_request"]["user"]["id"])
                print("User: {} has been created!".format(data["pull_request"]["user"]["id"]))
                # break
                # return users
        if data["pull_commits"]:
            for pull_commit in data["pull_commits"]:
                if pull_commit["committer"] is not None:
                    if pull_commit["committer"]["id"] not in users:
                        users[pull_commit["author"]["id"]] = get_user_full_data(user_id=pull_commit["author"]["id"])
                        print("User: {} has been created!".format(pull_commit["committer"]["id"]))
                        # break
                        # return users
    return users


def get_user_full_data(user_id=0):
    user_master = {}
    # Get user basic profile
    user_profile = mg_db["users"].find_one({"id": user_id}, {"login": 1, "url": 1})
    user_master["profile"] = {
        "login": user_profile["login"],
        "url": user_profile["url"]
    }

    # Get user repos
    repos = []
    user_repos = mg_db["repos"].find({"owner.id": user_id}, {"url": 1, "created_at": 1})
    for repo in user_repos:
        repos.append({
            "url": repo["url"],
            "created_at": repo["created_at"][0:10]
        })
    user_master["repos"] = repos

    # # Get user followers
    # followers = []
    # user_followers = mg_db["followers"].find({"follows": user_profile["login"]}, {"_id": 0})
    # for follower in user_followers:
    #     followers.append(follower)
    # user_master["followers"] = followers

    # # Get user orgs
    # orgs = []
    # user_orgs = mg_db["org_members"].find({"id": user_id}, {"_id": 0})
    # for org in user_orgs:
    #     orgs.append(org)
    # user_master["orgs"] = orgs

    # Get user commit comments
    commit_comments = []
    user_commit_comments = mg_db["commit_comments"].find({"user.id": user_id}, {"url": 1, "created_at": 1})
    for commit_comment in user_commit_comments:
        commit_comments.append({
            "url": commit_comment["url"],
            "created_at": commit_comment["created_at"][0:10]
        })
    user_master["commit_comments"] = commit_comments

    # Get user commits
    commits = []
    user_commits = mg_db["commits"].find({"committer.id": user_id}, {"url": 1, "commit.committer.date": 1})
    for commit in user_commits:
        commits.append({
            "url": commit["url"],
            "created_at": commit["commit"]["committer"]["date"][0:10]
        })
    user_master["commits"] = commits

    # Get user issue comments
    issue_comments = []
    user_issue_comments = mg_db["issue_comments"].find({"user.id": user_id}, {"url": 1, "created_at": 1})
    for issue_comment in user_issue_comments:
        issue_comments.append({
            "url": issue_comment["url"],
            "created_at": issue_comment["created_at"][0:10]
        })
    user_master["issue_comments"] = issue_comments

    # Get user issue events
    issue_events = []
    user_issue_events = mg_db["issue_events"].find({"actor.id": user_id}, {"url": 1, "created_at": 1})
    for issue_event in user_issue_events:
        issue_events.append({
            "url": issue_event["url"],
            "created_at": issue_event["created_at"][0:10]
        })
    user_master["issue_events"] = issue_events

    # Get user issues
    issues = []
    user_issues = mg_db["issues"].find({"user.id": user_id}, {"url": 1, "created_at": 1})
    for issue in user_issues:
        issues.append({
            "url": issue["url"],
            "created_at": issue["created_at"][0:10]
        })
    user_master["issues"] = issues

    # Get user pr comments
    pr_comments = []
    user_pr_comments = mg_db["pull_request_comments"].find({"user.id": user_id}, {"url": 1, "created_at": 1})
    for pr_comment in user_pr_comments:
        pr_comments.append({
            "url": pr_comment["url"],
            "created_at": pr_comment["created_at"][0:10]
        })
    user_master["pr_comments"] = pr_comments

    # Get user prs
    prs = []
    user_prs = mg_db["pull_requests"].find({"user.id": user_id}, {"url": 1, "created_at": 1})
    for pr in user_prs:
        prs.append({
            "url": pr["url"],
            "created_at": pr["created_at"][0:10]
        })
    user_master["prs"] = prs

    # # Get user repo collaborators
    # repo_collaborators = []
    # user_repo_collaborators = mg_db["repo_collaborators"].find({"id": user_id}, {"_id": 0})
    # for repo_collaborator in user_repo_collaborators:
    #     repo_collaborators.append(repo_collaborator)
    # user_master["repo_collaborators"] = repo_collaborators

    # Return user data
    return user_master


# ==============Main==============
dataset = bfs.readJsonFile(name="all_issues_{}".format(REPO), folder="data")

users_dataset = issue_analysis(issue_dataset=dataset)

print(users_dataset)

bfs.writeJsonFile(data=users_dataset, name="users_{}_v2".format(REPO), folder="data")
