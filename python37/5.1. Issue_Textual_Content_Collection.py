<<<<<<< HEAD
import pymongo
import urllib3
import requests
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
FIRST_TIMER_LABELS = ["Easy Pick"]


# ==============Functions==============
def get_issue_data(owner="symfony", repo="symfony", required_labels=["good first issue"]):
    dataset = {}

    # ============ Local Search ============
    issues = mg_db["issues"].find({"repo": repo, "owner": owner}, {"_id": 0})

    for issue in issues:
        RECORD = False
        for label in issue["labels"]:
            if label["name"] in required_labels:
                RECORD = True
        if RECORD:
            dataset[issue["id"]] = {
                "title": str(issue["title"]).replace("\"", ""),
                "body": str(issue["body"]).replace("\"", ""),
                "comments": search_issue_comments(issue["number"]),
                "commits": search_issue_commit(issue["number"])
            }

    return dataset


def search_issue_comments(issue_number=0):
    comments_result = []

    issue_comments_url = "https://api.github.com/repos/{}/{}/issues/{}/comments?client_id={}&client_secret={}".format(
        OWNER, REPO, issue_number, CLIENT_ID, CLIENT_SECRET)
    print(issue_comments_url)
    issue_comments = requests.get(issue_comments_url, verify=False).json()

    for comment in issue_comments:
        comments_result.append(str(comment["body"]).replace("\"", ""))

    return comments_result


def search_issue_commit(issue_number=0):
    comments_result = []

    commits_url = "https://api.github.com/repos/{}/{}/pulls/{}/commits?client_id={}&client_secret={}".format(
        OWNER, REPO, issue_number, CLIENT_ID, CLIENT_SECRET)
    print(commits_url)
    commits = requests.get(commits_url, verify=False).json()
    if "documentation_url" not in commits:
        for commit in commits:
            comments_result.append(str(commit["commit"]["message"]).replace("\"", ""))

    # Get referenced commits
    issue_event_url = "https://api.github.com/repos/{}/{}/issues/{}/events?client_id={}&client_secret={}".format(
        OWNER, REPO, issue_number, CLIENT_ID, CLIENT_SECRET)
    print(issue_event_url)
    issue_events = requests.get(issue_event_url, verify=False).json()
    for issue_event in issue_events:
        if issue_event["event"] == "referenced":
            reference_url = "{}?client_id={}&client_secret={}".format(
                issue_event["commit_url"], CLIENT_ID, CLIENT_SECRET)
            print(reference_url)
            issue_reference = requests.get(reference_url, verify=False).json()
            if "url" in issue_reference.keys() and "files" in issue_reference.keys():
                comments_result.append(str(issue_reference["commit"]["message"]).replace("\"", ""))

    return comments_result


# ==============Main==============
dataset_master = get_issue_data(owner=OWNER, repo=REPO, required_labels=FIRST_TIMER_LABELS)

bfs.writeJsonFile(data=dataset_master, name="issues_text_{}".format(REPO), folder="data/issue_text")

print(len(dataset_master))
=======
import pymongo
import Basic_Functions as bfs


# MongoDB construction
mg_client = pymongo.MongoClient("mongodb://localhost:27017/")
mg_db = mg_client["msr14"]

OWNER = "symfony"
REPO = "symfony"
FIRST_TIMER_LABELS = ["Easy Pick"]


# ==============Functions==============
def getIssueData(owner="symfony", repo="symfony", required_labels=["good first issue"]):
    output = {}

    # ============ Local Search ============
    issues = mg_db["issues"].find({"repo": repo, "owner": owner}, {"_id": 0})

    for issue in issues:
        RECORD = False
        for label in issue["labels"]:
            if label["name"] in required_labels:
                RECORD = True
        if RECORD:
            output[issue["id"]] = {
                "github_issue_id":issue["number"],
                "state":issue["state"],
                "title": issue["title"],
                "body": issue["body"],
            }

    return output


# ==============Main==============
dataset_master = getIssueData(owner=OWNER, repo=REPO, required_labels=FIRST_TIMER_LABELS)

bfs.writeJsonFile(data=dataset_master, name="issues_text_{}".format(REPO), folder="data/issue_text")

#print(len(dataset_master))
>>>>>>> d9bb0b72f761538bd084f26a41d91dfec0d96e39
