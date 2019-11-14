import csv
import math
import pickle
from subprocess import check_call
from unittest.mock import call

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
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
                row[1] = 0

                # repo_num
                # if int(row[2]) != 0:
                #     row[2] = math.log(int(row[2]), 10)

                # follower_num
                if int(row[3]) != 0:
                    row[3] = math.log(int(row[3]), 2)

                # commit_comment_num
                if int(row[4]) != 0:
                    row[4] = math.log(int(row[4]), 10)

                # commit_num
                if int(row[5]) != 0:
                    row[5] = math.log(int(row[5]), 10)

                # issue_comment_num
                if int(row[6]) != 0:
                    row[6] = math.log(int(row[6]), 10)

                # issue_event_num
                if int(row[7]) != 0:
                    row[7] = math.log(int(row[7]), 10)

                # issue_number
                if int(row[8]) != 0:
                    row[8] = math.log(int(row[8]), 10)

                # org_number
                # if int(row[9]) != 0:
                #     row[9] = math.log(int(row[9]), 10)

                # pr_comment_num
                if int(row[10]) != 0:
                    row[10] = math.log(int(row[10]), 10)

                # pr_num
                if int(row[11]) != 0:
                    row[11] = math.log(int(row[11]), 2)

                # collaborator_num
                # if int(row[12]) != 0:
                #     row[12] = math.log(int(row[12]), 10)

                data.append(row[1:12])
        index += 1


# Load Cluster Model
filename = 'models/user_kmeans_{}c.sav'.format(CLUSTER_NUM)
clustering = joblib.load(filename)

target = clustering.labels_


x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3)

# ---------------------------------------
# ---------------------------------------
# -------------Random Forest-------------
# ---------------------------------------
# ---------------------------------------
# Use Random Forest to verify whether the result is correct or not
x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3)

forest = RandomForestClassifier(criterion='entropy', n_estimators=10, random_state=3, n_jobs=16, max_features=4,
                                max_depth=3, min_samples_leaf=2)
forest.fit(x_train, y_train)

print("Random Forest Precision: " + str(forest.score(x_test, y_test)))

# Export random forest plot
estimator = forest.estimators_[9]
export_graphviz(estimator, out_file='user_cluster/user_forest_{}c.dot'.format(CLUSTER_NUM),
                feature_names=['repo_num', 'follower_num', 'commit_comment_num', 'commit_num',
                               'issue_comment_num', 'issue_event_num', 'issue_number', 'org_number', 'pr_comment_num',
                               'pr_num', 'collaborator_num'],
                rounded=True, proportion=False,
                precision=2, filled=True)
call(['dot', '-Tpng', 'user_cluster/user_forest_{}c.dot'.format(CLUSTER_NUM), '-o',
      'user_cluster/user_forest_{}c.png'.format(CLUSTER_NUM), '-Gdpi=600'])

# save the model to disk
filename = 'models/user_forest_{}c.sav'.format(CLUSTER_NUM)
pickle.dump(forest, open(filename, 'wb'))