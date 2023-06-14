# -*- coding: utf-8 -*-
"""Resume Screening.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e0m8o3nQ_kOQzaqNtJ06ya1vXL-0phrR

### Import required libraries
"""

import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv('UpdatedResumeDataSet.csv')
data.head(20)

"""### Categories visualization"""

print(data['Category'].unique())

print('Total Unique category : {}'.format(len(data['Category'].unique())))

print(data['Category'].value_counts())

import seaborn as sns

plt.figure(figsize=(20,20))
sns.countplot(y='Category',data=data);

"""### Category distribution visualization"""

from matplotlib.gridspec import GridSpec
count = data['Category'].value_counts()
label = data["Category"].value_counts().keys()

plt.figure(1, figsize = (20,20))
grid = GridSpec(2,2)

cmap = plt.get_cmap('coolwarm')
color=[cmap(i) for i in np.linspace(0, 1, 5)]
plt.subplot(grid[0,1], aspect=1, title='Category Distribution')

pie=plt.pie(count, labels=label, autopct='%1.1f%%')
plt.show()

"""### RegEx clean"""

def clean(text):
    text=re.sub('http\S+\s*', ' ', text)
    text=re.sub('RT|cc', ' ', text)
    text=re.sub('#\S+', '', text)
    text=re.sub('@\S+', '', text)
    text=re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', text)
    text=re.sub('\s+', ' ', text)
    text=re.sub(r'[^\x00-\x7f]', r' ', text)
    return text

data['clean text']=data.Resume.apply(lambda x: clean(x))

data['clean text']

"""### Word cloud plot"""

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
import string
from wordcloud import WordCloud, STOPWORDS

stopwords=set(stopwords.words('english')+['``',"''"])

total_words=[]
sentences=data['Resume'].values
cleanSentences =""

for i in range(0,200):
    text=clean(sentences[i])
    cleanSentences+=text
    words=nltk.word_tokenize(text)
    for word in words:
        if word not in stopwords and word not in string.punctuation:
            total_words.append(word)

word_freq_dist=nltk.FreqDist(total_words)
most_common=word_freq_dist.most_common(100)

print(most_common)

WC=WordCloud(background_color = "white").generate(cleanSentences)
plt.figure(figsize=(15,15))
plt.imshow(WC, interpolation='bilinear');

"""### Training Machine Learning Model"""

from sklearn.preprocessing import LabelEncoder

var=['Category']
le=LabelEncoder()

for i in var:
    data[i]=le.fit_transform(data[i])

data

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack

text=data['clean text'].values
terget=data['Category'].values

vect=TfidfVectorizer(
    sublinear_tf=True,
    stop_words='english',
    max_features=2000)

vect.fit(text)

Word_feature=vect.transform(text)

Word_feature

x_train, x_test, y_train, y_test=train_test_split(Word_feature, terget, random_state=0, test_size=0.2)
print(x_train.shape)
print(x_test.shape)

import sklearn
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier

model=OneVsRestClassifier(KNeighborsClassifier())
model.fit(x_train, y_train)

prediction=model.predict(x_test)

print("training Score: {:.2f}".format(model.score(x_train, y_train)))
print("test Score: {:.2f}".format(model.score(x_test, y_test)))

from sklearn import metrics
print("model report: %s: \n %s\n" % (model, metrics.classification_report(y_test, prediction)))