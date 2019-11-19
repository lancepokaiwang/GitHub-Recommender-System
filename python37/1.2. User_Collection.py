import pymongo
import requests
import urllib3
import Basic_Functions as bfs

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# MongoDB construction
mg_client = pymongo.MongoClient("mongodb://localhost:27017/")
mg_db = mg_client["msr14"]

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
                return users
        if data["pull_commits"]:
            for pull_commit in data["pull_commits"]:
                if pull_commit["committer"] is not None:
                    if pull_commit["committer"]["id"] not in users:
                        users[pull_commit["author"]["id"]] = get_user_full_data(user_id=pull_commit["author"]["id"])
                        print("User: {} has been created!".format(pull_commit["committer"]["id"]))
                        # break
                        return users
    return users


def get_user_full_data(user_id=0):
    user_master = {}
    # Get user basic profile
    user_profile = mg_db["users"].find_one({"id": user_id}, {"_id": 0})
    # user_master["login"] = user_profile["login"]
    user_master["profile"] = user_profile

    # Get user repos
    repos = []
    user_repos = mg_db["repos"].find({"owner.id": user_id})
    for repo in user_repos:
        del repo["_id"]
        repos.append(repo)
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
    user_commit_comments = mg_db["commit_comments"].find({"user.id": user_id})
    for commit_comment in user_commit_comments:
        del commit_comment["_id"]
        del commit_comment["body"]
        # commit_comment["body"] = str(commit_comment["body"]).replace("\"", "")
        commit_comments.append(commit_comment)
    user_master["commit_comments"] = commit_comments

    # Get user commits
    commits = []
    user_commits = mg_db["commits"].find({"committer.id": user_id})
    for commit in user_commits:
        # Delete All Changed Files Information
        del commit["_id"]
        del commit["files"]
        del commit["author"]
        del commit["stats"]
        del commit["parents"]
        del commit["commit"]["message"]
        commits.append(commit)
    user_master["commits"] = commits

    # Get user issue comments
    issue_comments = []
    user_issue_comments = mg_db["issue_comments"].find({"user.id": user_id})
    for issue_comment in user_issue_comments:
        del issue_comment["_id"]
        del issue_comment["body"]
        # issue_comment["body"] = str(issue_comment["body"]).replace("\"", "")
        issue_comments.append(issue_comment)
    user_master["issue_comments"] = issue_comments

    # Get user issue events
    issue_events = []
    user_issue_events = mg_db["issue_events"].find({"actor.id": user_id})
    for issue_event in user_issue_events:
        del issue_event["_id"]
        issue_events.append(issue_event)
    user_master["issue_events"] = issue_events

    # Get user issues
    issues = []
    user_issues = mg_db["issues"].find({"user.id": user_id})
    for issue in user_issues:
        del issue["_id"]
        del issue["title"]
        del issue["body"]
        # issue["title"] = str(issue["title"]).replace("\"", "")
        # issue["body"] = str(issue["body"]).replace("\"", "")
        issues.append(issue)
    user_master["issues"] = issues

    # Get user pr comments
    pr_comments = []
    user_pr_comments = mg_db["pull_request_comments"].find({"user.id": user_id})
    for pr_comment in user_pr_comments:
        # pr_comment["body"] = str(pr_comment["body"]).replace("\"", "")
        del pr_comment["_id"]
        del pr_comment["_links"]
        del pr_comment["body"]
        del pr_comment["diff_hunk"]
        pr_comments.append(pr_comment)
    user_master["pr_comments"] = pr_comments

    # Get user prs
    prs = []
    user_prs = mg_db["pull_requests"].find({"user.id": user_id})
    for pr in user_prs:
        del pr["_id"]
        del pr["head"]
        del pr["_links"]
        del pr["title"]
        del pr["body"]
        # pr["title"] = str(pr["title"]).replace("\"", "")
        # pr["body"] = str(pr["body"]).replace("\"", "")
        prs.append(pr)
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

bfs.writeJsonFile(data=users_dataset, name="users_{}_test".format(REPO), folder="data")
