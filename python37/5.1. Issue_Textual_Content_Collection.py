import pymongo
import urllib3
import requests
import Basic_Functions as bfs
from tqdm import tqdm

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
secret = ""
username = ""


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

    for issue in tqdm(issues):
        RECORD = False
        for label in issue["labels"]:
            if label["name"] in required_labels:
                RECORD = True
        if RECORD:
            output[issue["id"]] = {
                "github_issue_id": issue["number"],
                "state": issue["state"],
                "title": issue["title"],
                "body": issue["body"],
            }

    return output


def search_issue_comments(issue_number, username, token):
    comments_result = []

    issue_comments_url = "https://api.github.com/repos/{}/{}/issues/{}/comments".format(
        OWNER, REPO, issue_number)
    print(issue_comments_url)
    issue_comments = requests.get(
        issue_comments_url, verify=False, auth=(username, token)).json()

    for comment in issue_comments:
        comments_result.append(str(comment["body"]).replace("\"", ""))

    return comments_result




def search_issue_commits(issue_number, username, token):
    comments_result = []

    # Get referenced commits
    issue_event_url = "https://api.github.com/repos/{}/{}/issues/{}/events".format(OWNER, REPO, issue_number)
    print(issue_event_url)
    issue_events = requests.get(issue_event_url, verify=False, auth=(username, token)).json()
    for issue_event in issue_events:
        print(issue_event)
        if issue_event["event"] == "referenced":
            commit_url = issue_event["commit_url"]
            print(commit_url)
            issue_reference = requests.get(commit_url, verify=False, auth=(username,token)).json()
            if "url" in issue_reference.keys() and "files" in issue_reference.keys():
                comments_result.append(
                    str(issue_reference["commit"]["message"]).replace("\"", ""))

    return comments_result

# ==============Main==============
SCRAPE_COMMENTS = False
SCRAPE_COMMITS = True
RUN = False

issues_data_folder = "data/issue_text"
issues_output_filename = "issues_text_{}".format(REPO)
comment_output_filename = "issue_comments_text_{}".format(REPO)
commit_output_filename = "issue_commits_text_{}".format(REPO)

if RUN:

    dataset_master = getIssueData(
        owner=OWNER, repo=REPO, required_labels=FIRST_TIMER_LABELS)

    

    bfs.writeJsonFile(data=dataset_master,
                      name=issues_output_filename, folder=issues_data_folder)


requests_remaining = bfs.checkGitHubLimit(username, secret)["remaining"]
if requests_remaining >= 1000 and SCRAPE_COMMENTS:

    issues = bfs.readJsonFile(
        name=issues_output_filename, folder=issues_data_folder).items()
    output_issue_comments = {}
    for issue, text in tqdm(issues):
        output_issue_comments[issue] = {
            "comments": search_issue_comments(text["github_issue_id"], username, secret),
        }
    bfs.writeJsonFile(data=output_issue_comments,
                      name=comment_output_filename, folder=issues_data_folder)

requests_remaining = bfs.checkGitHubLimit(username, secret)["remaining"]

if requests_remaining >= 1000 and SCRAPE_COMMITS:

    issues = bfs.readJsonFile(name=issues_output_filename, folder=issues_data_folder).items()
    output_commits = {}
    for issue, text in tqdm(issues): 
        output_commits[issue] = {
            "commits": search_issue_commits (text["github_issue_id"], username, secret)
        }

    bfs.writeJsonFile(data=output_commits,
                      name=commit_output_filename, folder=issues_data_folder)