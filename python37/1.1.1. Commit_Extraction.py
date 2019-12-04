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
def getIssueData(owner="symfony", repo="symfony", required_labels=["good first issue"]):
    dataset = {}

    # ============ Local Search ============
    issues = mg_db["issues"].find({"repo": repo, "owner": owner}, {"_id": 0})

    for issue in issues:
        RECORD = False
        for label in issue["labels"]:
            if label["name"] in required_labels:
                RECORD = True
        if RECORD:
            # --process issue
            del issue["title"]
            del issue["body"]
            # issue["title"] = str(issue["title"]).replace("\"", "'")
            # issue["body"] = str(issue["body"]).replace("\"", "'")

            # Get pull request
            pull_request_url = "https://api.github.com/repos/{}/{}/pulls/{}?client_id={}&client_secret={}".format(
                owner, repo, issue["number"], CLIENT_ID, CLIENT_SECRET)
            print(pull_request_url)
            pull_request = requests.get(pull_request_url, verify=False).json()

            # Get referenced commits
            commits = []
            issue_event_url = "https://api.github.com/repos/{}/{}/issues/{}/events?client_id={}&client_secret={}".format(
                owner, repo, issue["number"], CLIENT_ID, CLIENT_SECRET)
            print(issue_event_url)
            issue_events = requests.get(issue_event_url, verify=False).json()
            for issue_event in issue_events:
                if issue_event["event"] == "referenced":
                    reference_url = "{}?client_id={}&client_secret={}".format(
                        issue_event["commit_url"], CLIENT_ID, CLIENT_SECRET)
                    print(reference_url)
                    issue_reference = requests.get(reference_url, verify=False).json()
                    if "url" in issue_reference.keys() and "files" in issue_reference.keys():
                        if issue_reference["committer"] is not None:
                            commits.append(str(issue_reference["committer"]["id"]))
            # --process pull request
            if "number" in pull_request:
                # Get commit
                pull_commits_url = "{}?client_id={}&client_secret={}".format(
                    pull_request["commits_url"], CLIENT_ID, CLIENT_SECRET)
                print(pull_commits_url)
                pull_commits = requests.get(pull_commits_url, verify=False).json()
                # --process pull request
                for pull_commit in pull_commits:
                    if "url" in pull_commit.keys() and "files" in pull_commit.keys():
                        if pull_commit["committer"] is not None:
                            commits.append(str(pull_commit["committer"]["id"]))
            else:
                pull_request = None

            # Add all data to dataset
            dataset[issue["id"]] = commits
    return dataset


# ==============Main==============
dataset_master = getIssueData(owner=OWNER, repo=REPO, required_labels=FIRST_TIMER_LABELS)

bfs.writeJsonFile(data=dataset_master, name="all_issues_{}_commits".format(REPO), folder="data/all_issues")

print(len(dataset_master))
