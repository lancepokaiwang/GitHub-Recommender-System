import json
import csv


def printDictionary(dict):
    for key in dict.keys():
        print(format(key) + ": " + format(dict[key]))


with open('data/data_users.json') as json_file:
    dataset = json.load(json_file)

    # Open CSV reader
    with open('data/data_users_ready_to_analysis_2.csv', 'w', newline='') as csvfile:
        # Create CSV writer
        writer = csv.writer(csvfile)
        # Write first row
        writer.writerow(
            ['age', 'repo_num', 'follower_num', 'commit_num', 'issue_comment_num', 'issue_event_num', 'issue_number', 'org_number', 'pr_comment_num', 'pr_num'])
        for user, profile in dataset.items():
            if int(profile['age']) >= 0:
                writer.writerow(
                    [profile['age'], profile['repo_num'], profile['follower_num'],
                     profile['commit_num'], profile['issue_comment_num'], profile['issue_event_num'],
                     profile['issue_number'], profile['org_number'], profile['pr_comment_num'], profile['pr_num']])
