# -*- coding: utf-8 -*-
"""privacy_policy_predictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15hWpfimK8Wk_pXNJQoDwlSEqOLhvHCrG
"""

import random

good_privacy = []
with open("good_privacy.txt", "r") as f:
  for line in f:
    good_privacy.append(line.rstrip())
bad_privacy_raw = []
with open("bad_privacy.txt", "r") as f:
  for line in f:
    bad_privacy_raw.append(line.rstrip())

bad_privacy = bad_privacy_raw[: -6 or None]

from sklearn.model_selection import train_test_split
# splitting the model into X and Y training and test data
# X is good, Y is bad
# we will represent X with 0 and Y with 1
X_train, X_test, y_train, y_test = train_test_split(good_privacy, bad_privacy, test_size=0.2, random_state=42)

combined_train = []
for item in X_train:
  combined_train.append([item, 0])
for item in y_train:
  combined_train.append([item, 1])
random.shuffle(combined_train)

training_data = []
training_target = []
for item in combined_train:
  training_data.append(item[0])
  training_target.append(item[1])

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

text_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', MultinomialNB()),
 ])
text_clf = text_clf.fit(training_data, training_target)

combined_test = []
for item in X_test:
  combined_test.append([item, 0])
for item in y_test:
  combined_test.append([item, 1])
random.shuffle(combined_test)

test_data = []
test_target = []
for item in combined_test:
  test_data.append(item[0])
  test_target.append(item[1])

import numpy as np
predicted = text_clf.predict(test_data)
np.mean(predicted == test_target)

for idx, item in enumerate(test_data):
  print(test_data[idx], 'predicted:', predicted[idx], 'actual:', test_target[idx])

from sklearn.linear_model import SGDClassifier
text_clf_svm = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf-svm', SGDClassifier(loss='hinge', penalty='l2',
                                        alpha=1e-3, random_state=42))
])
text_clf_svm = text_clf_svm.fit(training_data, training_target)
predicted_svm = text_clf_svm.predict(test_data)
np.mean(predicted_svm == test_target)

from sklearn.model_selection import GridSearchCV
parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
               'tfidf__use_idf': (True, False),
               'clf__alpha': (1e-2, 1e-3),
 }
gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
gs_clf = gs_clf.fit(training_data, training_target)
gs_clf.best_score_
gs_clf.best_params_

predicted_gs_clf = gs_clf.predict(test_data)
np.mean(predicted_gs_clf == test_target)

parameters_svm = {'vect__ngram_range': [(1, 1), (1, 2)],
               'tfidf__use_idf': (True, False),
               'clf-svm__alpha': (1e-2, 1e-3),
 }
gs_clf_svm = GridSearchCV(text_clf_svm, parameters_svm, n_jobs=-1)
gs_clf_svm = gs_clf_svm.fit(training_data, training_target)
gs_clf_svm.best_score_
gs_clf_svm.best_params_

predicted_gs_clf_svm = gs_clf_svm.predict(test_data)
np.mean(predicted_gs_clf_svm == test_target)