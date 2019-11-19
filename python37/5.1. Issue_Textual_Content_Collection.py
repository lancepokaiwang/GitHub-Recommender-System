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
            dataset[issue["id"]] = {
                "title": str(issue["title"]).replace("\"", ""),
                "body": str(issue["body"]).replace("\"", "")
            }

    return dataset


# ==============Main==============
dataset_master = getIssueData(owner=OWNER, repo=REPO, required_labels=FIRST_TIMER_LABELS)

bfs.writeJsonFile(data=dataset_master, name="issues_text_{}".format(REPO), folder="data/issue_text")

print(len(dataset_master))
