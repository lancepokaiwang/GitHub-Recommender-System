import json
import csv
import Basic_Functions as bfs

OWNER = "symfony"
REPO = "symfony"

dataset = bfs.readJsonFile(name="users_{}_filtered".format(REPO), folder="data")


# Open CSV reader
with open('data/data_users_{}_ready_to_analysis.csv'.format(REPO), 'w', newline='') as csvfile:
    # Create CSV writer
    writer = csv.writer(csvfile)
    # Write first row
    writer.writerow(
        ['newcomer', 'age', 'repos', 'commit_comments', 'commits', 'issue_comments', 'issue_events', 'issues', 'pr_comments', 'prs'])
    for data in dataset:
        writer.writerow(
            [1, int(data['age']), int(data['repos']), int(data['commit_comments']),
             int(data['commits']), int(data['issue_comments']), int(data['issue_events']),
             int(data['issues']), int(data['pr_comments']), int(data['prs'])])
