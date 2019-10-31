import datetime
import json
import urllib3
import requests
import pymongo

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GitHub API oAuth
CLIENT_ID = "6aca4b66775c629cbafd"
CLIENT_SECRET = "2349a0a9266e81f9f4d7df62ca49a98ca357b20c"

# MongoDB construction
mg_client = pymongo.MongoClient("mongodb://localhost:27017/")
mg_db = mg_client["msr14"]


# ==============Functions==============
def getIssueData():
    dataset = []

    # Find all CLOSED issues from symfony
    issues = mg_db["issues"]
    for issue in issues.find({"repo": "symfony", "owner": "symfony", "state": "closed"}, {"_id": 0}):
        # Labels
        labels = []
        GO_ON = False
        for label in issue["labels"]:
            labels.append(label["name"])
            if label["name"] == "Bug" or label["name"] == "Easy Pick":
                GO_ON = True
        if GO_ON:
            # Data we need:
            issue_id = None
            assignees = []
            title = None
            body = None
            issue_comments = None
            pr_comments = None
            pr_review_comments = None
            committers = []
            changed_files = None
            issue_created_by = None
            pr_merged_by = None
            # issue_closed_by = None
            issue_closed_at = None
            # ====================Begin====================
            issue_object = {}
            # Get issue data from GitHub API
            issue_url = "https://api.github.com/repos/symfony/symfony/issues/{}?client_id={}&client_secret={}".format(
                issue["number"], CLIENT_ID, CLIENT_SECRET)
            print(issue_url)
            issue_online = requests.get(issue_url, verify=False).json()

            issue_id = issue_online["number"]
            title = str(issue_online["title"]).replace("\"", "”")
            body = str(issue_online["body"]).replace("\"", "”")
            issue_comments = issue_online["comments"]
            issue_created_by = issue_online["user"]["login"]
            # if issue_online["closed_by"] is not None:
            #     issue_closed_by = issue_online["closed_by"]["login"]
            issue_closed_at = str(issue_online["closed_at"])[0:10]

            # Assignees
            for assignee in issue_online["assignees"]:
                assignees.append(assignee["login"])

            # Get pull-request data from GitHub API
            if issue_online.get("pull_request", False):
                pr_url = "https://api.github.com/repos/symfony/symfony/pulls/{}?client_id={}&client_secret={}".format(
                    issue_online["number"], CLIENT_ID, CLIENT_SECRET)
                print(pr_url)
                pr_online = requests.get(pr_url, verify=False).json()

                pr_comments = pr_online["comments"]
                pr_review_comments = pr_online["review_comments"]
                changed_files = pr_online["changed_files"]
                if pr_online["merged_by"] is not None:
                    pr_merged_by = pr_online["merged_by"]["login"]

                # Get commits data from GitHub API
                if pr_online["commits_url"] is not None:
                    commits_url = pr_online["commits_url"] + "?client_id={}&client_secret={}".format(CLIENT_ID, CLIENT_SECRET)
                    print(commits_url)
                    commits_online = requests.get(commits_url, verify=False).json()

                    # Committers
                    for commit in commits_online:
                        committers.append(commit["commit"]["committer"]["name"])

            # Archive data
            issue_object["issue_id"] = issue_id
            issue_object["assignees"] = assignees
            issue_object["title"] = title
            issue_object["body"] = body
            issue_object["issue_comments"] = issue_comments
            issue_object["pr_comments"] = pr_comments
            issue_object["pr_review_comments"] = pr_review_comments
            issue_object["committers"] = committers
            issue_object["changed_files"] = changed_files
            issue_object["issue_created_by"] = issue_created_by
            issue_object["pr_merged_by"] = pr_merged_by
            # issue_object["issue_closed_by"] = issue_closed_by
            issue_object["issue_closed_at"] = issue_closed_at
            # Append issue data to issue dataset
            print(issue_object)
            dataset.append(issue_object)
    print("Get data Done!!!")
    # Save pre-precessed data to json file
    print("Writing JSON...")
    newDataJson = json.dumps(dataset)
    with open('data/data.json', 'w') as f:
        json.dump(newDataJson, f)
    print("Writing JSON Done!!!")
    return dataset


# ==============Main==============
issue_dataset = getIssueData()
