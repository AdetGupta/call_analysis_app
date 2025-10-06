import re

from nltk.stem import PorterStemmer


def to_lowercase(text):
    return text.lower()

def remove_stopwords(text):
    stop_words = set()
    with open('./data/stopwords_eng', 'r', encoding='utf-8') as f:
        for line in f:
            stop_words.add(line.strip())

    tokens = text.split()
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return " ".join(filtered_tokens)

def remove_punctuation(text):
    return re.sub(r"[^a-zA-Z0-9\s\-\']", "", text)

def normalize_words(text):
    stemmer = PorterStemmer()
    tokens = text.split()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return " ".join(stemmed_tokens)

def transform_text(text):
    text = to_lowercase(text)
    text = remove_punctuation(text)
    text = remove_stopwords(text)
    text = normalize_words(text)
    return text

if __name__ == "__main__":
    text = "Hello there!, I've was borning but I was thinking about this history on 08-06-2004."
    print(transform_text(text))