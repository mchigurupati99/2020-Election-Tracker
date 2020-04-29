import pickle

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Open word embeddings and positive and negative word list
with pd.HDFStore('datascience.h5') as hdf:
    embeddings = pd.read_hdf(hdf, key='embeddings')
    pos_words = pd.read_hdf(hdf, key='pos_words')
    neg_words = pd.read_hdf(hdf, key='neg_words')

pos_vectors = embeddings.reindex(pos_words).dropna()
neg_vectors = embeddings.reindex(neg_words).dropna()

# Creating positive and negative data set with word embeddings
vectors = pd.concat([pos_vectors, neg_vectors])
targets = np.array([1 for entry in pos_vectors.index] + [-1 for entry in neg_vectors.index])
labels = list(pos_vectors.index) + list(neg_vectors.index)

# Defining tuning parameters for Logistic Regression model
model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                           intercept_scaling=1, l1_ratio=None, max_iter=100,
                           multi_class='warn', penalty='l2',
                           random_state=None, solver='lbfgs', tol=0.0001, verbose=0,
                           warm_start=False)

train_vectors, test_vectors, train_targets, test_targets, train_labels, test_labels = train_test_split(vectors, targets, labels, test_size=0.1, random_state=0)

# Fitting model to train data
model.fit(train_vectors, train_targets)

print("Test accuracy is ", accuracy_score(model.predict(test_vectors), test_targets))

# Fitting all data into the model
model.fit(vectors, targets)

# Saving model
pickle.dump(model, open('sentiment_model.sav', 'wb'))
