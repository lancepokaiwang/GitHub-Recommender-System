from subprocess import check_call
from sklearn.cluster import KMeans
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz, DecisionTreeClassifier
from subprocess import call
import pickle

data = []
target = []

with open('data/data_users_ready_to_analysis.csv', newline='') as csvfile:
    index = 0
    rows = csv.reader(csvfile)

    for row in rows:
        if index != 0 and index != 2:
            # print(row)
            data.append(row)
        index += 1

data = np.array(data)
# print(data)

# print(x_train)
# print(x_test)


# Use K-Means to classify 2 groups of user
kmeans = KMeans(n_clusters=2, init='random', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto',
                verbose=0, random_state=None, copy_x=True, n_jobs=None, algorithm='auto').fit(data)

print(kmeans.labels_)
target = kmeans.labels_

# Use Decision Tree to verify whether the result is correct or not
x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3)

tree = DecisionTreeClassifier(criterion='entropy', max_depth=13, random_state=0)
tree.fit(x_train, y_train)

print("Decision Tree Precision: " + str(tree.score(x_test, y_test)))

# Export decision tree plot
export_graphviz(tree, out_file='data/user_tree.dot',
                feature_names=['age', 'repo_num', 'follower_num', 'commit_comment_num', 'commit_num',
                               'issue_comment_num', 'issue_event_num', 'issue_number', 'org_number', 'pr_comment_num',
                               'pr_num', 'collaborator_num'],
                rounded=True, proportion=False,
                precision=2, filled=True)
check_call(['dot', '-Tpng', 'data/user_tree.dot', '-o', 'data/user_tree.png'])

# save the model to disk
filename = 'models/user_tree.sav'
pickle.dump(tree, open(filename, 'wb'))

# Use Random Forest to verify whether the result is correct or not
x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3)

forest = RandomForestClassifier(criterion='entropy', n_estimators=10, random_state=3, n_jobs=16)
forest.fit(x_train, y_train)

print("Random Forest Precision: " + str(forest.score(x_test, y_test)))

# Export random forest plot
estimator = forest.estimators_[5]
export_graphviz(estimator, out_file='data/user_forest.dot',
                feature_names=['age', 'repo_num', 'follower_num', 'commit_comment_num', 'commit_num',
                               'issue_comment_num', 'issue_event_num', 'issue_number', 'org_number', 'pr_comment_num',
                               'pr_num', 'collaborator_num'],
                rounded=True, proportion=False,
                precision=2, filled=True)
call(['dot', '-Tpng', 'data/user_forest.dot', '-o', 'data/user_forest.png', '-Gdpi=600'])

# save the model to disk
filename = 'models/user_forest.sav'
pickle.dump(forest, open(filename, 'wb'))

# Extra: Load model from disk
# loaded_model = pickle.load(open('models/user_forest.sav', 'rb'))
# result = loaded_model.score(X_test, Y_test)