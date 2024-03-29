# -*- coding: utf-8 -*-
"""Malayalam_sentiment_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VdsIb6pCRaeHP9Oaubl83hSyflvvqSzl
"""

# Commented out IPython magic to ensure Python compatibility.
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
from sklearn import feature_extraction, model_selection, naive_bayes, metrics
from sklearn.model_selection import train_test_split
# %matplotlib inline
from sklearn.feature_extraction.text import CountVectorizer
 
# Deep Learing Preprocessing - Keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.utils import to_categorical
 
# Deep Learning Model - Keras
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
 
# Deep Learning Model - Keras - CNN
from tensorflow.keras.layers import Conv1D, Conv2D, Convolution1D, MaxPooling1D, SeparableConv1D, SpatialDropout1D, GlobalAvgPool1D, GlobalMaxPool1D, GlobalMaxPooling1D 
from tensorflow.keras.layers import MaxPooling2D, GlobalMaxPooling2D, GlobalAveragePooling2D
 
# Deep Learning Model - Keras - RNN
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional
 
# Deep Learning Model - Keras - General
from tensorflow.keras.layers import Input, Add, concatenate, Dense, Activation, BatchNormalization, Dropout, Flatten
from tensorflow.keras.layers import LeakyReLU, PReLU, Lambda, Multiply
 
 
 
# Deep Learning Parameters - Keras
from tensorflow.keras.optimizers import RMSprop, Adam
 
# Deep Learning Callbacs - Keras
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard, ReduceLROnPlateau

from google.colab import drive
drive.mount('/content/drive')

cd /content/drive/My Drive/Malayalam Dataset

colnames=['text','label']
data = pd.read_csv(r'Mal_sentiment_full_train.tsv',names=colnames, delimiter='\t', error_bad_lines=False, header=None,
                      usecols=['text','label'], na_values=" NaN",skiprows=[0])
 
data_val = pd.read_csv(r'Mal_sentiment_full_dev.tsv',names=colnames, delimiter='\t', error_bad_lines=False, header=None,
                      usecols=['text','label'], na_values=" NaN",skiprows=[0])

data.size

def token(sentence):
  tokens = []
  for t in re.findall("[a-zA-Z]+",sentence):
    if len(t)>=1:
      tokens.append(t)
  return tokens

def emoji_ch (words):
  if words == '😄' :
    words='good'
  elif words == '😆' :
    words='good'
  elif words == '😊' :
    words='good'
  elif words == '😃' :
    words='good'    
  elif words == '🤬' :
    words='bad'
  elif words == '😏' :
    words='good'    
  elif words == '😍' :
    words='good'    
  elif words == '😘' :
    words='good'
  elif words == '😚' :
    words='good'    
  elif words == '😳' :
    words='flushed' 
  elif words == '😌' :
    words='bad'
  elif words == '😆' :
    words='good'    
  elif words == '😂' :
    words='good'    
  elif words == '😎' :
    words='good'        
  elif words == '🤯' :
    words='blow_mind'   
  elif words == '✌️' :
    words='vhand'           
  elif words == '🤘' :
    words='metal'
  elif words == '🤦' :
    words='bad'             
  elif words == '🤩':
    words='good'
  elif words == '🥰':
    words='good'
  elif words == '🤔':
    words='thinking'
  elif words == '🤣':
    words='good'
  elif words == '🤗':
    words = 'good'
  else :
    return None
  return words+" "

def malchar(ch):
    if ch == u'അ':
        ch="A"
    elif ch == u'ആ':
        ch="AA"
    elif ch == u'ഇ':
        ch="I"
    elif ch == u'ഈ':
        ch="II"
    elif ch == u'ഉ':
        ch="U"
    elif ch == u'ഊ':
        ch="UU"
    elif ch == u'എ':
        ch="E"
    elif ch == u'ഏ':
        ch="EE"
    elif ch == u'ഐ':
        ch="AI"
    elif ch == u'ഒ':
        ch="O"
    elif ch == u'ഓ':
        ch="OO"
    elif ch == u'ഔ':
        ch="AU"
    elif ch ==u'ക'or ch==u'ഖ':
        ch="KA"
    elif ch ==u'ഗ'or ch==u'ഘ':
        ch="GA"
    elif ch ==u'ങ':
        ch="NGA"
    elif ch ==u'ച'or ch==u'ഛ':
        ch="CH" 
    elif ch ==u'ച'or ch==u'ഛ':
        ch="CH" 
    elif ch ==u'ശ'or ch==u'ഷ':
        ch="SH"
    elif ch ==u'സ':
        ch="S"
    elif ch ==u'ജ' or ch==u'ഝ':
        ch="JA"
    elif ch ==u'ഡ'or ch==u'ദ':
        ch="DA"
    elif ch ==u'ഥ'or ch==u'ത':
        ch="THA"
    elif ch ==u'ണ'or ch==u'ന':
        ch="NA"
    elif ch ==u'പ':
        ch="PA"
    elif ch ==u'മ':
        ch="MA"
    elif ch ==u'യ':
        ch="YA"
    elif ch ==u'ര':
        ch="RA"
    elif ch ==u'ള':
        ch="LA"
    elif ch ==u'വ':
        ch="VA"
    elif ch ==u'ഹ':
        ch="HA"
    elif ch ==u'ഭ'or ch==u'ബ':
        ch="BA"
    elif ch ==u'ഢ'or ch==u'ധ':
        ch="DH"
    elif ch ==u'ഠ':
        ch="DT"
    elif ch ==u'ട':
        ch="T"
    elif ch ==u'ഞ':
        ch="NJ"
    elif ch ==u'ഫ':
        ch="PH"
    elif ch ==u'ഴ':
        ch="ZH"
    elif ch ==u'റ':
        ch="RA"    
    else:
        return None
    return ch

