import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from sklearn.decomposition import TruncatedSVD
# If nltk stop word is not downloaded
nltk.download('stopwords')
from nltk.corpus import stopwords

import nltk,csv,numpy
nltk.download('punkt')
from nltk import sent_tokenize, word_tokenize, pos_tag
sentences=[]
name = "csv/Biyetimi pendrive multifunctional OTG 64gb usb флэш-накопители for phone 32gb pen drive 16gb usb flash drives 64GB usb"

reader = csv.reader(open(name+'.csv', 'rU'), delimiter= ",",quotechar='|')
for line in reader:
    for field in line:
      sentences.append(field)
print(sentences)

df = pd.DataFrame()
df["documents"] = sentences
df.head()
df['clean_documents'] = df['documents'].str.replace("[^a-zA-Z#]", " ")
df['clean_documents'] = df['clean_documents'].fillna('').apply(lambda x: ' '.join([w for w in x.split() if len(w)>2]))
df['clean_documents'] = df['clean_documents'].fillna('').apply(lambda x: x.lower())

df.head()

# tokenization
tokenized_doc = df['clean_documents'].fillna('').apply(lambda x: x.split())

# remove stop-words

tokenized_doc = tokenized_doc.apply(lambda x: [itemstop_words== stopwords.words('english') for item in x if item not in stop_words])

# de-tokenization
detokenized_doc = []
for i in range(len(df)):
    t = ' '.join(tokenized_doc[i])
    detokenized_doc.append(t)

df['clean_documents'] = detokenized_doc

# TF-IDF vector
vectorizer = TfidfVectorizer(stop_words='english', smooth_idf=True)
X = vectorizer.fit_transform(df['clean_documents'])
X.toarray()

# SVD represent documents and terms in vectors 
svd_model = TruncatedSVD(n_components=2, algorithm='randomized', n_iter=100, random_state=122)
lsa = svd_model.fit_transform(X)

#Documents - Topic vector
pd.options.display.float_format = '{:,.16f}'.format
topic_encoded_df = pd.DataFrame(lsa, columns = ["topic_1", "topic_2"])
topic_encoded_df["documents"] = df['clean_documents']
display(topic_encoded_df[["documents", "topic_1", "topic_2"]])

dictionary = vectorizer.get_feature_names()

encoding_matrix = pd.DataFrame(svd_model.components_, index = ["topic_1","topic_2"], columns = (dictionary)).T
encoding_matrix

