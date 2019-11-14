import csv
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



with open('data/data_users_ready_to_analysis_2.csv', newline='') as csvfile:
    index = 0
    rows = csv.reader(csvfile)

    for row in rows:
        # print(row)
        if index != 0:
            ages.append(round(int(row[1]) / 365, 2))
            repo_nums.append(round(int(row[2]), 3))
            follower_nums.append(round(int(row[3]), 3))
            commit_comment_nums.append(round(int(row[4]), 3))
            commit_nums.append(round(int(row[5]), 3))
            issue_comment_nums.append(round(int(row[6]), 3))
            issue_event_nums.append(round(int(row[7]), 3))
            issue_numbers.append(round(int(row[8]), 3))
            org_numbers.append(round(int(row[9]), 3))
            pr_comment_nums.append(round(int(row[10]), 3))
            pr_nums.append(round(int(row[11]), 3))
            collaborator_nums.append(round(int(row[12]), 3))
        index += 1

plt.hist(ages, bins=50, color='steelblue', density=True)
plt.title("Age")
plt.show()

plt.hist(repo_nums, bins=50, color='steelblue', density=True)
plt.title("Repo number")
plt.show()

plt.hist(follower_nums, bins=50, color='steelblue', density=True)
plt.title("follower Number")
plt.show()

plt.hist(commit_comment_nums, bins=50, color='steelblue', density=True)
plt.title("commit_comment Number")
plt.show()

plt.hist(commit_nums, bins=50, color='steelblue', density=True)
plt.title("commit_nums")
plt.show()

plt.hist(issue_comment_nums, bins=50, color='steelblue', density=True)
plt.title("issue_comment Number")
plt.show()

plt.hist(issue_event_nums, bins=50, color='steelblue', density=True)
plt.title("issue_event Number")
plt.show()

plt.hist(issue_numbers, bins=50, color='steelblue', density=True)
plt.title("issue Number")
plt.show()

plt.hist(org_numbers, bins=50, color='steelblue', density=True)
plt.title("org Number")
plt.show()

plt.hist(pr_comment_nums, bins=50, color='steelblue', density=True)
plt.title("pr_commen Number")
plt.show()

plt.hist(pr_nums, bins=50, color='steelblue', density=True)
plt.title("pr Number")
plt.show()

plt.hist(collaborator_nums, bins=50, color='steelblue', density=True)
plt.title("Collaborator Number")
plt.show()

