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


# ==============Main==============
dataset = bfs.readJsonFile(name="all_issues_{}".format(REPO), folder="data/all_issues")

num_pull = 0
num_commits = 0

for data in dataset:
    if data["pull_request"] is not None:
        num_pull += 1
    if data["pull_commits"]:
        num_commits += 1

print("{} issues have pull request.".format(num_pull))
print("{} issues have commits.".format(num_commits))
