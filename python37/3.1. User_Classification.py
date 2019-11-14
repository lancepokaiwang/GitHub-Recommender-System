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

CLUSTER_NUM = 2

with open('data/data_users_ready_to_analysis_2.csv', newline='') as csvfile:
    index = 0
    rows = csv.reader(csvfile)

    for row in rows:
        # print(row)
        if index != 0:
            # if index != 0:
            # print(row)
            # row = [int(x) for x in row]

            if int(row[3]) < 3000:
                # Newcomer
                # print(row[0])

                if row[0] == 'True':
                    row[0] = bool(1)
                elif row[0] == 'False':
                    row[0] = bool(0)
                row[0] = int(row[0])

                # Age
                # row[1] = round(int(row[1]) / 365, 2)
                row[1] = int(row[1]) / 365
                if int(row[1]) != 0:
                    row[1] = math.log(int(row[1]), 2)

                # repo_num
                if int(row[2]) != 0:
                    row[2] = math.log(int(row[2]), 2)

                # follower_num
                # if int(row[3]) != 0:
                #     row[3] = math.log(int(row[3]), 2)
                row[3] = 0

                # commit_comment_num
                if int(row[4]) != 0:
                    row[4] = math.log(int(row[4]), 2)

                # commit_num
                if int(row[5]) != 0:
                    row[5] = math.log(int(row[5]), 2)

                # issue_comment_num
                if int(row[6]) != 0:
                    row[6] = math.log(int(row[6]), 2)

                # issue_event_num
                if int(row[7]) != 0:
                    row[7] = math.log(int(row[7]), 2)

                # issue_number
                if int(row[8]) != 0:
                    row[8] = math.log(int(row[8]), 2)

                # org_number
                if int(row[9]) != 0:
                    row[9] = math.log(int(row[9]), 2)

                # pr_comment_num
                if int(row[10]) != 0:
                    row[10] = math.log(int(row[10]), 2)

                # pr_num
                if int(row[11]) != 0:
                    row[11] = math.log(int(row[11]), 2)

                # collaborator_num
                if int(row[12]) != 0:
                    row[12] = math.log(int(row[12]), 2)

                data.append(row[1:12])
                # data.append(row[2:12])
                # data.append([row[1], row[6], row[7], row[8]])
                # data.append([row[6], row[7], row[8]])
                # data.append([row[1], row[10], row[11]])
                # data.append([row[10], row[11]])
                # data.append([row[1], row[6], row[7], row[8], row[10], row[11]])
                # data.append([row[6], row[7], row[8], row[10], row[11]])


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
    filename = 'models/user_kmeans_{}c.sav'.format(CLUSTER_NUM)
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
with open('data/data_users_cluster_with_results.csv', 'w', newline='') as csvfile:
    # Create CSV writer
    writer = csv.writer(csvfile)
    # Write first row
    writer.writerow(
        ['result', 'newcomer', 'age', 'repo_num', 'follower_num', 'commit_comment_num', 'commit_num', 'issue_comment_num', 'issue_event_num', 'issue_number', 'org_number', 'pr_comment_num', 'pr_num', 'collaborator_num'])

    i = 0
    while i < len(target):
        writer.writerow(
            [target[i], data_original[i][0], data_original[i][1], data_original[i][2], data_original[i][3], data_original[i][4],
             data_original[i][5], data_original[i][6], data_original[i][7],
             data_original[i][8], data_original[i][9], data_original[i][10], data_original[i][11], data_original[i][12]])
        i += 1
