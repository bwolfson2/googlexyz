import spacy
# Word tokenization
from spacy.lang.en import English
import string
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import pandas as pd
import numpy as np

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en_core_web_sm')

#  Create our list of stopwords
stop_words = spacy.lang.en.stop_words.STOP_WORDS

# Load English tokenizer, tagger, parser, NER and word vectors
parser = English()

def clean_text(text):
    # Removing spaces and converting text into lowercase
    trans = str.maketrans( string.punctuation,' '*len(string.punctuation))
    text = text.translate(trans)
    return text.strip().lower()

# Creating our tokenizer function
def spacy_tokenizer(sentence):
    sentence = clean_text(sentence)
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]

    # Removing stop words
    mytokens = [ word for word in mytokens if word not in stop_words]

    mytokens = [word for word in mytokens if len(word) > 1 ]
    # return preprocessed list of tokens
    return mytokens



def get_tfidf_mat(sentences):
    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.95, min_df=2, max_features=30, stop_words="english", strip_accents="ascii",tokenizer = spacy_tokenizer
    )
    weights = tfidf_vectorizer.fit_transform(sentences)
    return weights,tfidf_vectorizer.get_feature_names()

def get_weighted_score(tfidf_mat,words):
    doc = nlp(" ".join(words))
    a = np.array([i.vector for i in doc])
    embeddings = (tfidf_mat @ a)
    return embeddings


