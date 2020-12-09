from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
lblout = None
def ReadTextFromInput(TextData):
	article = TextData.split(". ")
	sentences = []

	for sentence in article:
		print(sentence)
		sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
	sentences.pop() 
	
	return sentences

def ReadText(file_name):
	file = open(file_name, "r")
	filedata = file.readlines()


	article = filedata[0].split(". ")
	sentences = []
	global txt
	txt.delete(1.0,"end")
	txt.insert(1.0, filedata[0])
	for sentence in article:
		print(sentence)
		sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
	sentences.pop() 
	
	return sentences

def SentenceSimilarity(sent1, sent2, stopwords=None):
	if stopwords is None:
		stopwords = []
 
	sent1 = [w.lower() for w in sent1]
	sent2 = [w.lower() for w in sent2]
 
	all_words = list(set(sent1 + sent2))
 
	vector1 = [0] * len(all_words)
	vector2 = [0] * len(all_words)
 
	for w in sent1:
		if w in stopwords:
			continue
		vector1[all_words.index(w)] += 1
 
	for w in sent2:
		if w in stopwords:
			continue
		vector2[all_words.index(w)] += 1
 
	return 1 - cosine_distance(vector1, vector2)
 
def BuildSimilarityMatrix(sentences, stop_words):
	similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
	for idx1 in range(len(sentences)):
		for idx2 in range(len(sentences)):
			if idx1 == idx2: 
				continue 
			similarity_matrix[idx1][idx2] = SentenceSimilarity(sentences[idx1], sentences[idx2], stop_words)

	return similarity_matrix


def GenerateSummary(file_name, top_n=5 , demo = 0):
	stop_words = stopwords.words('english')
	summarize_text = []

	if demo:
		sentences =  ReadText(file_name)
	else:
		sentences =  ReadTextFromInput(file_name)

	SentenceSimilarity_martix = BuildSimilarityMatrix(sentences, stop_words)

	SentenceSimilarity_graph = nx.from_numpy_array(SentenceSimilarity_martix)
	scores = nx.pagerank(SentenceSimilarity_graph)

	ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
	print("Indexes of top ranked_sentence order are ", ranked_sentence)    
	try:
		for i in range(top_n):
		  summarize_text.append(" ".join(ranked_sentence[i][1]))
	except:
		pass

	print("Summarize Text: \n", ". ".join(summarize_text))
	return (". ".join(summarize_text))


#================================================================GUI================================================
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

clr1 = "#0C0D0B"
clr2 = "#262624"
clr3 = "#FFC54A"

window = tk.Tk()

window.title("Text Summarizer")

window.geometry('800x600')
tab1 = tk.Frame(window, bg=clr1,relief=tk.RAISED,bd=3)
lbl = tk.Label(tab1, text="Text Summarizer",bg=clr1, fg=clr3, font=('Arial', 30,"bold"),relief=tk.RAISED,bd=3)
lbl.pack(side = tk.TOP,expand=1, fill=tk.X)
tab1.pack(side = tk.TOP, fill=tk.X)



tab2 = tk.Frame(window,bg=clr1,relief=tk.RAISED,bd=3)
tk.Label(tab2, text="Input Text",bg=clr1, fg=clr3, font=('Arial', 15,"bold"),relief=tk.RAISED,bd=3).pack(side = tk.TOP, fill=tk.X)
txt = tk.Text(tab2, height=12,width=10, bg=clr2, fg="#fff", font=('Arial', 15),relief=tk.RAISED,bd=3)
txt.pack(fill=tk.X)
tk.Label(tab2, text="Summarized Text",bg=clr1,fg=clr3 , font=('Arial', 15,"bold"),relief=tk.RAISED,bd=3).pack(side = tk.TOP, fill=tk.X)
lblout = tk.Text(tab2, height=6,width=10 , bg=clr2, fg="#fff", font=('Arial', 15),relief=tk.RAISED,bd=3)
lblout.pack(expand=1, fill=tk.BOTH)
tab2.pack(side = tk.TOP,expand=1, fill=tk.BOTH)

tab3 = tk.Frame(window,relief=tk.RAISED,bd=3,bg=clr2)
def setTextInput(text):
	global lblout
	lblout.delete(1.0,"end")
	lblout.insert(1.0, text)

def clicked():
	res = txt.get('1.0', tk.END)
	res2 = GenerateSummary(res, 2)
	setTextInput(res2)

def clicked2():
	res2 = GenerateSummary("mytxt.txt", 2 , 1)
	setTextInput(res2)
btn = tk.Button(tab3, text="Submit Text",font=('Arial', 10,"bold"),bg = clr1,fg=clr3 ,command=clicked)
btn.grid(row=0, column=0,padx=7,pady=7)
btn2 = tk.Button(tab3, text="Demo",font=('Arial', 10,"bold"),bg = clr1,fg=clr3,command=clicked2)
btn2.grid(row=0, column=1,padx=7,pady=7)
tab3.pack(side = tk.TOP, fill=tk.X)
# tab3.grid_columnconfigure(0, weight=1, uniform="fred")
window.mainloop()