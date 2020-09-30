import pandas as pd
#Number of stopwords
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

stop = stopwords.words('english')

print("\n"+"*"*100+"\n")

# name = input("Enter File Name [ put file in csv folder first ] : ")
name = "Biyetimi pendrive multifunctional OTG 64gb usb флэш-накопители for phone 32gb pen drive 16gb usb flash drives 64GB usb"
data = pd.read_csv(r"csv\\"+name+".csv",usecols=['comments']) 
#Number of Words
data['word_count'] = data['comments'].apply(lambda x: len(str(x).split(" ")))
# print(data[['comments','word_count']].head())

print("\n"+"*"*100+"\n")


#Number of characters
data['char_count'] = data['comments'].str.len() ## this also includes spaces
# print(data[['comments','char_count']].head())

print("\n"+"*"*100+"\n")

#Average Word Length
#Number of characters(without space count)/Total number of words
def avg_word(sentence):
  if(type(sentence)==str):
	  words = sentence.split()
	  # print(words)
	  # print(len(words))
	  # print(sum(len(word) for word in words))
	  return (sum(len(word) for word in words)/len(words))

data['avg_word'] = data['comments'].apply(lambda x: avg_word(x))
# print(data[['comments','avg_word']].head())

print("\n"+"*"*100+"\n")

#Number of Words
data['word_count'] = data['comments'].apply(lambda x: len(str(x).split(" ")))
data[['comments','word_count']].head()

print("\n"+"*"*100+"\n")

#Number of characters
data['char_count'] = data['comments'].str.len() ## this also includes spaces
data[['comments','char_count']].head()



print("\n"+"*"*100+"\n")


#Average Word Length
#Number of characters(without space count)/Total number of words
def avg_word(sentence):
  if(type(sentence)==str):
	  words = sentence.split()
	  print(words)
	  print(len(words))
	  print(sum(len(word) for word in words))
	  return (sum(len(word) for word in words)/len(words))

data['avg_word'] = data['comments'].apply(lambda x: avg_word(x))
data[['comments','avg_word']].head()


print("\n"+"*"*100+"\n")


data['stopwords'] = data['comments'].apply(lambda x: len([x for x in x.split() if x in stop]))
data[['comments','stopwords']].head()



print("\n"+"*"*100+"\n")


#Number of special characters
data['hastags'] = data['comments'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
data[['comments','hastags']].head()



print("\n"+"*"*100+"\n")



#Number of numerics
data['numerics'] = data['comments'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))
data[['comments','numerics']].head()


print("\n"+"*"*100+"\n")


#Number of Uppercase words
data['upper'] = data['comments'].apply(lambda x: len([x for x in x.split() if x.isupper()]))
data[['comments','upper']].head()




print("\n"+"*"*100+"\n")



pos_family = {
    'noun' : ['NN','NNS','NNP','NNPS'],
    'pron' : ['PRP','PRP$','WP','WP$'],
    'verb' : ['VB','VBD','VBG','VBN','VBP','VBZ'],
    'adj' :  ['JJ','JJR','JJS'],
    'adv' : ['RB','RBR','RBS','WRB']
}

# function to check and get the part of speech tag count of a words in a given sentence
from textblob import TextBlob, Word, Blobber
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
def check_pos_tag(x, flag):
    cnt = 0
    try:
        wiki = TextBlob(x)
        for tup in wiki.tags:
            ppo = list(tup)[1]
            if ppo in pos_family[flag]:
                cnt += 1
                print(ppo, tup)
    except:
        pass
    return cnt

data['noun_count'] = data['comments'].apply(lambda x: check_pos_tag(x, 'noun'))
data['verb_count'] = data['comments'].apply(lambda x: check_pos_tag(x, 'verb'))
data['adj_count'] = data['comments'].apply(lambda x: check_pos_tag(x, 'adj'))
data['adv_count'] = data['comments'].apply(lambda x: check_pos_tag(x, 'adv'))
data['pron_count'] = data['comments'].apply(lambda x: check_pos_tag(x, 'pron'))
print(data[['comments','noun_count','verb_count','adj_count', 'adv_count', 'pron_count' ]].head())


A = list(data['comments'])
cv=CountVectorizer()
A_vec = cv.fit_transform(A)
print(A_vec.toarray())


tv=TfidfVectorizer()
t_vec = tv.fit_transform(A)
print(t_vec.toarray())

feature_names = tv.get_feature_names()

dense = t_vec.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)


df_c =pd.concat([df,data], axis=1)
print(df_c.head())