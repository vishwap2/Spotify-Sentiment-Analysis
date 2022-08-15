from distutils.command.clean import clean
from tracemalloc import stop
import nltk

nltk.download('punkt')
nltk.download('twitter_samples')
nltk.download('wordnet') # lexical database for determing words' bases
nltk.download('averaged_perceptron_tagger') # determines context of word in sentence
nltk.download('omw-1.4')
nltk.download('stopwords') # stop words library
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import NaiveBayesClassifier

import re
import string
import random

def tokenize_train():
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    p_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    n_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')
    return positive_tweets, negative_tweets, text, p_tweet_tokens, n_tweet_tokens

def normalize_tokens(tweet_tokens):
    # lemmatization - groups together different inflected words
    # -> outputs a lemma
    # tradeoff between lemmatization and stemming - speed
    # before lemmatization, determine context of word in text through tagging algorithm
    # -> tagging determines position of word in sentence
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words('english')
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        token = lemmatizer.lemmatize(token, pos)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in string.punctuation and token not in stop_words:
            token = token.lower()
            cleaned_tokens.append(token)
        # lemmatizes word with position retrieved from pos tag function
    return cleaned_tokens

def convertToDict(all_tokens):
    for tweet_tokens in all_tokens:
        yield dict([token, True] for token in tweet_tokens)

def buildClassifier():
    _, _, _, p_tweet_tokens, n_tweet_tokens = tokenize_train()
    p_tweet_tokens_clean = []
    n_tweet_tokens_clean = []
    for token in p_tweet_tokens:
        p_tweet_tokens_clean.append(normalize_tokens(token))
    for token in n_tweet_tokens:
        n_tweet_tokens_clean.append(normalize_tokens(token))

    p_tokens_model = convertToDict(p_tweet_tokens_clean)
    n_tokens_model = convertToDict(n_tweet_tokens_clean)

    # split data set into training and testing
    p_dataset = [(tweet_dict, "Positive") for tweet_dict in p_tokens_model]
    n_dataset = [(tweet_dict, "Negative") for tweet_dict in n_tokens_model]
    dataset = p_dataset + n_dataset
    random.shuffle(dataset)
    train_data = dataset[:7000]

    # train model
    classifier = NaiveBayesClassifier.train(train_data)
    return classifier
