import csv
import math

import seaborn as sns
import matplotlib.pyplot as plt

ages = []
repo_nums = []
follower_nums = []
commit_comment_nums = []
commit_nums = []
issue_comment_nums = []
issue_event_nums = []
issue_numbers = []
org_numbers = []
pr_comment_nums = []
pr_nums = []
collaborator_nums = []

with open('data/ready_to_ana/data_users_symfony_ready_to_analysis.csv', newline='') as csvfile:
    index = 0
    rows = csv.reader(csvfile)

    for row in rows:
        # print(row)
        if index != 0:

            # Age
            row[1] = round((int(row[1]) / 365), 4)

            # Rest of features
            columns = [2, 3, 4, 5, 6, 7, 8, 9]
            for i in columns:
                if int(row[i]) != 0:
                    row[i] = math.log(int(row[i]), 10)

            ages.append(round(int(row[1]), 3))
            repo_nums.append(round(int(row[2]), 3))
            commit_comment_nums.append(round(int(row[3]), 3))
            commit_nums.append(round(int(row[4]), 3))
            issue_comment_nums.append(round(int(row[5]), 3))
            issue_event_nums.append(round(int(row[6]), 3))
            issue_numbers.append(round(int(row[7]), 3))
            pr_comment_nums.append(round(int(row[8]), 3))
            pr_nums.append(round(int(row[9]), 3))
        index += 1

plt.hist(ages, bins=None, color='steelblue', density=True)
plt.title("Age")
plt.show()

plt.hist(repo_nums, bins=None, color='steelblue', density=True)
plt.title("Repo number")
plt.show()

plt.hist(commit_comment_nums, bins=None, color='steelblue', density=True)
plt.title("commit_comment Number")
plt.show()

plt.hist(commit_nums, bins=None, color='steelblue', density=True)
plt.title("commit_nums")
plt.show()

plt.hist(issue_comment_nums, bins=None, color='steelblue', density=True)
plt.title("issue_comment Number")
plt.show()

plt.hist(issue_event_nums, bins=None, color='steelblue', density=True)
plt.title("issue_event Number")
plt.show()

plt.hist(issue_numbers, bins=None, color='steelblue', density=True)
plt.title("issue Number")
plt.show()

plt.hist(pr_comment_nums, bins=None, color='steelblue', density=True)
plt.title("pr_comment Number")
plt.show()

plt.hist(pr_nums, bins=None, color='steelblue', density=True)
plt.title("pr Number")
plt.show()
