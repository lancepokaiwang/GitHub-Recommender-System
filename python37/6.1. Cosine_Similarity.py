import Basic_Functions as bfs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math

REPO = "symfony"
THRESHOLD = 3 #top 3 results



issue_comments = bfs.readJsonFile(name="issue_comments_text_{}".format(REPO), folder="data/issue_text")
issue_commits = bfs.readJsonFile(name="issue_commits_text_{}".format(REPO), folder="data/issue_text")
issues = bfs.readJsonFile(name="processed_issues_text_{}".format(REPO), folder="data/issue_text").items()
users = bfs.readJsonFile(name="processed_user_text_{}".format(REPO), folder="data/user_text")
commits = bfs.readJsonFile(name="all_issues_{}_commits".format(REPO), folder="data/all_issues")

user_numbers = {}
for commit_id, commit_users in commits.items():
    for user in commit_users:
        if user not in user_numbers:
            user_numbers[user] = 1
        else:
            user_numbers[user] += 1

def recommendation(user):
    TOP_RESULTS = []
    ALL = []

    user_profile = users[user]
    # print(user_profile)
    user_content = ""

    user_content += (user_profile["commit_comments"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["commits"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["issue_comments"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["pr_comments"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["prs"].replace('\r', '')).replace('\n', '') + " "

    for issue_id, issue in issues:
        temp = ""
        temp += "{} {}".format((issue["title"].replace('\r', '')).replace('\n', ''), (issue["body"].replace('\r', '')).replace('\n', ''))
        for comment in issue_comments[issue_id]["comments"]:
            temp += "{}".format((comment.replace('\r', '')).replace('\n', ''))
        for commit in issue_commits[issue_id]["commits"]:
            temp += "{}".format((commit.replace('\r', '')).replace('\n', ''))
        documents = (user_content, temp)

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

        result = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
        result = result.tolist()
        score = float(result[0][1])

        ALL.append((issue_id,score)) 

        TOP_RESULTS = sorted(ALL, key=lambda tup: tup[1],reverse=True)[3:]
       # print(TOP_RESULTS)

    return TOP_RESULTS


ISSUES_EXPECTED = {}
TOTAL_CORRECT = 0
TOTAL_RESULTS = 0

ISSUES = set()
for userid, user in users.items():
    if userid in user_numbers:
        result = recommendation(userid)

        print("Results for user {}: ".format(userid))
        #print(result)

        correct = 0
        for item, score in result:
            ISSUES.add(item)
            TOTAL_RESULTS += 1
            if (userid in commits[item]):
                ISSUES_EXPECTED[item] = 1
                correct += 1
                TOTAL_CORRECT += 1
        if user_numbers[userid] < THRESHOLD:
            print("Overall correct: {} / {}".format(correct, user_numbers[userid]))
        else:
            print("Overall correct: {} / {}".format(correct, THRESHOLD))
        #print("\n\n\n")

#print("\n\n\n")
print("Average accuracy: {}%".format(round((TOTAL_CORRECT / TOTAL_RESULTS) * 100), 2))
print(ISSUES_EXPECTED)
print(ISSUES)
print(len(ISSUES_EXPECTED)/len(ISSUES))

#result = recommendation(TARGET_USER)
#print("The best issue for user {} is issue No.{} (score: {})".format(TARGET_USER, result["number"], result["score"]))
