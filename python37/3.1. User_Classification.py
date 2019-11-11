from subprocess import check_call

import pandas
import pandas as pd
from sklearn.cluster import KMeans
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz, DecisionTreeClassifier
from subprocess import call
import pickle
from matplotlib import pyplot as plt
import math

data = []
target = []

CLUSTER_NUM = 2

with open('data/data_users_ready_to_analysis_2.csv', newline='') as csvfile:
    index = 0
    rows = csv.reader(csvfile)

    for row in rows:
        print(row)
        if index != 0 and index != 2:
            # if index != 0:
            # print(row)
            row = [int(x) for x in row]

            # Age
            row[0] = round(row[0] / 365, 2)

            # age
            # if row[0] != 0:
            #     row[0] = math.log(row[0], 10)

            # repo_num
            if row[1] != 0:
                row[1] = math.log(row[1], 2)

            # follower_num
            if row[2] != 0:
                row[2] = math.log(row[2], 2)

            # commit_num
            if row[3] != 0:
                row[3] = math.log(row[3], 2)

            # issue_comment_num
            if row[4] != 0:
                row[4] = math.log(row[4], 2)

            # issue_event_num
            if row[5] != 0:
                row[5] = math.log(row[5], 2)

            # issue_number
            if row[6] != 0:
                row[6] = math.log(row[6], 2)

            # org_number
            if row[7] != 0:
                row[7] = math.log(row[7], 2)

            # pr_comment_num
            if row[8] != 0:
                row[8] = math.log(row[8], 2)

            # pr_num
            if row[9] != 0:
                row[9] = math.log(row[9], 2)

            # print(row)

            data.append(row)
        index += 1

data_kmeans = np.array(data)
print(data)

# print(x_train)
# print(x_test)


# Use K-Means to classify 2 groups of user
kmeans = KMeans(n_clusters=CLUSTER_NUM, init='random', n_init=10, max_iter=50, tol=0.0001, precompute_distances='auto',
                verbose=0, random_state=None, copy_x=True, n_jobs=None, algorithm='elkan').fit(data_kmeans)

# print(kmeans.labels_)
target = kmeans.labels_

print(target)

print(kmeans.cluster_centers_)

# print(type(target.tolist()))
#
# data.append(target.tolist())
#
# print(data)
#
# pandas.plotting.parallel_coordinates(data, 'cluster')

# Use Decision Tree to verify whether the result is correct or not
x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3)

tree = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
tree.fit(x_train, y_train)

print("Decision Tree Precision: " + str(tree.score(x_test, y_test)))

# Export decision tree plot
export_graphviz(tree, out_file='user_cluster/user_tree_{}c.dot'.format(CLUSTER_NUM),
                feature_names=['age', 'repo_num', 'follower_num', 'commit_num', 'issue_comment_num', 'issue_event_num',
                               'issue_number', 'org_number', 'pr_comment_num', 'pr_num'],
                rounded=True, proportion=False,
                precision=2, filled=True)
check_call(['dot', '-Tpng', 'user_cluster/user_tree_{}c.dot'.format(CLUSTER_NUM), '-o',
            'user_cluster/user_tree_{}c.png'.format(CLUSTER_NUM)])

# save the model to disk
filename = 'models/user_tree_5c.sav'
pickle.dump(tree, open(filename, 'wb'))

# Use Random Forest to verify whether the result is correct or not
x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3)

forest = RandomForestClassifier(criterion='entropy', n_estimators=10, random_state=3, n_jobs=16, max_features=4,
                                max_depth=5, min_samples_leaf=2)
forest.fit(x_train, y_train)

print("Random Forest Precision: " + str(forest.score(x_test, y_test)))

# Export random forest plot
estimator = forest.estimators_[9]
export_graphviz(estimator, out_file='user_cluster/user_forest_{}c.dot'.format(CLUSTER_NUM),
                feature_names=['age', 'repo_num', 'follower_num', 'commit_num', 'issue_comment_num', 'issue_event_num',
                               'issue_number', 'org_number', 'pr_comment_num', 'pr_num'],
                rounded=True, proportion=False,
                precision=2, filled=True)
call(['dot', '-Tpng', 'user_cluster/user_forest_{}c.dot'.format(CLUSTER_NUM), '-o',
      'user_cluster/user_forest_{}c.png'.format(CLUSTER_NUM), '-Gdpi=600'])

# save the model to disk
filename = 'models/user_forest_5c.sav'
pickle.dump(forest, open(filename, 'wb'))

# Extra: Load model from disk
# loaded_model = pickle.load(open('models/user_forest.sav', 'rb'))
# result = loaded_model.score(X_test, Y_test)
