from nltk.stem import WordNetLemmatizer
import Basic_Functions as bfs
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import *
from collections import Counter
import nltk
import math
import string
from nltk.corpus import stopwords

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

OWNER = "symfony"
REPO = "symfony"


def clean(text):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    return text.lower().translate(remove_punctuation_map)


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    return tokens


def remove_stopwords(tokens):
    return [w for w in tokens if not w in stopwords.words('english')]


def lemmatize(tokens, lemmatizer):
    output = []
    for token in tokens:
        output.append(lemmatizer.lemmatize(token))
    return output


def stem(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tf(word, count):
    return count[word] / sum(count.values())


def tf_document(document_count):
    output = []
    total = len(document_count)
    for word, count in document_count.items():
        output.append((word, count / total))
    return output


def tf_idf_document(tf_document, corpus):
    output = []
    total = len(corpus)
    for word, tf in tf_document:
        idf = math.log(total / corpus[word])
        print("word: {} total:{} count:{} idf:{}".format(word, total, corpus[word], idf))
        output.append((word, tf * idf))
    return output


def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


def idf(word, count_list):
    return math.log(len(count_list) / (n_containing(word, count_list)))


def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


users = bfs.readJsonFile(name="users_{}_textual".format(REPO), folder="data/user_text").items()

output_tf_idf = {}
output_dataset_processed = {}
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

corpus_ccs_word_list = []
corpus_commits_word_list = []
corpus_ics_word_list = []
corpus_prcs_word_list = []
corpus_prs_word_list = []
# corpus_title_body_word_list = []

PRINT_EXAMPLE = True

for userID, items in users:
    print(userID)

    user_id = userID

    # commit_comments
    ccs = ""
    ccs_processed = []
    for cc in items["commit_comments"]:
        clean_context = clean(cc)
        ccs += clean_context + " "
    context_words = remove_stopwords(tokenize(ccs))
    context_processed = lemmatize(context_words, lemmatizer)
    ccs_processed = context_processed

    # commits
    commits = ""
    commits_processed = []
    for commit in items["commits"]:
        clean_context = clean(commit)
        commits += clean_context + " "
    context_words = remove_stopwords(tokenize(commits))
    context_processed = lemmatize(context_words, lemmatizer)
    commits_processed = context_processed

    # issue_comments
    ics = ""
    ics_processed = []
    for ic in items["issue_comments"]:
        clean_context = clean(ic)
        ics += clean_context + " "
    context_words = remove_stopwords(tokenize(ics))
    context_processed = lemmatize(context_words, lemmatizer)
    ics_processed = context_processed

    # pr_comments
    prcs = ""
    prcs_processed = []
    for prc in items["pr_comments"]:
        clean_context = clean(prc)
        prcs += clean_context + " "
    context_words = remove_stopwords(tokenize(prcs))
    context_processed = lemmatize(context_words, lemmatizer)
    prcs_processed = context_processed

    # prs
    prs = ""
    prs_processed = []
    for pr in items["prs"]:
        clean_context = clean(pr["title"]) + " " + clean(pr["body"])
        prs += clean_context
    context_words = remove_stopwords(tokenize(clean_context))
    context_processed = lemmatize(context_words, lemmatizer)
    prs_processed = context_processed

    output_dataset_processed[userID] = {
        "commit_comments": ccs,
        "commit_comments_processed": ccs_processed,
        "commits": commits,
        "commits_processed": commits_processed,
        "issue_comments": ics,
        "issue_comments_processed": ics_processed,
        "pr_comments": prcs_processed,
        "pr_comments_processed": prcs_processed,
        "prs": prs,
        "prs_processed": prs_processed,
    }

    if PRINT_EXAMPLE:
        bfs.writeJsonFile(output_dataset_processed, "processed_user_text_{}_example".format(REPO), "data/user_text")
        PRINT_EXAMPLE = False


    # TF works
    count_ccs = Counter(ccs_processed)
    count_commits = Counter(commits_processed)
    count_ics = Counter(ics_processed)
    count_prcs = Counter(prcs_processed)
    count_prs = Counter(prs_processed)
    count_all = count_ccs + count_commits + count_ics + count_prcs + count_prs

    corpus_ccs_word_list.extend(list(count_ccs))
    corpus_commits_word_list.extend(list(count_commits))
    corpus_ics_word_list.extend(list(count_ics))
    corpus_prcs_word_list.extend(list(count_prcs))
    corpus_prs_word_list.extend(list(count_prs))

    # corpus_title_word_list.extend(list(count_title))
    # corpus_body_word_list.extend(list(count_body))

    output_tf_idf[userID] = {
        "commit_comments": tf_document(count_ccs),
        "commits": tf_document(count_commits),
        "issue_comments": tf_document(count_ics),
        "pr_comments": tf_document(count_prcs),
        "prs": tf_document(count_prs),
        "all": tf_document(count_all),
    }

corpus_ccs = Counter(corpus_ccs_word_list)
corpus_commits = Counter(corpus_commits_word_list)
corpus_ics = Counter(corpus_ics_word_list)
corpus_pres = Counter(corpus_prcs_word_list)
corpus_prs = Counter(corpus_prs_word_list)

bfs.writeJsonFile(output_tf_idf, "users_tf_" + REPO, "data/user_text")

for i, document in output_tf_idf.items():
    document["commit_comments"] = tf_idf_document(document["commit_comments"], corpus_ccs)
    document["commits"] = tf_idf_document(document["commits"], corpus_commits)
    document["issue_comments"] = tf_idf_document(document["issue_comments"], corpus_ics)
    document["pr_comments"] = tf_idf_document(document["pr_comments"], corpus_pres)
    document["prs"] = tf_idf_document(document["prs"], corpus_prs)
    document["all"] = tf_idf_document(document["all"],
                                      corpus_ccs + corpus_commits + corpus_ics + corpus_pres + corpus_prs)

bfs.writeJsonFile(output_tf_idf, "users_tf_idf_" + REPO, "data/user_text")
bfs.writeJsonFile(output_dataset_processed, "processed_user_text_" + REPO, "data/user_text")
