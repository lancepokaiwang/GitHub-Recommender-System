import json
import csv
import Basic_Functions as bfs

OWNER = "symfony"
REPO = "symfony"

dataset = bfs.readJsonFile(name="users_{}_filtered".format(REPO), folder="data/user_filtered")


# Open CSV reader
with open('data/ready_to_ana/data_users_{}_ready_to_analysis.csv'.format(REPO), 'w', newline='') as csvfile:
    # Create CSV writer
    writer = csv.writer(csvfile)
    # Write first row
    writer.writerow(
        ['newcomer', 'age', 'repos', 'commit_comments', 'commits', 'issue_comments', 'issue_events', 'issues', 'pr_comments', 'prs'])
    for data in dataset:
        if int(data['age']) >= 0:
            writer.writerow(
                [1, int(data['age']), int(data['repos']), int(data['commit_comments']),
                 int(data['commits']), int(data['issue_comments']), int(data['issue_events']),
                 int(data['issues']), int(data['pr_comments']), int(data['prs'])])

# Open CSV reader
with open('data/ready_to_ana/data_users_{}_ready_to_analysis_2.csv'.format(REPO), 'w', newline='') as csvfile:
    # Create CSV writer
    writer = csv.writer(csvfile)
    # Write first row
    writer.writerow(
        ['newcomer', 'age', 'repos', 'commit_comments', 'commits', 'issue_comments', 'issue_events', 'issues', 'pr_comments', 'prs'])
    former = {}
    for data in dataset:
        if int(data['age']) >= 0:
            print(former)
            print(data)
            if not former:
                writer.writerow(
                    [1, int(data['age']), int(data['repos']), int(data['commit_comments']),
                     int(data['commits']), int(data['issue_comments']), int(data['issue_events']),
                     int(data['issues']), int(data['pr_comments']), int(data['prs'])])
                former = data
                print("saved")
            elif former['age'] != data['age'] or former['repos'] != data['repos'] or former['commit_comments'] != data['commit_comments'] or former['commits'] != data['commits'] or former['issue_comments'] != data['issue_comments'] or former['issue_events'] != data['issue_events'] or former['issues'] != data['issues'] or former['pr_comments'] != data['pr_comments'] or former['prs'] != data['prs']:
                writer.writerow(
                    [1, int(data['age']), int(data['repos']), int(data['commit_comments']),
                     int(data['commits']), int(data['issue_comments']), int(data['issue_events']),
                     int(data['issues']), int(data['pr_comments']), int(data['prs'])])
                former = data
                print("saved")
            else:
                print("skipped")
            print("=======================")
