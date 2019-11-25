import csv
import math
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.metrics import pairwise_distances
from sklearn.cluster import KMeans

reference = np.random.rand(100, 2)
plt.figure(figsize=(12, 3))

data = []
k_max = 6
CLUSTER_NUM = 2
REPO = "symfony"

with open('data/ready_to_ana/data_users_{}_ready_to_analysis_2.csv'.format(REPO), newline='') as csvfile:
    index = 0
    rows = csv.reader(csvfile)


    for row in rows:
        # print(row)
        if index != 0:
            # Newcomer
            row[0] = int(row[0])

            # Age
            row[1] = round((int(row[1]) / 365), 4)

            data.append(row[1:-1])
        index += 1

data = preprocessing.scale(data)
data_kmeans = np.array(data)


# print(data_kmeans)


# for k in range(1, 6):
#     kmeans = KMeans(n_clusters=k)
#     a = kmeans.fit_predict(reference)
#     plt.subplot(1, 5, k)
#     plt.scatter(reference[:, 0], reference[:, 1], c=a)
#     plt.xlabel('k=' + str(k))
# plt.tight_layout()
# plt.show()

# plt.figure(figsize=(12, 3))
# for k in range(1,6):
#     kmeans = KMeans(n_clusters=k)
#     a = kmeans.fit_predict(data_kmeans)
#     plt.subplot(1,5,k)
#     plt.scatter(data_kmeans[:, 0], data_kmeans[:, 1], c=a)
#     plt.xlabel('k='+str(k))
# plt.tight_layout()
# plt.show()

def compute_inertia(a, X):
    W = [np.mean(pairwise_distances(X[a == c, :])) for c in np.unique(a)]
    return np.mean(W)


def compute_gap(clustering, k_max=10, n_references=5):
    reference_inertia = []
    for k in range(1, k_max + 1):
        local_inertia = []
        for _ in range(n_references):
            clustering.n_clusters = k
            assignments = clustering.fit_predict(reference)
            local_inertia.append(compute_inertia(assignments, reference))
        reference_inertia.append(np.mean(local_inertia))
    ondata_inertia = []
    for k in range(1, k_max + 1):
        clustering = KMeans(n_clusters=k, init='random', n_init=10, max_iter=10000, tol=0.0001,
                       precompute_distances='auto',
                       verbose=0, random_state=None, copy_x=True, n_jobs=None, algorithm='elkan')
        # clustering.n_clusters = k
        assignments = clustering.fit_predict(data_kmeans)
        ondata_inertia.append(compute_inertia(assignments, data_kmeans))
    gap = np.log(reference_inertia) - np.log(ondata_inertia)
    return gap, np.log(reference_inertia), np.log(ondata_inertia)


gap, reference_inertia, ondata_inertia = compute_gap(clustering=KMeans(), k_max=6)

plt.plot(range(1, k_max + 1), reference_inertia,
         '-o', label='reference')
plt.plot(range(1, k_max + 1), ondata_inertia,
         '-o', label='data')
plt.xlabel('k')
plt.ylabel('log(inertia)')
plt.show()

plt.plot(range(1, k_max + 1), gap, '-o')
plt.ylabel('gap')
plt.xlabel('k')
plt.show()
