import nltk
from nltk import pos_tag
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
#nltk.download()
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from nltk.tag import StanfordNERTagger
from A_V import main_parser
st = StanfordNERTagger('stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
					   'stanford-ner-2018-10-16/stanford-ner.jar',
					   encoding='utf-8')

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
def convertHash(string):
	s=""
	for a in string:
		s+=a
	return hash(s)

fp = open("S2-HT.txt","w+")
for filenum in range(1001,1020):
#	file_name = "sample.txt"
	file_name = "newscrap/article"+str(filenum)+".txt"
	fil = filenum
	fp.write(str(fil))
	fp.write("\n")
	
	fileid = "	FileID: "+ "article"+str(filenum)+".txt"
	fp.write(fileid)
	fp.write("\n")
	img = "	Image: "+ str(filenum) +".jpg"
	fp.write(img)
	fp.write("\n")
	raw_txt = open(file_name).read()
	sent_tokenize_list = sent_tokenize(raw_txt)
	if len(sent_tokenize_list) > 1:
		for raw_text in sent_tokenize_list:
			tokenized_text = word_tokenize(raw_text)
			tokenized_text=[word for word in tokenized_text if word.isalpha()]
			hash_sent = convertHash(tokenized_text)
			main_parser(raw_text)
			# print(raw_text)
			if hash_sent != 0:
				fp.write("	sid: ")
				fp.write(str(hash_sent))
				fp.write("\n")
	#			fp.write("	Sentence: ")
	#			fp.write(raw_text)
	#			fp.write("\n")
			#	tokens = []
			#	for val in tokenized_text:
			#		if val.find(".") != -1:
			##			print(val)
			#			a = val.split(".")
			#			if len(a)==2:
			#				if len(a[0]) > 2 and len(a[1]) > 2:
			#					tokens.append(a[0])
			#					tokens.append(a[1])
			#		else:
			#			tokens.append(val)
				stop_words = set(stopwords.words('english'))
				filtered_sentence = [w for w in tokenized_text if not w in stop_words]
				classified_text = st.tag(filtered_sentence)
			#	print(classified_text,"\n\n\n")
				output={}
				output["PERSON"]=[]
				output["O"] = []
				output["DATE"]=[]
				output["ORGANIZATION"]=[]
				output["LOCATION"]=[]
				output["VERBS"]=[]
		#		for word in classified_text:
		#			if word[1] == "PERSON":
		#				output["PERSON"].append(word[0])
		#			if word[1] == "O":
		#				output["O"].append(word[0])
		#			elif word[1] == "DATE":
		#				output["DATE"].append(word[0])
		#			elif word[1] == "ORGANIZATION":
		#				output["ORGANIZATION"].append(word[0])
		#			elif word[1] == "LOCATION":
		#				output["LOCATION"].append(word[0])
			#	output["O"]=list(filter(("(").__ne__, output["O"]))
				
		#		output["DATE"] = date_classify(output["DATE"])
				def bio_tagger(ne_tagged):
						bio_tagged = []
						prev_tag = "O"
						for token, tag in ne_tagged:
							if tag == "O": #O
								bio_tagged.append((token, tag))
								prev_tag = tag
								continue
							if tag != "O" and prev_tag == "O": # Begin NE
								bio_tagged.append((token, "B-"+tag))
								prev_tag = tag
							elif prev_tag != "O" and prev_tag == tag: # Inside NE
								bio_tagged.append((token, "I-"+tag))
								prev_tag = tag
							elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
								bio_tagged.append((token, "B-"+tag))
								prev_tag = tag
						return bio_tagged

				def stanford_tree(bio_tagged):
					tokens, ne_tags = zip(*bio_tagged)
					pos_tags = [pos for token, pos in pos_tag(tokens)]

					conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
					ne_tree = conlltags2tree(conlltags)
					return ne_tree

				def structure_ne(ne_tree):
					ne = []
					neo = []
					for subtree in ne_tree:
						if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
							ne_label = subtree.label()
							ne_string = " ".join([token for token, pos in subtree.leaves()])
							ne.append((ne_string, ne_label))
						else:
							neo.append((subtree[0], "O"))
							if subtree[1] in ["VBD","VBG","VBN","VBP","VBZ"]:
								output["VERBS"].append(subtree[0])
					return [ne,neo]
				def attribute_verb(ne_tree):
					ne = []
					neo = []
					for subtree in ne_tree:
						if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
							ne_label = subtree.label()
							ne_string = " ".join([token for token, pos in subtree.leaves()])
							ne.append((ne_string, ne_label))
						else:
							neo.append((subtree[0], "O"))
							if subtree[1] in ["VBD","VBG","VBN","VBP","VBZ"]:
								output["VERBS"].append(subtree[0])
				def stanford_main():
					txt_file=file_name
					tree_stanford = stanford_tree(bio_tagger(classified_text))
					# print(tree_stanford)
					return structure_ne(tree_stanford)
					
				phrase_text,others = stanford_main()
				
			

				for word_p in phrase_text:
					if word_p[1] == 'PERSON':
						output['PERSON'].append(word_p[0])
					if word_p[1] == 'ORGANIZATION':
						output["ORGANIZATION"].append(word_p[0])
					elif word_p[1] == 'LOCATION':
						output['LOCATION'].append(word_p[0])
					elif word_p[1] == "DATE":
						output["DATE"].append(word_p[0])
					elif word_p[1] == "LOCATION":
						output["LOCATION"].append(word_p[0])
						
				output["DATE"] = str(date_classify(output["DATE"]))
				for word_p in others:
					if word_p[1] == 'O':
						output['O'].append(word_p[0])	
				for key, value in output.items():
					fp.write("	")
					fp.write(key)
					fp.write(" : ")
					fp.write(str(value))
					fp.write("\n")
				fp.write("\n")
fp.close()

