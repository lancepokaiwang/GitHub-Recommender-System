from sklearn.cluster import KMeans
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz, DecisionTreeClassifier
from subprocess import call, check_call
import pickle
from sklearn.externals import joblib
import math

data_original = []
data = []
target = []

CLUSTER_NUM = 3
REPO = "symfony"

with open('data/ready_to_ana/data_users_{}_ready_to_analysis_2.csv'.format(REPO), newline='') as csvfile:
    index = 0
    rows = csv.reader(csvfile)

    for row in rows:
        # print(row)
        if index != 0:
            # if index != 0:
            # print(row)
            # row = [int(x) for x in row]

            # Newcomer
            row[0] = int(row[0])

            # Age
            row[1] = round((int(row[1]) / 365), 4)

            # Rest of features
            columns = [2, 3, 4, 5, 6, 7, 8, 9]
            for i in columns:
                if int(row[i]) != 0:
                    row[i] = math.log(int(row[i]), 10)

            data.append(row[1:-1])

            data_original.append(row)

        index += 1

data_kmeans = np.array(data)
print(data)

# ---------------------------------------
# ---------------------------------------
# ----------------KMeans-----------------
# ---------------------------------------
# ---------------------------------------

best_acc = 0
best_results = {}

for i in range(100):
    kmeans = KMeans(n_clusters=CLUSTER_NUM, init='random', n_init=100, max_iter=100, tol=0.0001,
                    precompute_distances=True,
                    verbose=0, random_state=None, copy_x=True, n_jobs=None, algorithm='elkan').fit(data_kmeans)

    # print(kmeans.labels_)
    target = kmeans.labels_

    # print(target)

    # print(kmeans.cluster_centers_)

    # save the model to disk
    filename = 'models/user_kmeans_{}_{}c.sav'.format(REPO, CLUSTER_NUM)
    joblib.dump(kmeans, filename)

    # Data Validation
    if CLUSTER_NUM == 2:
        target = target.tolist()
        results = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
        for i in range(len(data_original)):
            # print(data_original[i])
            # print(target[i])
            if data_original[i][0] == 1:
                if 1 == target[i]:
                    results["TP"] += 1
                elif 0 == target[i]:
                    results["FN"] += 1
            elif data_original[i][0] == 0:
                if 0 == target[i]:
                    results["TN"] += 1
                elif 1 == target[i]:
                    results["FP"] += 1
        # print(results)
        accuracy = ((results["TP"] + results["TN"]) / (results["TP"] + results["TN"] + results["FP"] + results["FN"]))
        # print(accuracy)
        if accuracy > best_acc:
            best_acc = accuracy
            best_results = results

print(best_acc)
print(best_results)

# target = target.tolist()

# Open CSV reader
with open('data/cluster_result/data_users_{}_cluster_with_results_{}c.csv'.format(REPO, CLUSTER_NUM), 'w', newline='') as csvfile:
    # Create CSV writer
    writer = csv.writer(csvfile)
    # Write first row
    writer.writerow(
        ['result', 'newcomer', 'age', 'repos', 'commit_comments', 'commits', 'issue_comments', 'issue_events', 'issues',
         'pr_comments', 'prs'])

    i = 0
    while i < len(target):
        writer.writerow(
            [target[i], data_original[i][0], data_original[i][1], data_original[i][2], data_original[i][3],
             data_original[i][4],
             data_original[i][5], data_original[i][6], data_original[i][7],
             data_original[i][8], data_original[i][9]])
        i += 1

# Only include results
with open('data/cluster_result/data_users_{}_cluster_results_only_{}c.csv'.format(REPO, CLUSTER_NUM), 'w', newline='') as csvfile:
    # Create CSV writer
    writer = csv.writer(csvfile)
    # Write first row
    writer.writerow(
        ['newcomer', 'age', 'repos', 'commit_comments', 'commits', 'issue_comments', 'issue_events', 'issues',
         'pr_comments', 'prs'])

    i = 0
    while i < len(target):
        writer.writerow(
            [target[i], data_original[i][1], data_original[i][2], data_original[i][3],
             data_original[i][4],
             data_original[i][5], data_original[i][6], data_original[i][7],
             data_original[i][8], data_original[i][9]])
        i += 1
