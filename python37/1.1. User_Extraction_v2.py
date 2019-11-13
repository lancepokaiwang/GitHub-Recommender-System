import datetime
import json
import pymongo
import requests
import urllib3
import threading
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["msr14"]

# GitHub API oAuth
CLIENT_ID = "6aca4b66775c629cbafd"
CLIENT_SECRET = "2349a0a9266e81f9f4d7df62ca49a98ca357b20c"

def user_extraction():
    user_master = []
    with open('data/data.json') as json_file:
        dataset = json.load(json_file)
        index = 0
        for data in dataset:
            newcomer = False
            for label in data["lables"]:
                if label == "Easy Pick":
                    newcomer = True
            # Issue creator
            print("issue_created_by")
            return_user = getUserDetails(data["issue_created_by"], data["issue_closed_at"], newcomer)
            if bool(return_user):
                print(return_user)
                index += 1
                print(str(index) + " records has been added!")
                user_master.append(return_user)

            # Issue comment makers
            print("assignees")
            for user in data["assignees"]:
                return_user = getUserDetails(user, data["issue_closed_at"], newcomer)
                if bool(return_user):
                    print(return_user)
                    index += 1
                    print(str(index) + " records has been added!")
                    user_master.append(return_user)

            # Issue comment makers
            print("issue_comment_users")
            for user in data["issue_comment_users"]:
                return_user = getUserDetails(user, data["issue_closed_at"], False)
                if bool(return_user):
                    print(return_user)
                    index += 1
                    print(str(index) + " records has been added!")
                    user_master.append(return_user)

            # Issue event users
            print("issue_event_users")
            for user in data["issue_event_users"]:
                return_user = getUserDetails(user, data["issue_closed_at"], False)
                if bool(return_user):
                    print(return_user)
                    index += 1
                    print(str(index) + " records has been added!")
                    user_master.append(return_user)

            # PR review comment makers
            print("pr_comment_users")
            for user in data["pr_comment_users"]:
                return_user = getUserDetails(user, data["issue_closed_at"], False)
                if bool(return_user):
                    print(return_user)
                    index += 1
                    print(str(index) + " records has been added!")
                    user_master.append(return_user)

            # PR committers
            print("committers")
            for user in data["committers"]:
                return_user = getUserDetails(user, data["issue_closed_at"], newcomer)
                if bool(return_user):
                    print(return_user)
                    index += 1
                    print(str(index) + " records has been added!")
                    user_master.append(return_user)

                # if index == 3:
            #     break
    return user_master


user_collections = {}


def getUserDetails(name, issue_end_date, newcomer):
    print("\n\n\n\ncurrent user: {}".format(name))
    # print(issue_end_date)
    # print(name)

    if name not in user_collections:
        getDataFromDataset(name)

    mongo_table = mongo_db["users"]
    user = {}

    results = mongo_table.find({"login": name})
    # url = "https://api.github.com/users/{}?client_id={}&client_secret={}".format(name, CLIENT_ID, CLIENT_SECRET)
    # print(url)
    # result = requests.get(url, verify=False).json()

    for result in results:
        # print(result)
        user["newcomer"] = newcomer

        # user login
        user["login"] = name

        # user age
        print("age")
        age_delta = datetime.datetime.strptime(issue_end_date, '%Y-%m-%d') - datetime.datetime.strptime(
            result["created_at"][0:10], '%Y-%m-%d')
        user_age = age_delta.days
        user["age"] = user_age

        # number of repositories
        print("repo_num")
        user["repo_num"] = getNumber("repos", "owner.login", name, issue_end_date)

        # number of followers
        print("follower_num")
        # user["follower_num"] = getNumber("followers", "login", name, issue_end_date)
        user["follower_num"] = result["followers"]

        # number of commit comments
        print("commit_comment_num")
        user["commit_comment_num"] = getNumber("commit_comments", "user", name, issue_end_date)

        # number of commits
        print("commit_num")
        user["commit_num"] = getNumber("commits", "author.login", name, issue_end_date)

        # number of issue comments
        print("issue_comment_num")
        user["issue_comment_num"] = getNumber("issue_comments", "user.login", name, issue_end_date)

        # number of issue events
        print("issue_event_num")
        user["issue_event_num"] = getNumber("issue_events", "actor.login", name, issue_end_date)

        # number of issues
        print("issue_number")
        user["issue_number"] = getNumber("issues", "user.login", name, issue_end_date)

        # number of org
        print("org_number")
        user["org_number"] = getNumber("org_members", "login", name, issue_end_date)

        # number of PR comments
        print("pr_comment_num")
        user["pr_comment_num"] = getNumber("pull_request_comments", "user.login", name, issue_end_date)

        # number of PRs
        print("pr_num")
        user["pr_num"] = getNumber("pull_requests", "user.login", name, issue_end_date)

        # number of collaborator
        print("collaborator_num")
        user["collaborator_num"] = getNumber("repo_collaborators", "login", name, issue_end_date)

    print("brand new user has been generated!")
    # print(user)

    return user


