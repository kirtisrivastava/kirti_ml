from __future__ import print_function
from django.shortcuts import render
import json
from collections import Counter
import os
import re
import config.settings as settings

import urllib2, cookielib, urllib
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import operator
import training_set
import tokenize_training
import response_data
import keywords_data
import training
import random
import string
from lxml import etree
from itertools import combinations
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

import sys  
from nltk.chat.util import Chat
import eliza_chat
from nltk.chat.util import Chat, reflections
import nltk
from nltk.tokenize import sent_tokenize

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing

import re
from google import google

# Create your views here.
"Intial page for taking text file."	
def chatbotpage(request):
	return render(request,'chatbot.html')

module_dir = os.path.dirname(__file__)

          		
with open(module_dir + '/techport_dict.txt') as word_file:
	english_words = set(word.strip().lower() for word in word_file)


def chatbotresponse(request):
	if request.method == 'GET':
		response = {}
		sentence = request.GET.get('string')
		#remove spaces bigining and after the sentences. 
		initial_sentence = sentence.strip()
		#remove extra spaces inbetween the sentences. 
		initial_sentence = re.sub(' +',' ',initial_sentence)
		initial_sentence = initial_sentence.lower()		 
		print ("initial_sentence",initial_sentence)
		if sentence:
			list1 = keywords_data.getkeyworddata();
			list_of_swear_words = ["dumbo","fool","stupid","arse","ass","asshole","bastard","bitch","crap","cockfucker","cunt","damn","dammit","fuck","fucking","goddamn","godsdamn","hell","holy shit","retard","shitty","motherfucker","shit","shitass"]
			if not re.match(r'^[_\W]+$', sentence):
				if not sentence.isdigit():
					print("after num and special remove sentence", sentence)
					sentence = re.sub('[^a-zA-Z0-9.?@$#!%^&*()+_=~*,""/><\{}[]]', ' ', sentence)
					print("sentence", sentence)
					sentence = str(sentence.lower())
					chatbot_sentence = sentence
					sentence = sentence.split(' ')
					modified_string1 =[]
					modified_string =[]
					for word in sentence:
						if word:
							sub=correction(word)
							modified_string1.append(sub)
						if word=='helo':				
							modified_string.append('hello')
						else:
							if not re.match(r'^[_\W]+$', word):
								if word:
									check_spellings = ""
									if word.lower() not in english_words:
										check_spellings = word
									if re.match(r'^[_\W]+$', word) and check_spellings:
										#"checking misspelled word and Correctoring"
										sub=correction(word)
										modified_string.append(sub)
									else:
										if re.match("^[a-zA-Z0-9]*$", str(word)):
											#"checking misspelled word and Correctoring"
											sub=correction(word)
											modified_string.append(sub)
										else:
											modified_string.append(str(word))
							else:
								if word:
									print("word",word)
									modified_string.append((word))
					
					print("modified_string1", modified_string1)
					matched_swear_words = [x for x in list_of_swear_words if x in modified_string]
					if not matched_swear_words:
						print("checking")
						try:
							cobination_of_sentence =[]
							print("modified_string",len(modified_string))
							for i in range(len(modified_string)):
								list2 = [modified_string[i]]
								cobination_of_sentence.append(list2)

							for phrase in phrase_builder(modified_string):
								list3 =[phrase]
								cobination_of_sentence.append(list3)
							#cobination_of_sentence = sum([map(list, combinations(modified_string, i)) for i in range(len(modified_string) + 1)], [])			
							print("checked")
							set_of_cobination = []						
							for words in cobination_of_sentence:
								statement=' '.join(map(str, words))
								set_of_cobination.append(statement)

							S1 = set(set_of_cobination)
							S2 = set(list1)
							maching_strings = []
							maching_strings = S1.intersection(S2)
							print("maching_strings", maching_strings) 		
							longest_stirng = ""
							if maching_strings:
								longest_stirng = max(maching_strings, key=len)
							print("longest_stirng", longest_stirng)
							# Checking matching elements in both the list
							matched_word = [x for x in list1 if x in modified_string]
							matched_word1 = [x for x in list1 if x in modified_string1]
							print("matched_word1", matched_word1)
						except:
							response = {'status':'error', 'message':'What are you asking'}
							return HttpResponse(json.dumps(response), content_type='application/json')
						if not (longest_stirng) and not (matched_word1):
							print ("modified_string", modified_string)
							makeitastring = ' '.join(map(str, modified_string))
							removed_special_chars_str = re.sub('[^a-zA-Z0-9-]', ' ', makeitastring)
							check_spelling = [word for word in removed_special_chars_str if re.sub('[^a-zA-Z0-9-]', '', word) not in english_words]
							print("check_spelling", check_spelling)
							if check_spelling:
								print ("check_spelling not match", check_spelling)
								makeproper_sentence= "your search" +" "+ makeitastring + " " + "did not match any document"
								response = {'status':'error', 'message': makeproper_sentence}
							else:
								print("len(modified_string)",len(modified_string))
								if len(modified_string) == 1:
									training_sentences = training_set.gettrainingdata();
									get_index = False
									for index, words in enumerate(training_sentences):
										if(modified_string[0] == words.lower()):
											indexs = index
											wordss = words
											get_index = True 
									print ("get_index", get_index)
									if get_index:
										print ("indexs", indexs)						     
										response_values = response_data.get_response_data();
										data = response_values.get(int(indexs), None)
										if data:
											if str(data[0]) == "tech_news":
												result = get_news(settings.TECHPORTAL_NEWS);					
												if result:
													response['status'] = "success"
													response['do_you_want'] = "Do you want to see more? If you are then please click on Yes else No"
													response['chatbotresponse'] = result
													print ("initial_sentence", initial_sentence)												
													print ("makeitastring", makeitastring)
													if str(initial_sentence) == str(makeitastring):								
														response['wait_looking'] = "Just a sec, I am looking that up"
														response['matched_word'] = "Here are the most relevant news results for"
													else:
														response['wait_looking'] = "Showing results for" +" "+ makeitastring
														response['matched_word'] = "No results found for" +" "+ initial_sentence
											else:
												response['status'] = "chat_success"
												response['chatbotresponse'] = str(random.choice(data)) 

										else:
											response['status'] = "error"
											response['message'] = "I think you have entered which we can't give information"
									else:
										response['status'] = "error"
										response['message'] = "Try more general keywords. Or Try by giving more keywords"

								if len(modified_string) == 0:
									response['status'] = "error"
									response['message'] = "What you are asking i didn't get"
								elif (len(modified_string) != 0) and (len(modified_string) != 1):
									train_set=training_set.gettrainingdata();

									test_set = [chatbot_sentence]
									# print "test_set", test_set
									count_vectorizer= CountVectorizer()
									count_vectorizer.fit_transform(train_set)

									# print"Vocabulary:",count_vectorizer.vocabulary

									freq_term_matrix = count_vectorizer.transform(test_set)
									# print freq_term_matrix.todense()

									tfidf = TfidfTransformer(norm="l2")
									tfidf.fit(freq_term_matrix)
									TfidfTransformer(norm='l2', smooth_idf=True, sublinear_tf=False, use_idf=True)
									# print "IDF:", tfidf.idf_

									tf_idf_matrix = tfidf.transform(freq_term_matrix)
									# print tf_idf_matrix.todense()

									tfidf_vectorizer = TfidfVectorizer()

									tfidf_matrix1 = tfidf_vectorizer.fit_transform(train_set)

									check_cosine_similarity =cosine_similarity(tf_idf_matrix[0:1], tfidf_matrix1)
									# if not all(v == 0.0 for v in check_cosine_similarity[0]):
									maximum_cosine_similarity= max(check_cosine_similarity)
									index,value = max(enumerate(maximum_cosine_similarity), key=operator.itemgetter(1))
									print(index)
									print(value)
									if (value > 0.7):
										response_values = response_data.get_response_data();
										data = response_values.get(int(index), None)
										if data:
											print ("data", data)
											if str(data[0]) == "tech_news":
												result = get_news(settings.TECHPORTAL_NEWS);					
												if result:
													response['status'] = "success"
													response['chatbotresponse'] = result
													response['do_you_want'] = "Do you want to see more? If you are then please click on Yes else No"
													print ("initial_sentence", initial_sentence)
													print("makeitastring", makeitastring)
													if str(initial_sentence) == str(makeitastring):								
														response['wait_looking'] = "Just a sec, I am looking that up"
														response['matched_word'] = "Here are the most relevant news results for" +" "+ makeitastring
													else:
														response['wait_looking'] = "Showing results for" +" "+ makeitastring
														response['matched_word'] = "No results found for" +" "+ initial_sentence
											else:
												response['status'] = "chat_success"
												response['chatbotresponse'] = str(random.choice(data)) 
										else:
											response['status'] = "error"
											response['message'] = "I think you have entered which we can't give information"																		
									else:								
										response= get_eliza_chat_response(response, modified_string);	
						else:
							if not longest_stirng:
								longest_stirng = matched_word1[0]
							pass_to_site = "-".join(tuple(re.sub("[^\w]", " ",  longest_stirng).split()))
							makeitastring = ' '.join(map(str, modified_string))
							my_string = makeitastring.rstrip('.,')
							
							print("longest_stirng", longest_stirng)
							if longest_stirng == my_string:
								response= pass_string_site(pass_to_site, initial_sentence, makeitastring, response, longest_stirng);
							else:
								print("modified_string", modified_string)
								removed_special_chars_str = re.sub('[^a-zA-Z0-9-]', ' ', makeitastring)
								print("removed_special_chars_str", removed_special_chars_str)
								check_spelling = [word for word in removed_special_chars_str if re.sub('[^a-zA-Z0-9-]', '', word) not in english_words]
								
								if check_spelling:
									print(check_spelling)					
									makeproper_sentence= "your search" +" "+ makeitastring + " " + "did not match any document"
									response = {'status':'error', 'message': makeproper_sentence}
								else:
									print("makeitastring sent_tokenize", makeitastring)
									sent_tokenize_list = sent_tokenize(makeitastring)
									print('len(sent_tokenize_list)',len(sent_tokenize_list))
									if len(sent_tokenize_list) ==1:
										X_test = np.array([makeitastring])
										# target_names = ['news', 'conversation']
										X_train = training.gettrainingdata();
										y_train_text = training.giving_response_data();

										lb = preprocessing.LabelBinarizer()
										Y = lb.fit_transform(y_train_text)

										classifier = Pipeline([
										('vectorizer', CountVectorizer()),
										('tfidf', TfidfTransformer()),
										('clf', OneVsRestClassifier(LinearSVC()))])

										classifier.fit(X_train, Y)
										predicted = classifier.predict(X_test)
										all_labels = lb.inverse_transform(predicted)

										for item, labels in zip(X_test, all_labels):
											classified_ans = (labels)	

										print("classified_ans1", classified_ans)
										if classified_ans == 1:								
											response= pass_string_site(pass_to_site, initial_sentence, makeitastring, response, longest_stirng);
										if classified_ans == 2:
											print("trivia questions")

											num_page = 3
											search_results = google.search("This is my query", num_page)
											print(search_results)
											response['status'] = "error"
											response['message'] = "this is trivia question"
										else:
											response= get_eliza_chat_response(response, modified_string);
									else:
										for token_setence in range(len(sent_tokenize_list)):										
											X_test = np.array([sent_tokenize_list[token_setence]])
											# target_names = ['news', 'conversation']
											X_train = tokenize_training.gettrainingdata();
											y_train_text = tokenize_training.giving_response_data();

											lb = preprocessing.LabelBinarizer()
											Y = lb.fit_transform(y_train_text)

											classifier = Pipeline([
											('vectorizer', CountVectorizer()),
											('tfidf', TfidfTransformer()),
											('clf', OneVsRestClassifier(LinearSVC()))])

											classifier.fit(X_train, Y)
											predicted = classifier.predict(X_test)
											all_labels = lb.inverse_transform(predicted)

											for item, labels in zip(X_test, all_labels):
												classified_ans = (labels)	

											print("classified_ans1222", classified_ans)
											if classified_ans == 1:
												if longest_stirng in sent_tokenize_list[token_setence]:
													response= pass_string_site(pass_to_site, initial_sentence, makeitastring, response, longest_stirng);
													break
												else:
													keyword_exist = [x for x in matched_word1 if x in sent_tokenize_list[token_setence]]								
													if keyword_exist:
														longest_stirng = max(keyword_exist, key=len)
														pass_to_site = "-".join(tuple(re.sub("[^\w]", " ",  longest_stirng).split()))
														print('keyword_exist',keyword_exist)
														response= pass_string_site(pass_to_site, initial_sentence, makeitastring, response, longest_stirng);
														break
													else:
														token_count = token_setence
														while (token_count >=0):
															token_count = token_count - 1
															if longest_stirng in sent_tokenize_list[token_count]:
																response= pass_string_site(pass_to_site, initial_sentence, makeitastring, response, longest_stirng);										
																break
															else:
																keyword_exist = [x for x in matched_word1 if x in sent_tokenize_list[token_count]]
																if keyword_exist:
																	longest_stirng = max(keyword_exist, key=len)
																	pass_to_site = "-".join(tuple(re.sub("[^\w]", " ",  longest_stirng).split()))
																	print('keyword_exist else',keyword_exist)
																	response= pass_string_site(pass_to_site, initial_sentence, makeitastring, response, longest_stirng);	
																	break
														
											else:
												response= get_eliza_chat_response(response, modified_string);
					else:
						response = {'status':'error', 'message': 'Oh I am sorry if i have done some thing wrong? or be polite dont use harse words' +" "+ "(;_;)"}
				else:
					response = {'status':'error', 'message':'What are you asking'}
			else:
				response = {'status':'error', 'message':'What are you asking'}
		else:
			response = {'status':'error', 'message':'Please enter something'}
	else:
		response = {'status':'error', 'message':'Error'}


	with open(module_dir + '/logfile.txt', "a") as text_file:
		if response:
			if not response['status'] == "success":			
				convert_str = response
				text_file.write(str(initial_sentence) + '\n')
				text_file.write(str(convert_str) + '\n')
			else:
				convert_str = {'status':'success', 'message':'Giving news'}
				text_file.write(str(initial_sentence) + '\n')
				text_file.write(str(convert_str) + '\n')
			text_file.close()
		else:
			response['status'] = "error"
			response['message'] = "I am here to give information of tech news like amazon,flipkart,google etc."
	return HttpResponse(json.dumps(response), content_type='application/json')


