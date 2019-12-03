import Basic_Functions as bfs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math

REPO = "symfony"

TARGET_USER = "248818"

issue_comments = bfs.readJsonFile(name="issue_comments_text_{}".format(REPO), folder="data/issue_text")
issue_commits = bfs.readJsonFile(name="issue_commits_text_{}".format(REPO), folder="data/issue_text")
issues = bfs.readJsonFile(name="processed_issues_text_{}".format(REPO), folder="data/issue_text").items()
users = bfs.readJsonFile(name="processed_user_text_{}".format(REPO), folder="data/user_text")


def recommendation(user="248818"):

    BEST_SCORE = 0.0
    BEST_RESULT = {"number": "", "score": 0.0}

    user_profile = users[user]
    # print(user_profile)
    user_content = ""

    user_content += (user_profile["commit_comments"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["commits"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["issue_comments"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["pr_comments"].replace('\r', '')).replace('\n', '') + " "
    user_content += (user_profile["prs"].replace('\r', '')).replace('\n', '') + " "

    print(user_content)

    # For every issue
    for issue_id, issue in issues:
        # print(issue_id)
        temp = ""
        temp += "{} {}".format((issue["title"].replace('\r', '')).replace('\n', ''), (issue["body"].replace('\r', '')).replace('\n', ''))
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
        print(score)

        if score > BEST_SCORE or BEST_RESULT["number"] == "":
            BEST_SCORE = score
            BEST_RESULT["score"] = score
            BEST_RESULT["number"] = issue_id


    return BEST_RESULT


result = recommendation(TARGET_USER)
print("The best issue for user {} is issue No.{} (score: {})".format(TARGET_USER, result["number"], result["score"]))
