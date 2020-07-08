import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer 
import pandas as pd 
# name = "Biyetimi pendrive multifunctional OTG 64gb usb флэш-накопители for phone 32gb pen drive 16gb usb flash drives 64GB usb"

name = input("Enter File Name [ put file in csv folder first ] : ")
data = pd.read_csv(r"csv\\"+name+".csv",usecols=['comments']) 
l = data.values.tolist()
porter_stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer() 

csv_doc = pd.DataFrame(columns = ['comments','stem words' , 'lemmatize [noun][adjective]'])

for j,i in enumerate(l):
	print(j)
	if type(i[0])==str:
		nltk_tokens = nltk.word_tokenize(i[0])

	wrd  = dict()
	lemwrd = dict()
	for w in nltk_tokens:
		if(w.isalnum() and not w.isdecimal()):
			temp = porter_stemmer.stem(w)
			temp2 = lemmatizer.lemmatize(w)
			temp3 = lemmatizer.lemmatize(w,pos='a')
			wrd[w] = temp
			lemwrd[w] = [temp2,temp3]
	csv_doc.loc[j] = [ i[0], wrd , lemwrd]

csv_doc.to_csv('csv/(processed)'+name+'.csv')
