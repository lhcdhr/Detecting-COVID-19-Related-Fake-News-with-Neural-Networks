# -*- coding: utf-8 -*-
"""550fp_logistic_regression_baseline.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1StVfRN6HxYJ8x3UQ0kYBpkSL7hPAbGH5
"""

import pandas as pd
import nltk
import numpy as np
from nltk.stem import 	WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
wordnet_lemmatizer = WordNetLemmatizer()
porter_stemmer  = PorterStemmer()
import preprocessor as p
#from preprocessor.api import clean, tokenize, parse,set_options
import re
from string import punctuation

from nltk.tokenize.toktok import ToktokTokenizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score

p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.HASHTAG)

df = pd.read_csv("data/Constraint_Train.csv")
val_df = pd.read_csv("data/Constraint_Val.csv")
test_df = pd.read_csv("data/Constraint_Test.csv")
test_label = pd.read_csv("data/english_test_with_labels.csv")

print(df['tweet'])
print(df['tweet'][6416])

def preprocess(instance):
  x = instance['tweet']
  # text = text.strip('\xa0')
  x = p.clean(x)
  tokenization = nltk.word_tokenize(x)     
  tokenization = [w for w in tokenization if not w in stop_words]
#   text = ' '.join([porter_stemmer.stem(w) for w in tokenization])
#   text = ' '.join([lemmatizer.lemmatize(w) for w in tokenization])
#   text = re.sub(r'\([0-9]+\)', '', text).strip()    
  return x

def relabel(instance):
    new_l=0
    if instance ['label']=='real':
        new_l=1
    return new_l

df.apply(lambda x: preprocess(x),1)

df['label_encoded'] = df.apply(lambda x: relabel(x), 1)
val_df['label_encoded'] = val_df.apply(lambda x: relabel(x), 1)
test_df['label_encoded'] = test_label.apply(lambda x: relabel(x), 1)

print(df['tweet'])

def remove_punctuations(sentence):
    for p in punctuation:
        sentence = sentence.replace(p,'')
    return sentence
def to_lower_case(sentence):
    return sentence.lower()

real = 0
fake = 0
for i in range(6420):
    if(df['label_encoded'][i]==1):
        real = real+1
    else:
        fake = fake+1
print(real)
print(fake)
real = 0
fake = 0
for i in range(2140):
    if(val_df['label_encoded'][i]==1):
        real = real+1
    else:
        fake = fake+1
print(real)
print(fake)
real = 0
fake = 0
for i in range(2140):
    if(test_df['label_encoded'][i]==1):
        real = real+1
    else:
        fake = fake+1
print(real)
print(fake)
for i in range(6420):
    if(len(df['tweet'][i])>2000):
        print(i)
        print(df['tweet'][i])

df['tweet'] = df.apply(lambda x: preprocess(x), 1)
df['tweet'] = df['tweet'].apply(remove_punctuations)
df['tweet'] = df['tweet'].apply(to_lower_case)
val_df['tweet'] = val_df.apply(lambda x: preprocess(x), 1)
val_df['tweet'] = val_df['tweet'].apply(remove_punctuations)
val_df['tweet'] = val_df['tweet'].apply(to_lower_case)
test_df['tweet'] = test_df.apply(lambda x: preprocess(x), 1)
test_df['tweet'] = test_df['tweet'].apply(remove_punctuations)
test_df['tweet'] = test_df['tweet'].apply(to_lower_case)

print(df['tweet'])
print(val_df['tweet'])
print(test_df['tweet'])

all_tweets=pd.concat([df['tweet'],val_df['tweet'],test_df['tweet']])
print(all_tweets.shape)

all_tweets[0]=all_tweets[0].astype("str")
cv=CountVectorizer(lowercase = True,ngram_range=(1,1))
cv_mixed = cv.fit_transform(all_tweets)

print(all_tweets)
#print(cv_mixed)

print(df.shape)
print(val_df.shape)
print(test_df.shape)

train_sentences = cv_mixed[:6420]
val_sentences = cv_mixed[6420:(6420+2140)]
test_sentences = cv_mixed[(6420+2140):]

train_labels = df['label_encoded']
val_labels = val_df['label_encoded']
test_labels = test_df['label_encoded']

def train(train_data,train_result):
    lr_model = LogisticRegression(penalty = 'l2', max_iter=200, C=1,random_state = 1)
    lr_model_train = lr_model.fit(train_data, train_result)
    lr_model_test = lr_model.predict(train_data)
    lr_model_score = accuracy_score(train_result,lr_model_test)
    return lr_model_score

def test(train_data,train_result,test_data,test_result):
    lr_model = LogisticRegression(penalty = 'l2', max_iter=200, C=1,random_state = 1)
    lr_model_train = lr_model.fit(train_data, train_result)
    lr_model_test = lr_model.predict(test_data)
    lr_model_score = accuracy_score(test_result,lr_model_test)
    return lr_model_score

train_score = train(train_sentences,train_labels)
print(train_score)

val_score = test(train_sentences,train_labels,val_sentences,val_labels)
print(val_score)

test_score = test(train_sentences,train_labels,test_sentences,test_labels)
print(test_score)