def getDataFromDataset(name):
    user = {}

    user["login"] = name

    array = []
    items = mongo_db["repos"].find({"owner.login": name})
    for item in items:
        array.append(item)
    user["repos"] = array

    array = []
    items = mongo_db["commit_comments"].find({"user": name})
    for item in items:
        array.append(item)
    user["commit_comments"] = array

    array = []
    items = mongo_db["commits"].find({"author.login": name})
    for item in items:
        array.append(item)
    user["commits"] = array

    array = []
    items = mongo_db["issue_comments"].find({"user.login": name})
    for item in items:
        array.append(item)
    user["issue_comments"] = array

    array = []
    items = mongo_db["issue_events"].find({"actor.login": name})
    for item in items:
        array.append(item)
    user["issue_events"] = array

    array = []
    items = mongo_db["issues"].find({"user.login": name})
    for item in items:
        array.append(item)
    user["issues"] = array

    array = []
    items = mongo_db["org_members"].find({"login": name})
    for item in items:
        array.append(item)
    user["org_members"] = array

    array = []
    items = mongo_db["pull_request_comments"].find({"user.login": name})
    for item in items:
        array.append(item)
    user["pull_request_comments"] = array

    array = []
    items = mongo_db["pull_requests"].find({"user.login": name})
    for item in items:
        array.append(item)
    user["pull_requests"] = array

    array = []
    items = mongo_db["repo_collaborators"].find({"login": name})
    for item in items:
        array.append(item)
    user["repo_collaborators"] = array

    user_collections[name] = user
    # print(user)


def getNumber(table, condition, user, end_date):
    local_tables = ["repos", "commit_comments", "commits", "issue_comments", "issue_events", "issues",
                    "pull_request_comments", "pull_requests"]
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    count = 0

    items = user_collections[user][table]

    if table in local_tables:
        for item in items:
            if table == "commits":
                created_at = datetime.datetime.strptime(item["commit"]["author"]["date"][0:10], '%Y-%m-%d')
            else:
                created_at = datetime.datetime.strptime(item["created_at"][0:10], '%Y-%m-%d')

            if (end_date - created_at).days > 0: count += 1
    else:
        for item in items:
            url = "{}?client_id={}&client_secret={}".format(item["url"], CLIENT_ID, CLIENT_SECRET)
            # print(url)
            online_item = requests.get(url, verify=False).json()
            created_at = datetime.datetime.strptime(online_item["created_at"][0:10], '%Y-%m-%d')
            if (end_date - created_at).days > 0: count += 1
    print("count: {}".format(count))
    return count


t = threading.Thread(target=getUserDetails)

# ==========Main==========
users = user_extraction()
print(users)

newDataJson = json.dumps(users)
with open('data/data_users_2.json', 'w') as f:
    json.dump(newDataJson, f)
