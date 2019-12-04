import operator

import Basic_Functions as bfs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math

REPO = "symfony"

TARGET_USER = "248818"
NUM_OF_SELECTION = 3

issue_comments = bfs.readJsonFile(name="issue_comments_text_{}".format(REPO), folder="data/issue_text")
issue_commits = bfs.readJsonFile(name="issue_commits_text_{}".format(REPO), folder="data/issue_text")
issues = bfs.readJsonFile(name="processed_issues_text_{}".format(REPO), folder="data/issue_text").items()
users = bfs.readJsonFile(name="processed_user_text_{}_valid_purpose".format(REPO), folder="data/validation")
commits = bfs.readJsonFile(name="all_issues_{}_commits".format(REPO), folder="data/all_issues")

user_numbers = {}
for commit_id, commit_users in commits.items():
    for user in commit_users:
        if user not in user_numbers:
            user_numbers[user] = 1
        else:
            user_numbers[user] += 1


def recommendation(user="248818"):
    scores = {}

    user_profile = users[user]
    # print(user_profile)
    user_content = ""

    user_content += (user_profile["commit_comments"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["commits"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["issue_comments"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["pr_comments"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["prs"].replace('\r', '')).replace('\n', '') + " "

    # print(user_content)

    # For every issue
    for issue_id, issue in issues:
        # print(issue_id)
        temp = ""
        temp += "{} {}".format((issue["title"].replace('\r', '')).replace('\n', ''),
                               (issue["body"].replace('\r', '')).replace('\n', ''))
        for comment in issue_comments[issue_id]["comments"]:
            temp += "{}".format((comment.replace('\r', '')).replace('\n', ''))
        for commit in issue_commits[issue_id]["commits"]:
            temp += "{}".format((commit.replace('\r', '')).replace('\n', ''))
        # print(temp)
        documents = (user_content, temp)

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        # print(tfidf_matrix.shape)

        result = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
        result = result.tolist()
        score = float(result[0][1])
        # print(score)

        scores[issue_id] = score

    if user_numbers[user] < NUM_OF_SELECTION:
        scores = dict(sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[:user_numbers[user]])
    else:
        scores = dict(sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[:NUM_OF_SELECTION])

    return scores


# Main


TOTAL_CORRECT = 0
TOTAL_RESULTS = 0
for userid, user in users.items():
    if userid in user_numbers:
        result = recommendation(userid)

        print("Results for user {}: ".format(userid))
        print(result)

        correct = 0
        for item, score in result.items():
            TOTAL_RESULTS += 1
            for commit_user in commits[item]:
                if commit_user == userid:
                    correct += 1
                    TOTAL_CORRECT += 1
        if user_numbers[userid] < NUM_OF_SELECTION:
            print("Overall correct: {} / {}".format(correct, user_numbers[userid]))
        else:
            print("Overall correct: {} / {}".format(correct, NUM_OF_SELECTION))
        print("\n\n\n")

print("\n\n\n")
print("Average accuracy: {}%".format(round((TOTAL_CORRECT / TOTAL_RESULTS) * 100), 2))
