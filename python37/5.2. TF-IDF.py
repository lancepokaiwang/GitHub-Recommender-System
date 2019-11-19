import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
import math
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer
import Basic_Functions as bfs

OWNER = "symfony"
REPO = "symfony"


def get_tokens(text):
    lowers = text.lower()
    # remove the punctuation using the character deletion step of translate
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    no_punctuation = lowers.translate(remove_punctuation_map)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tf(word, count):
    return count[word] / sum(count.values())


def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


def idf(word, count_list):
    return math.log(len(count_list) / (n_containing(word, count_list)))


def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


dataset = bfs.readJsonFile(name="issues_text_{}".format(REPO), folder="data/issue_text")

countlist = []


for issue, context in dataset.items():
    # Pre-process
    content = "{} {}".format(context["title"], context["body"])
    tokens = get_tokens(content)
    filtered = [w for w in tokens if not w in stopwords.words('english')]
    stemmer = PorterStemmer()
    stemmed = stem_tokens(filtered, stemmer)

    count = Counter(stemmed)
    print(count)

    countlist.append(count)

words_overall = {}
for i, count in enumerate(countlist):
    print("\n\nTop words in document {}".format(i+1))
    scores = {word: tfidf(word, count, countlist) for word in count}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:10]:
        if word not in words_overall:
            words_overall["word"] = score
        else:
            words_overall["word"] += score
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))



for word, freq in words_overall.items():
    print("{}: {}".format(word, freq))


