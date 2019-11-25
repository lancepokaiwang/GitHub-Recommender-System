import json
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx + 1))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))

# dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
# documents = dataset.data

textSet = []
excludedTextSet = ["http://", "https://", "for", "and", "or", "as", "the", "is", "are", "was", "were", "if", "be", "in",
                   "on", "at", "to", "therefore", "I", "you", "he", "she", "it", "they", "us", "we", "symfony"]

with open('data-context.json') as json_file:
    dataset = json.load(json_file)
    for data in dataset:
        dataTextSet = []
        # # ======Solution 1======
        # # print(data["issue_id"])
        # for text in str(data["title"]).split():
        #     if not any([x in text for x in excludedTextSet]):
        #         dataTextSet.append(text)
        # for text in str(data["body"]).split():
        #     if not any([x in text for x in excludedTextSet]):
        #         dataTextSet.append(text)
        # # print(dataTextSet)
        # textSet.append(dataTextSet)

        # ======Solution 2======
        for excluded in excludedTextSet:
            data["title"].replace(excluded, " ")
            data["body"].replace(excluded, " ")
        temp = data["title"] + " " + data["body"]
        textSet.append(temp)

no_features = 1000

# NMF is able to use tf-idf
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(textSet)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(textSet)
tf_feature_names = tf_vectorizer.get_feature_names()

no_topics = 10

# Run NMF
nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

# Run LDA
lda = LatentDirichletAllocation()
lda = LatentDirichletAllocation(n_components=no_topics, max_iter=100, learning_method='online', learning_offset=50., random_state=0).fit(tf)

no_top_words = 10

# display_topics(nmf, tfidf_feature_names, no_top_words)
display_topics(lda, tf_feature_names, no_top_words)

from joblib import dump, load
dump(lda, 'lda_Model.joblib')


