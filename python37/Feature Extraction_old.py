import datetime
import json
import pymongo

# Download MSR 2014 in here: http://ghtorrent.org/msr14.html

# Functions
def grabData():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["msr14"]
    mycol = mydb["issues"]
    # Find all closed issues from symfony
    query = {"closed_at": {"$ne": None}, "repo": "symfony", "state": "closed"}
    columns = {"_id": 0}

    for issue in mycol.find(query, columns):
        # Only record "good first time" issue
        for label in issue['labels']:
            # Record all labels
            if label['name'] not in labels:
                labels[label['name']] = 1
            else:
                labels[label['name']] += 1
            # Check whether it is an easy issue
            if label['name'] == 'Easy Pick' or label['name'] == 'Bug':
                issue["title"] = str(issue["title"]).replace("\"", "”")
                issue["body"] = str(issue["body"]).replace("\"", "”")
                measurements.append(issue)
    # Save original data to json file
    # originalJasonData = json.dumps(measurements)
    # with open('original_data.json', 'w') as f:
    #     json.dump(originalJasonData, f)


def dataPreprocess(oldData):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["msr14"]
    newData = []
    TOTAL_NUM = len(oldData)
    CURRENT_NUM = 0
    for issue in oldData:
        CURRENT_NUM += 1
        print("Progress: " + str(CURRENT_NUM) + " / " + str(TOTAL_NUM))
        if issue["user"]["login"] != "symfony":
            # print(issue)
            # User data
            issueClosedAt = issue["closed_at"][0:10]
            userData = None
            users = mydb["users"]
            for user in users.find({"login": issue["user"]["login"]}):
                userData = user

            # print(userData)
            repoNumber = userData["public_repos"] if userData != None else -1
            followerNumber = int(userData["followers"]) if userData != None else -1
            userCreatedAt = userData["created_at"][0:10] if userData != None else issue["closed_at"][0:10]
            delta = datetime.datetime.strptime(issueClosedAt, '%Y-%m-%d') - datetime.datetime.strptime(userCreatedAt,
                                                                                                       '%Y-%m-%d')
            userAge = delta.days

            # Languages
            prs = mydb["pull_requests"]
            repos = mydb["repos"]
            languages = {}
            # ---Find all comments made by the user
            query = {"closed_at": {"$ne": None}, "state": "closed", "user.login": issue["user"]["login"]}
            columns = {"_id": 0}

            for subIssue in prs.find(query, columns):
                for repo in repos.find({"full_name": subIssue["owner"] + "/" + subIssue["repo"]}, {"_id": 0}):
                    # print(repo)
                    if repo["language"] not in languages:
                        languages[repo["language"]] = 1
                    else:
                        languages[repo["language"]] += 1

            # Comments
            prs = mydb["pull_requests"]
            issue_comments = mydb["issue_comments"]
            query = {"state": "closed", "user.login": issue["user"]["login"]}
            columns = {"_id": 0}

            comments = {}
            # ---Find all pull request comments
            for pullRequest in prs.find(query, columns):
                for issue_comment in issue_comments.find({"repo": pullRequest["repo"], "owner": pullRequest["owner"], "issue_id": pullRequest["number"]}, {"_id": 0}):
                    # print(pullRequestComment)
                    singleComment = issue_comment["owner"] + "/" + issue_comment["repo"] + "/" + str(issue_comment["issue_id"])
                    if singleComment not in comments:
                        comments[singleComment] = 1
                    else:
                        comments[singleComment] += 1

            # Extract label(s)
            issue_labels = []
            for label in issue["labels"]:
                issue_labels.append(label["name"])

            # Add filtered data into newData (only record the developer who is still existed)
            if repoNumber != -1 and followerNumber != -1:
                newData.append(
                    {
                        "issue_id": issue["id"],
                        "title": str(issue["title"]).replace("\"", ""),
                        "body": str(issue["body"]).replace("\"", ""),
                        "user_followers": followerNumber,
                        "user_age": userAge,
                        "repo_number": repoNumber,
                        "labels": issue_labels,
                        "user_commit_languages": languages,
                        "user_comments": comments
                    }
                )
    # print(newData)

    # Save pre-precessed data to json file
    # newDataJson = json.dumps(newData)
    # with open('data.json', 'w') as f:
    #     json.dump(newDataJson, f)
    return newData

def dataPreprocessWithContext(oldData):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["msr14"]
    newData = []
    TOTAL_NUM = len(oldData)
    CURRENT_NUM = 0
    for issue in oldData:
        CURRENT_NUM += 1
        print("Progress: " + str(CURRENT_NUM) + " / " + str(TOTAL_NUM))
        if issue["user"]["login"] != "symfony":
            titles = str(issue["title"]) + " "
            bodies = str(issue["body"]) + " "
            # print(issue)
            # User data
            issueClosedAt = issue["closed_at"][0:10]
            userData = None
            users = mydb["users"]
            for user in users.find({"login": issue["user"]["login"]}):
                userData = user

            # print(userData)
            repoNumber = userData["public_repos"] if userData != None else -1
            followerNumber = int(userData["followers"]) if userData != None else -1
            userCreatedAt = userData["created_at"][0:10] if userData != None else issue["closed_at"][0:10]
            delta = datetime.datetime.strptime(issueClosedAt, '%Y-%m-%d') - datetime.datetime.strptime(userCreatedAt,
                                                                                                       '%Y-%m-%d')
            userAge = delta.days

            # Languages
            prs = mydb["pull_requests"]
            repos = mydb["repos"]
            languages = {}
            # ---Find all comments made by the user
            query = {"closed_at": {"$ne": None}, "state": "closed", "user.login": issue["user"]["login"]}
            columns = {"_id": 0}

            for subIssue in prs.find(query, columns):
                for repo in repos.find({"full_name": subIssue["owner"] + "/" + subIssue["repo"]}, {"_id": 0}):
                    # print(repo)
                    if repo["language"] not in languages:
                        languages[repo["language"]] = 1
                    else:
                        languages[repo["language"]] += 1

            # Comments
            issue_comments = mydb["issue_comments"]
            query = {"owner": issue["owner"], "repo": issue["repo"], "issue_id": issue["number"]}
            columns = {"_id": 0}

            # ---Find all pull request comments
            for issue_comment in issue_comments.find(query, columns):
                bodies += issue_comment["body"] + " "


            # Extract label(s)
            issue_labels = []
            for label in issue["labels"]:
                issue_labels.append(label["name"])

            # Add filtered data into newData (only record the developer who is still existed)
            if repoNumber != -1 and followerNumber != -1:
                newData.append(
                    {
                        "issue_id": issue["id"],
                        "title": str(titles).replace("\"", ""),
                        "body": str(bodies).replace("\"", ""),
                        "user_followers": followerNumber,
                        "user_age": userAge,
                        "repo_number": repoNumber,
                        "labels": issue_labels,
                        "user_commit_languages": languages,
                    }
                )
            print(newData)
    # print(newData)

    # Save pre-precessed data to json file
    newDataJson = json.dumps(newData)
    with open('data-context.json', 'w') as f:
        json.dump(newDataJson, f)
    return newData


def printDictionary(dict):
    for key in dict.keys():
        print(format(key) + ": " + format(dict[key]))


def printArray(arr):
    for item in arr:
        print(item)


# ===================================Main===================================
measurements = []
labels = {}

grabData()
# print(len(measurements))
printDictionary(labels)
# measurements = dataPreprocess(measurements)
measurements = dataPreprocessWithContext(measurements)
# printArray(measurements)
