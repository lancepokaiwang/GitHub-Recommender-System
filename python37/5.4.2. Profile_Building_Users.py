import Basic_Functions as bfs
import operator

REPO = "symfony"

issues = bfs.readJsonFile(name="users_tf_idf_{}".format(REPO), folder="data/user_text").items()

issue_profiles = {}

for id, items in issues:
    texts = {}

    # Analysis commit_comments_processed
    for text in items["commit_comments"]:
        if text[0] not in texts:
            texts[text[0]] = text[1]
        else:
            texts[text[0]] += text[1]
    # Analysis commits_processed
    for text in items["commits"]:
        if text[0] not in texts:
            texts[text[0]] = text[1]
        else:
            texts[text[0]] += text[1]
    # Analysis issue_comments_processed
    for text in items["issue_comments"]:
        if text[0] not in texts:
            texts[text[0]] = text[1]
        else:
            texts[text[0]] += text[1]
    # Analysis pr_comments_processed
    for text in items["pr_comments"]:
        if text[0] not in texts:
            texts[text[0]] = text[1]
        else:
            texts[text[0]] += text[1]
    # Analysis prs_processed
    for text in items["prs"]:
        if text[0] not in texts:
            texts[text[0]] = text[1]
        else:
            texts[text[0]] += text[1]

    texts = sorted(texts.items(), key=operator.itemgetter(1), reverse=True)

    # if len(texts) > 30:
    #     texts = texts[0:30]

    issue_profiles[id] = {
        "profile": texts
    }

bfs.writeJsonFile(data=issue_profiles, name="profile_users_{}".format(REPO), folder="data/profiles")