#Function for generating Combination of list values
def phrase_builder(words):
    for start in range(0, len(words)-1):
        for end in range(start+2, len(words)+1):
            yield ' '.join(words[start:end])

def get_eliza_chat_response(response, modified_string):
	makeitastring = ' '.join(map(str, modified_string))
	bots = [(eliza_chat,  'Eliza (psycho-babble)')]         
	chatbot = bots[int(1)-1][0]
	string1 = makeitastring
	nltkres = chatbot.eliza_chat(string1)
	print("Success")
	response['status'] = "chat_success"
	response['chatbotresponse'] = str(nltkres)
	return response

def pass_string_site(pass_to_site, initial_sentence, makeitastring, response, longest_stirng):
	site = str(settings.TECHPORTAL+'/'+pass_to_site+'/feed/')
	print(site)
	result = get_news(site);					
	if result:
		response['status'] = "success"
		response['do_you_want'] = "Do you want to see more news? If you are then please click on Yes else No"
		response['chatbotresponse'] = result
		#initial_sentence = initial_sentence.rstrip('?')
		print(initial_sentence)
		print(makeitastring)
		if initial_sentence == makeitastring:								
			response['wait_looking'] = "Just a sec, I am looking that up"
			response['matched_word'] = "Here are the most relevant news results for" +" "+ longest_stirng
		else:
			response['wait_looking'] = "Showing results for" +" "+ makeitastring
			response['matched_word'] = "No results found for" +" "+ initial_sentence
	else:
		response['status'] = "error"
		response['message'] = "I think you have entered which we can't give information"
	return response


