import pickle
import re
import os

import pandas as pd
import numpy as np

# Opening model from saved file
model_path = os.path.abspath('sentiment_analysis/sentiment_model.sav')
model = pickle.load(open(model_path, 'rb'))

# Opening word embeddings
word_embedding_path = os.path.abspath('sentiment_analysis/datascience.h5')
with pd.HDFStore(word_embedding_path) as hdf:
    word_embeddings = pd.read_hdf(hdf, key='embeddings')

# Opening list of stop words
stop_words_path = os.path.abspath('sentiment_analysis/stop_words.txt')
file = open(stop_words_path, "r")
stop_words = file.readlines()
file.close()
stop_words = [word.strip('\n') for word in stop_words]
candidate_names = ['joe', 'biden', 'donald', 'trump']
stop_words.extend(candidate_names)

print('Sentiment model and word embeddings loaded and ready to analyze!')


def text_to_sentiment(text):
    """
    Determines the sentiment of a given text

    :param text: Text from a Tweet
    :return: Sentiment rating along with list of tokens from the text
    """
    # Using regex to clean text from '@' tags and links
    cleaned_text = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split()
    tokens = [token.lower() for token in cleaned_text if not token.lower() in stop_words]

    # Obtaining word embeddings of all tokens found
    vectors = word_embeddings.reindex(tokens).dropna()

    # No valid words were present in the text
    if len(vectors) == 0:
        return 0, []

    predictions = model.predict_log_proba(vectors)
    score = np.mean(predictions[:, 1] - predictions[:, 0])
    return score, tokens
