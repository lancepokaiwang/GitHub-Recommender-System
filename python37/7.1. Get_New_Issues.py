import urllib3
import requests
import Basic_Functions as bfs

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    # ============ Online Search ============
    index = 0
    STOP = False
    STATE = "open"
    while not STOP:
        index += 1
        # Example Page: https://api.github.com/repos/symfony/symfony/issues?state=closed&page=1
        issues_url = "https://api.github.com/repos/{}/{}/issues?state={}&page={}&per_page=100&client_id={}&client_secret={}".format(
            owner, repo, STATE, index, CLIENT_ID, CLIENT_SECRET)
        print(issues_url)
        issues = requests.get(issues_url, verify=False).json()
        # If the length of issues is 0, check whether should search closed issue or stop the while loop
        if len(issues) == 0:
            STOP = True
        # Process all issues
        for issue in issues:
            RECORD = True
            # for label in issue["labels"]:
            #     if label["name"] in required_labels:
            #         RECORD = True
            if RECORD:
                # --process issue
                issue["title"] = str(issue["title"]).replace("\"", "'")
                issue["title"] = str(issue["title"]).replace('\n', "")
                issue["title"] = str(issue["title"]).replace('\r', "")
                issue["body"] = str(issue["title"]).replace("\"", "'")
                issue["body"] = str(issue["title"]).replace('\n', "")
                issue["body"] = str(issue["title"]).replace('\r', "")

                # Get pull request
                # pull_request_url = "https://api.github.com/repos/{}/{}/pulls/{}?client_id={}&client_secret={}".format(
                #     owner, repo, issue["number"], CLIENT_ID, CLIENT_SECRET)
                # print(pull_request_url)
                # pull_request = requests.get(pull_request_url, verify=False).json()
                # --process pull request
                # commits = []
                # if "number" in pull_request:
                #     pull_request["title"] = str(pull_request["title"]).replace("\"", "'")
                #     pull_request["body"] = str(pull_request["body"]).replace("\"", "'")
                #
                #     # Get commit
                #     pull_commits_url = "{}?client_id={}&client_secret={}".format(
                #         pull_request["commits_url"], CLIENT_ID, CLIENT_SECRET)
                #     print(pull_commits_url)
                #     pull_commits = requests.get(pull_commits_url, verify=False).json()
                #     # --process pull request
                #     for pull_commit in pull_commits:
                #         commits.append(pull_commit)
                # else:
                #     pull_request = None

                # Add all data to dataset
                # dataset.append({"issue": issue, "pull_request": pull_request, "pull_commits": commits})
                dataset[issue["number"]] = issue
                # dataset.append({"issue": issue})
    return dataset


# ==============Main==============
dataset_master = getIssueData(owner=OWNER, repo=REPO, required_labels=FIRST_TIMER_LABELS)

bfs.writeJsonFile(data=dataset_master, name="all_open_issues_{}".format(REPO), folder="data/open_issues")

print(len(dataset_master))
