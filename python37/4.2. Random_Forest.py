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
REPO = "symfony"

with open('data/cluster_result/data_users_{}_cluster_results_only_{}c.csv'.format(REPO, CLUSTER_NUM), newline='') as csvfile:
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
            # row[1] = round((int(row[1]) / 365), 4)

            data.append(row[1:12])
        index += 1


# Load Cluster Model
filename = 'models/user_kmeans_{}_{}c.sav'.format(REPO, CLUSTER_NUM)
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
export_graphviz(estimator, out_file='user_cluster/user_forest_{}_{}c.dot'.format(REPO, CLUSTER_NUM),
                feature_names=['age', 'repos', 'commit_comments', 'commits', 'issue_comments', 'issue_events', 'issues', 'pr_comments', 'prs'],
                rounded=True, proportion=False,
                precision=2, filled=True)
call(['dot', '-Tpng', 'user_cluster/user_forest_{}_{}c.dot'.format(REPO, CLUSTER_NUM), '-o',
      'user_cluster/user_forest_{}_{}c.png'.format(REPO, CLUSTER_NUM), '-Gdpi=600'])

# save the model to disk
filename = 'models/user_forest_{}_{}c.sav'.format(REPO, CLUSTER_NUM)
pickle.dump(forest, open(filename, 'wb'))
