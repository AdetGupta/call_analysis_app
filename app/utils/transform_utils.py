import re

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def to_lowercase(text):
    return text.lower()

def remove_punctuation(text):
    return re.sub(r"[^a-zA-Z0-9\s\']", "", text)

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return filtered_tokens

def normalize_words(tokens):
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens if token.isalnum() and len(token)<30]
    return " ".join(stemmed_tokens)


def transform_text(text):
    text = to_lowercase(text)
    text = remove_punctuation(text)
    tokens = word_tokenize(text)
    tokens = remove_stopwords(tokens)
    text = normalize_words(tokens)
    return text

if __name__ == "__main__":
    text = "1232 hello there 234234@24"
    print(transform_text(text))