import Basic_Functions as bfs
import operator

REPO = "symfony"

issues = bfs.readJsonFile(name="issues_tf_idf_{}".format(REPO), folder="data/issue_text").items()

issue_profiles = {}

for id, items in issues:
    texts = {}

    # Analysis Title
    for text in items["title"]:
        if text[0] not in texts:
            texts[text[0]] = text[1]
        else:
            texts[text[0]] += text[1]
    # Analysis Body
    for text in items["body"]:
        if text[0] not in texts:
            texts[text[0]] = text[1]
        else:
            texts[text[0]] += text[1]

    texts = sorted(texts.items(), key=operator.itemgetter(1), reverse=True)

    # if len(texts) > 30:
    #     texts = texts[0:30]

    issue_profiles[id] = {
        "issue_number": items["github_issue_id"],
        "profile": texts
    }

bfs.writeJsonFile(data=issue_profiles, name="profile_issues_{}".format(REPO), folder="data/profiles")