def get_news(site = None):
	print("site", site)
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
	result = []	
	try:
		req = urllib2.Request(site, headers=hdr)
		xmlfile = urllib2.urlopen(req)
		the_page = xmlfile.read()
		parser = etree.XMLParser(recover=True)
		root = etree.fromstring(the_page, parser=parser)
	except:
		return result	
	
	for title in root.findall("./channel/item"):
		data={}
		titles = title.find('title')
		link = title.find('link')
		description = title.find('description')
		image1 = title.find('image1')
		titless= str(unicode(titles.text.encode('ascii', 'ignore')).replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", ""))
		link= str(unicode(link.text.encode('ascii', 'ignore')).replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", ""))
		if description.text:
			description = str(unicode(description.text.encode('ascii', 'ignore')).replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", ""))
		if image1.text:
			image1 = str(unicode(image1.text.encode('ascii', 'ignore')).replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", ""))
		data['title'] = str(titless)
		data['link'] = str(link)
		if description:
			data['description'] = str(description)
		if image1:
			data['image1'] = str(image1)
		if data:
			result.append(data)
	if result:
		return result


def words(text): return re.findall(r'\w+', text.lower())

#Getting current directory and opening big.txt file
module_dir = os.path.dirname(__file__)
WORDS = Counter(words(open(module_dir + '/techport_dict.txt').read()))

def P(word, N=sum(WORDS.values())):
	"Probability of `word`."
	return WORDS[word] / N

def correction(word): 
	"Most probable spelling correction for word."
	return max(candidates(word), key=P)

def candidates(word): 
	"Generate possible spelling corrections for word."
	return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
	"The subset of `words` that appear in the dictionary of WORDS."
	return set(w for w in words if w in WORDS)

def edits1(word):
	"All edits that are one edit away from `word`."
	letters    = 'abcdefghijklmnopqrstuvwxyz'
	splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
	deletes    = [L + R[1:]               for L, R in splits if R]
	transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
	replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
	inserts    = [L + c + R               for L, R in splits for c in letters]
	return set(deletes + transposes + replaces + inserts)

def edits2(word): 
	"All edits that are two edits away from `word`."
	return (e2 for e1 in edits1(word) for e2 in edits1(e1))
