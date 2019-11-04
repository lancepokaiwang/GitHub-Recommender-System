import datetime
import json
import pymongo
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["msr14"]

# GitHub API oAuth
CLIENT_ID = "6aca4b66775c629cbafd"
CLIENT_SECRET = "2349a0a9266e81f9f4d7df62ca49a98ca357b20c"


def user_extraction():
    user_master = {}
    with open('data/data.json') as json_file:
        dataset = json.load(json_file)
        length = len(dataset)
        index = 0
        for data in dataset:
            # Counter
            print("Current progress: {} / {}".format(index, length))
            # Issue creator
            if data["issue_created_by"] not in user_master:
                return_user = getUserDetails(data["issue_created_by"], data["issue_closed_at"])
                if return_user != {}:
                    user_master[data["issue_created_by"]] = return_user
                    index += 1
                    print(str(index) + " users has been added!")
            # Issue comment makers
            for user in data["assignees"]:
                if user not in user_master:
                    return_user = getUserDetails(user, data["issue_closed_at"])
                    if return_user != {}:
                        user_master[user] = return_user
                        index += 1
                        print(str(index) + " users has been added!")
            # Issue comment makers
            for user in data["issue_comment_users"]:
                if user not in user_master:
                    return_user = getUserDetails(user, data["issue_closed_at"])
                    if return_user != {}:
                        user_master[user] = return_user
                        index += 1
                        print(str(index) + " users has been added!")
            # Issue event users
            for user in data["issue_event_users"]:
                if user not in user_master:
                    return_user = getUserDetails(user, data["issue_closed_at"])
                    if return_user != {}:
                        user_master[user] = return_user
                        index += 1
                        print(str(index) + " users has been added!")
            # PR review comment makers
            for user in data["pr_comment_users"]:
                if user not in user_master:
                    return_user = return_user
                    if return_user != {}:
                        user_master[user] = return_user
                        index += 1
                        print(str(index) + " users has been added!")
            # PR committers
            for user in data["committers"]:
                if user not in user_master:
                    return_user = getUserDetails(user, data["issue_closed_at"])
                    if return_user != {}:
                        user_master[user] = return_user
                        index += 1
                        print(str(index) + " users has been added!")

            # if index == 3:
            #     break
    return user_master


def getUserDetails(name, issue_end_date):
    # print(issue_end_date)
    # print(name)
    mongo_table = mongo_db["users"]
    user = {}
    if mongo_table.count_documents({"login": name}) > 0:
        for result in mongo_table.find({"login": name}, {"_id": 0}):
            user["login"] = name
            # user age
            age_delta = datetime.datetime.strptime(issue_end_date, '%Y-%m-%d') - datetime.datetime.strptime(
                result["created_at"][0:10], '%Y-%m-%d')
            user_age = age_delta.days
            user["age"] = user_age

            # number of repositories
            user["repo_num"] = result["public_repos"]

            # number of followers
            user["follower_num"] = result["followers"]
            # number of events
            # user["event_num"] = 0
            # event_url = "https://api.github.com/users/{}/events?client_id={}&client_secret={}".format(name, CLIENT_ID,
            #                                                                                           CLIENT_SECRET)
            # print(event_url)
            # events = requests.get(event_url, verify=False).json()
            # for event in events:
            #     day_delta = datetime.datetime.strptime(issue_end_date, '%Y-%m-%d') - datetime.datetime.strptime(
            #         event["created_at"][0:10], '%Y-%m-%d')
            #     if day_delta.days > 0:
            #         user["event_num"] += 1

            # number of commit comments
            user["commit_comment_num"] = mongo_db["users"].count_documents({"user": name})
            # print(user["commit_comment_num"])

            # number of commits
            user["commit_num"] = mongo_db["commits"].count_documents({"author.login": name})

            # number of issue comments
            user["issue_comment_num"] = mongo_db["issue_comments"].count_documents({"user.login": name})

            # number of issue events
            user["issue_event_num"] = mongo_db["issue_events"].count_documents({"actor.login": name})

            # number of issues
            user["issue_number"] = mongo_db["issues"].count_documents({"user.login": name})

            # number of org
            user["org_number"] = mongo_db["org_members"].count_documents({"login": name})

            # number of PR comments
            user["pr_comment_num"] = mongo_db["pull_request_comments"].count_documents({"user.login": name})

            # number of PRs
            user["pr_num"] = mongo_db["pull_requests"].count_documents({"user.login": name})

            # number of collaborator
            user["collaborator_num"] = mongo_db["repo_collaborators"].count_documents({"login": name})

            # print(user)
    return user


# ==========Main==========
users = user_extraction()
print(users)

newDataJson = json.dumps(users)
with open('data/data_users.json', 'w') as f:
    json.dump(newDataJson, f)
