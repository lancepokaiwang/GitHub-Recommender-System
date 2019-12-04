import requests
import urllib3
import time
import Basic_Functions as bfs

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GitHub API oAuth
CLIENT_ID = "6aca4b66775c629cbafd"
CLIENT_SECRET = "2349a0a9266e81f9f4d7df62ca49a98ca357b20c"

OWNER = "symfony"
REPO = "symfony"

users = bfs.readJsonFile(name="users_{}_valid_purpose".format(REPO), folder="data/validation")


users_textual_data = {}

for userID, items in users.items():
    user_textual = {}

    # repos
    repos = []
    for item in items["repos"]:
        url = "{}?client_id={}&client_secret={}".format(item["url"], CLIENT_ID, CLIENT_SECRET);
        print(url)
        result = requests.get(url, verify=False).json()
        if "description" in result:
            text = str(result["description"]).replace("\"", " ")
            repos.append(text)
        # time.sleep(1)
    user_textual["repos"] = repos

    # commit_comments
    ccs = []
    for item in items["commit_comments"]:
        url = "{}?client_id={}&client_secret={}".format(item["url"], CLIENT_ID, CLIENT_SECRET);
        print(url)
        result = requests.get(url, verify=False).json()
        if "body" in result:
            text = str(result["body"]).replace("\"", " ")
            ccs.append(text)
        # time.sleep(1)
    user_textual["commit_comments"] = ccs

    # commits
    cs = []
    for item in items["commits"]:
        url = "{}?client_id={}&client_secret={}".format(item["url"], CLIENT_ID, CLIENT_SECRET);
        print(url)
        result = requests.get(url, verify=False).json()
        if "commit" in result:
            text = str(result["commit"]["message"]).replace("\"", " ")
            cs.append(text)
        # time.sleep(1)
    user_textual["commits"] = cs

    # issue_comments
    ics = []
    for item in items["issue_comments"]:
        url = "{}?client_id={}&client_secret={}".format(item["url"], CLIENT_ID, CLIENT_SECRET);
        print(url)
        result = requests.get(url, verify=False).json()
        if "body" in result:
            text = str(result["body"]).replace("\"", " ")
            ics.append(text)
        # time.sleep(1)
    user_textual["issue_comments"] = ics

    # issues
    iss = []
    for item in items["issues"]:
        url = "{}?client_id={}&client_secret={}".format(item["url"], CLIENT_ID, CLIENT_SECRET);
        print(url)
        result = requests.get(url, verify=False).json()
        if "title" in result:
            title = str(result["title"]).replace("\"", " ")
            body = str(result["body"]).replace("\"", " ")
            iss.append({
                "title": title,
                "body": body
            })
        # time.sleep(1)
    user_textual["issues"] = iss

    # pr_comments
    pcs = []
    for item in items["pr_comments"]:
        url = "{}?client_id={}&client_secret={}".format(item["url"], CLIENT_ID, CLIENT_SECRET);
        print(url)
        result = requests.get(url, verify=False).json()
        if "body" in result:
            text = str(result["body"]).replace("\"", " ")
            pcs.append(text)
        # time.sleep(1)
    user_textual["pr_comments"] = pcs
    # prs
    prs = []
    for item in items["prs"]:
        url = "{}?client_id={}&client_secret={}".format(item["url"], CLIENT_ID, CLIENT_SECRET);
        print(url)
        result = requests.get(url, verify=False).json()
        if "title" in result:
            title = str(result["title"]).replace("\"", " ")
            body = str(result["body"]).replace("\"", " ")
            prs.append({
                "title": title,
                "body": body
            })
        # time.sleep(1)
    user_textual["prs"] = prs

    # Save to master array
    users_textual_data[userID] = user_textual

bfs.writeJsonFile(data=users_textual_data, name="users_{}_textual_valid_purpose".format(REPO), folder="data/validation")

