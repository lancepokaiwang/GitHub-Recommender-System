import json
import csv


def printDictionary(dict):
    for key in dict.keys():
        print(format(key) + ": " + format(dict[key]))


with open('data/data_users_2.json') as json_file:
    dataset = json.load(json_file)

    # Open CSV reader
    with open('data/data_users_ready_to_analysis_2.csv', 'w', newline='') as csvfile:
        # Create CSV writer
        writer = csv.writer(csvfile)
        # Write first row
        writer.writerow(
            ['newcomer', 'age', 'repo_num', 'follower_num', 'commit_comment_num', 'commit_num', 'issue_comment_num', 'issue_event_num', 'issue_number', 'org_number', 'pr_comment_num', 'pr_num', 'collaborator_num'])
        for profile in dataset:
            if int(profile['age']) >= 0:
                writer.writerow(
                    [profile['newcomer'], profile['age'], profile['repo_num'], profile['follower_num'], profile['commit_comment_num'],
                     profile['commit_num'], profile['issue_comment_num'], profile['issue_event_num'],
                     profile['issue_number'], profile['org_number'], profile['pr_comment_num'], profile['pr_num'], profile['collaborator_num']])