def preprocess(word):
  word=re.sub(r'([a-z])\1+', r'\1',word)
  return word

def malword(word):
    fla=0
    string=""
    for ch in word:
        if(malchar(ch) is not None):
            ch=malchar(ch)
            fla=1
        string=string+str(ch)
    if(fla==1):
        return string
    else:
        return None

import re
for index, line in data.iterrows():
  i=line[0].split()
  for word in range(len(i)):
    for ch in range(len(i[word])):
      checker=emoji_ch(i[word][ch])
      if(checker is not None):
        i[word]+=checker
    i[word]=preprocess(i[word])
      
    checker=malword(i[word])
    if(checker is not None):
      i[word]=checker
    i[word]=preprocess(i[word])
  line[0]=' '.join(i)

for index, line in data_val.iterrows():
  i=line[0].split()
  for word in range(len(i)):
    for ch in range(len(i[word])):
      checker=emoji_ch(i[word][ch])
      if(checker is not None):
        i[word]+=checker
    i[word]=preprocess(i[word])
      
    checker=malword(i[word])
    if(checker is not None):
      i[word]=checker
    i[word]=preprocess(i[word])
  line[0]=' '.join(i)

X_train = data['text'].tolist()
X_test = data_val['text'].tolist()
y_train = data['label']
y_test = data_val['label']

print(X_train)

print(len(X_train))

from sklearn.utils import class_weight
#class_weights = class_weight.compute_class_weight('balanced',np.unique(y_train),y_train)
y_train=pd.get_dummies(y_train).values
y_test=pd.get_dummies(y_test).values

max_words = len(set(" ".join(X_train).split()))
max_len = 100
 
tokenizer = Tokenizer(num_words=max_words)
 
tokenizer.fit_on_texts(X_train)
 
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_train_seq = sequence.pad_sequences(X_train_seq, maxlen=max_len)

print(X_train_seq)
print(X_train_seq.shape)

print(y_train)

embeddings_index = dict()
f = open(r"glove.6B.100d.txt",encoding="utf8")
for line in f:
    values = line.split()
    #print(values)
    word = values[0]
    #print(word)
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()
print('Loaded %s word vectors.' % len(embeddings_index))

vocab_size = len(tokenizer.word_index) + 1
print(vocab_size)
embedding_matrix = np.zeros((vocab_size, 100))
for word, i in tokenizer.word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector
 
print(embedding_matrix.shape)

model = Sequential()
model.add(Embedding(vocab_size, 100, weights=[embedding_matrix], input_length=max_len, trainable=True))
model.add(Dropout(0.1))
model.add(Conv1D(64, 3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.1))
model.add(LSTM(100))
model.add(Dense(5, activation='softmax'))

loss = 'categorical_crossentropy'
metrics = ['accuracy']

model.summary()

print("Starting...\n")

print("\n\nCompliling Model ...\n")
learning_rate = 0.001
optimizer = Adam(learning_rate)
# optimizer = Adam()

model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

verbose = 1
epochs = 10
batch_size = 1024

print("Trainning Model ...\n")

history1 = model.fit(
    X_train_seq,
    y_train,
    batch_size=batch_size,
    epochs=epochs
    )

print("Completed Model Trainning")

test_X_seq = tokenizer.texts_to_sequences(X_test)
test_X_seq = sequence.pad_sequences(test_X_seq, maxlen=max_len)
accuracy1 = model.evaluate(test_X_seq, y_test)
predhybrid = model.predict_classes(test_X_seq, verbose=1)

score = model.evaluate(test_X_seq, y_test,batch_size=128, verbose=1)
print('Test accuracy:', score[1])

preds = model.predict(test_X_seq)

from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(np.argmax(y_test,axis=1),np.argmax(preds,axis=1)))















from keras.preprocessing.sequence import pad_sequences
vocabulary_size = 30000
tokenizer = Tokenizer(num_words= vocabulary_size)
tokenizer.fit_on_texts(X_train)
sequences = tokenizer.texts_to_sequences(X_train)
X_train = pad_sequences(sequences, maxlen=100)
sequences = tokenizer.texts_to_sequences(X_test)
X_test = pad_sequences(sequences, maxlen=100)

model = Sequential()
model.add(Embedding(30000, 100, input_length=100))
model.add(Dropout(0.1))
model.add(Conv1D(64, 3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.1))
model.add(LSTM(100))
model.add(Dense(5, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train,
                    batch_size=1024,
                    epochs=10,
                    verbose=1)

score = model.evaluate(X_test, y_test,
                       batch_size=256, verbose=1)
print('Test accuracy:', score[1])

preds = model.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(np.argmax(y_test,axis=1),np.argmax(preds,axis=1)))