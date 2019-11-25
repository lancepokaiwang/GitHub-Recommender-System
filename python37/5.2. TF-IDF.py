from nltk.stem import WordNetLemmatizer
import Basic_Functions as bfs
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import *
from collections import Counter
import nltk
import math
import string
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

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
        output.append((word,count/total))
    return output

def tf_idf_document(tf_document, corpus):
    output = []
    total = len(corpus)
    for word, tf in tf_document:
        idf = math.log(total/corpus[word])
        print("word: {} total:{} count:{} idf:{}".format(word, total, corpus[word], idf))
        output.append((word, tf * idf))
    return output

def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


def idf(word, count_list):
    return math.log(len(count_list) / (n_containing(word, count_list)))


def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


issues = bfs.readJsonFile(name="issues_text_{}".format(REPO), folder="data/issue_text").items()
output_tf_idf = {}
output_dataset_processed = {}
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
corpus_title_word_list = []
corpus_body_word_list = []
corpus_title_body_word_list = []

for issue, text in issues:

    github_id = text["github_issue_id"]
    clean_title_text = clean(text["title"])
    clean_body_text = clean(text["body"])

    title_words = remove_stopwords(tokenize(clean_title_text))
    body_words = remove_stopwords(tokenize (clean_body_text))

    title_processed = lemmatize(title_words, lemmatizer)
    body_processed = lemmatize(body_words, lemmatizer)

    output_dataset_processed[issue] = {
        "title": clean_title_text,
        "body": clean_body_text,
        "github_issue_id": github_id,
        "title_processed": title_processed,
        "body_processed": body_processed,
    }

    count_title = Counter(title_processed)
    count_body = Counter(body_processed)
    count_title_body = count_title + count_body

    corpus_title_word_list.extend(list(count_title))
    corpus_body_word_list.extend(list(count_body))


    output_tf_idf[issue] = {
        "github_issue_id": github_id,
        "title": tf_document(count_title),
        "body": tf_document(count_body),
        "title_body": tf_document(count_title_body),
    }

corpus_title = Counter(corpus_title_word_list)
corpus_body = Counter(corpus_body_word_list)

bfs.writeJsonFile(output_tf_idf,"issues_tf_" + REPO,"data/issue_text")

for i, document in output_tf_idf.items():
    document["title"] = tf_idf_document(document["title"],corpus_title)
    document["body"] = tf_idf_document(document["body"],corpus_body)
    document["title_body"] = tf_idf_document(document["title_body"],corpus_title + corpus_body)

bfs.writeJsonFile(output_tf_idf,"issues_tf_idf_" + REPO,"data/issue_text")
bfs.writeJsonFile(output_dataset_processed,"processed_issues_text_" + REPO,"data/issue_text")
