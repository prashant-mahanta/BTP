import nltk
from nltk import pos_tag
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
#nltk.download()
#from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
#from nltk.stem import PorterStemmer
#from nltk.corpus import state_union
#from nltk.tokenize import PunktSentenceTokenizer

#example_text = "Hello mr. Smith, how are you doing today? the weather is great, and python is awesome. the sky is pinkish-blue. you shouldn't eat cardboard."

#print("Sentence Tokenize:",sent_tokenize(example_text))
#print("\n \n")
#print("Word Tokenize:",word_tokenize(example_text))


#stop_words = set(stopwords.words('english'))

#word_tokens = word_tokenize(example_text)

#filtered_sentence = [w for w in word_tokens if not w in stop_words]

#filtered_sentence = []

#for w in word_tokens:
#    if w not in stop_words:
#        filtered_sentence.append(w)

#print("\n \n")
#print("After Stopwords removal:",filtered_sentence)


#ps = PorterStemmer()
#after_stem = []
#for w in filtered_sentence:
#	after_stem.append(ps.stem(w))

#print("\n\nAfter Stemming:",after_stem)


from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

st = StanfordNERTagger('stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
					   'stanford-ner-2018-10-16/stanford-ner.jar',
					   encoding='utf-8')

#text = "Pak vs SA 5th ODI Live Cricket Score Streaming Online: After being overpowered in the Test series, Pakistan have a golden opportunity to beat South Africa in their own backyard and win the 5-match ODI series. The final match of the series will be played on Wednesday. After enduring an unfortunate loss in the third ODI in Durban, Pakistan bounced back in the contest by securing an impressive 8-wicket win in the previous ODI. Usman Khan led the bowling unit, while Imam-ul-Haq struck a brilliant 71 as the visitors dominated their opponent in both the departments of the game. South Africa, on the other hand, would look to take the defeat as a wake up call. Apart from Hashim Amla and skipper Faf du Plessis, the entire South African batting line-up bowed down against the Pakistani seamers. Usman Khan, who scalped 4-wickets in the previous ODI was the key man behind South Africa’s collpase. The hosts lost the final six wickets for 24 runs in the previous ODI, with Khan picking three wickets in the 37th over of the match. IBM ACM ICPC 2018 Google 10 dollars."

def date_classify(date):
	d={}
	d["DAY"]=[]
	d["MONTH"]=[]
	d["YEAR"]=[]
	d["TIME"]=[]
	day=["monday","tuesday","thursday","wednesday","friday","saturday","sunday"]
	month=["january","february","march","april","may","june","july","august","september","october","november","december"]
	for i in date:
		try:
			year = int(i)
			if year > 1900:
				d["YEAR"].append(i)
			else:
				d["TIME"].append(i)
		except ValueError:
			if  i.lower() in day:
				d["DAY"].append(i)
			elif i.lower() in month:
				d["MONTH"].append(i)	
			else:
				d["TIME"].append(i)
				
	return d	
	
fp = open("S-HT.txt","w+")
for filenum in range(1001,1051):
#	file_name = "sample.txt"
	file_name = "news_files/ht/News"+str(filenum)+".txt"
	fil = filenum+1000
	fp.write(str(fil))
	fp.write("\n")
	
	fileid = "FileID: "+ "News"+str(filenum)+".txt"
	fp.write(fileid)
	fp.write("\n")
	raw_text = open(file_name).read()
	tokenized_text = word_tokenize(raw_text)
	tokens = []
	for val in tokenized_text:
		if val.find(".") != -1:
#			print(val)
			a = val.split(".")
			if len(a)==2:
				if len(a[0]) > 2 and len(a[1]) > 2:
					tokens.append(a[0])
					tokens.append(a[1])
		else:
			tokens.append(val)
	stop_words = set(stopwords.words('english'))
	filtered_sentence = [w for w in tokens if not w in stop_words]
	classified_text = st.tag(filtered_sentence)

#	print(classified_text,"\n\n\n")
	output={}
	output["PERSON"]=[]
	output["O"] = []
	output["DATE"]=[]
	output["ORGANIZATION"]=[]
	output["LOCATION"]=[]

	for word in classified_text:
		if word[1] == "PERSON":
			output["PERSON"].append(word[0])
		elif word[1] == "O":
			output["O"].append(word[0])
		elif word[1] == "DATE":
			output["DATE"].append(word[0])
		elif word[1] == "ORGANIZATION":
			output["ORGANIZATION"].append(word[0])
		elif word[1] == "LOCATION":
			output["LOCATION"].append(word[0])
	output["O"]=list(filter(("(").__ne__, output["O"]))
	output["O"]=list(filter((")").__ne__, output["O"]))
	output["O"]=list(filter((".").__ne__, output["O"]))
	output["O"]=list(filter((",").__ne__, output["O"]))
	output["O"]=list(filter((";").__ne__, output["O"]))
	output["O"]=list(filter((":").__ne__, output["O"]))
	output["O"]=list(filter(("’").__ne__, output["O"]))
	output["O"]=list(filter(("``").__ne__, output["O"]))
	
	output["DATE"] = date_classify(output["DATE"])
	for key,value in output.items():
		fp.write(key)
		fp.write(" : ")
		if key != "DATE":
			fp.write(str(list(set(value))))
		else:
			fp.write(str(value))
		fp.write("\n")
		
#		print(key,":",value)
	fp.write("\n")
fp.close()


	#------------------------------------------------------------------------------------------
#	print("\n\n\n----------------------------------------\n\n\n\n")
#	def process_text(txt_file):
#		raw_text = open(txt_file).read()
#		token_text = word_tokenize(raw_text)
#		return token_text

#	# Stanford NER tagger    
#	def stanford_tagger(token_text):
#		st = StanfordNERTagger('stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
#								'stanford-ner-2018-10-16/stanford-ner.jar',
#								encoding='utf-8')   
#		ne_tagged = st.tag(token_text)
#		return(ne_tagged)
#	def bio_tagger(ne_tagged):
#			bio_tagged = []
#			prev_tag = "O"
#			for token, tag in ne_tagged:
#				if tag == "O": #O
#					bio_tagged.append((token, tag))
#					prev_tag = tag
#					continue
#				if tag != "O" and prev_tag == "O": # Begin NE
#					bio_tagged.append((token, "B-"+tag))
#					prev_tag = tag
#				elif prev_tag != "O" and prev_tag == tag: # Inside NE
#					bio_tagged.append((token, "I-"+tag))
#					prev_tag = tag
#				elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
#					bio_tagged.append((token, "B-"+tag))
#					prev_tag = tag
#			return bio_tagged

#	def stanford_tree(bio_tagged):
#		tokens, ne_tags = zip(*bio_tagged)
#		pos_tags = [pos for token, pos in pos_tag(tokens)]

#		conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
#		ne_tree = conlltags2tree(conlltags)
#		return ne_tree

#	def structure_ne(ne_tree):
#		ne = []
#		for subtree in ne_tree:
#			if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
#				ne_label = subtree.label()
#				ne_string = " ".join([token for token, pos in subtree.leaves()])
#				ne.append((ne_string, ne_label))
#		return ne



#	def stanford_main():
#		txt_file=file_name
#		print(structure_ne(stanford_tree(bio_tagger(stanford_tagger(process_text(txt_file))))))
		
#	stanford_main()


