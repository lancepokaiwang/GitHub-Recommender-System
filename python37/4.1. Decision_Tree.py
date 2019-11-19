import csv
import math
import pickle
from subprocess import check_call

import numpy as np
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
# -------------Decision Tree-------------
# ---------------------------------------
# ---------------------------------------
tree = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
tree.fit(x_train, y_train)

print("Decision Tree Precision: " + str(tree.score(x_test, y_test)))

# Export decision tree plot
export_graphviz(tree, out_file='user_cluster/user_tree_{}_{}c.dot'.format(REPO, CLUSTER_NUM),
                feature_names=['age', 'repos', 'commit_comments', 'commits', 'issue_comments', 'issue_events', 'issues', 'pr_comments', 'prs'],
                rounded=True, proportion=False,
                precision=2, filled=True)
check_call(['dot', '-Tpng', 'user_cluster/user_tree_{}_{}c.dot'.format(REPO, CLUSTER_NUM), '-o',
            'user_cluster/user_tree_{}_{}c.png'.format(REPO, CLUSTER_NUM)])

# save the model to disk
filename = 'models/user_tree_{}_{}c.sav'.format(REPO, CLUSTER_NUM)
pickle.dump(tree, open(filename, 'wb'))
