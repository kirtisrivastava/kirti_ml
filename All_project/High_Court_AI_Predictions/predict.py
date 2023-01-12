# Usage: python predict.py labels_map.csv model_dir documens_dir output_dir 

import numpy as np
import os
import pickle
import sys
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.multiclass import OutputCodeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC, SVC

from labels_map import LabelMapping 
from parse_document import DocumentClass 
from training_data import TrainingData

DO_DEBUG = 0 
NUM_FEATURES_PER_CLASSSES = 20

def get_unpickle_file(model_file): 
    
    
    return (pickle.load(open(model_file, "rb"),encoding='latin1'))

def get_predictions_probability(labels_map_class, model, X_test):
    predictions_prob = model.predict_proba(X_test)
    return predictions_prob

def get_predictions(labels_map_class, model, X_test):
    predictions = model.predict(X_test)
    predictions_str = []
    for prediction in predictions:
            predictions_str.append(labels_map_class.get_label_string(prediction))
    return predictions_str

def write_predictions(document_filename, test_data, predictions_str, predictions_prob, outfile):
    for i in range(0, len(test_data)):
        outfile.write("%s,%s,%f,%s\n" % (document_filename, predictions_str[i].encode('utf-8'), np.max(predictions_prob[i]), test_data[i].encode('utf-8')))
    return

def do_post_processing(test_data, predictions_str, predictions_probability):

    PARTY_STR = "PARTIES"
    TITLE_STR = "TITLE"
    SCORE_THRESHOLD = 0.5

    processed_test_data = []
    processed_predictions = []
    processed_probability = []

    found_title = 0
    
    for i in range(0, len(test_data)):
        doc_text = test_data[i]
        prediction = predictions_str[i]
        probability = np.max(predictions_probability[i])

        # Making sure only one TITLE is predicted, ignore rest
        if (i==0):           
            
            if found_title == 0: 
                found_title = 1
                prediction = TITLE_STR
                probability = 1
            else:
                continue

        # Make sure no other prediction in between series of PARTIES 
        if (i < len(predictions_str)-1) and (len(processed_predictions) >= 1) \
           and (processed_predictions[-1] == PARTY_STR) \
           and (predictions_str[i+1] == PARTY_STR):
            # print "Correcting prediction from: %s to %s" % (prediction, PARTY_STR)
            prediction = PARTY_STR
            probability = 1

        # Ignore threshold for PARTY_STR
        if prediction == PARTY_STR:
            probability = 1
            continue
        # Filter out predictions less than threshold
        # if probability < SCORE_THRESHOLD:
        #     continue

        processed_predictions.append(prediction)
        processed_probability.append(probability)
        processed_test_data.append(doc_text)
    
    return processed_test_data, processed_predictions, processed_probability


def do_predictions(label_maps_file, model_dir, documents_dir, output_dir):

    # Loading data
    labels_map_class = LabelMapping(label_maps_file) 
    training_class = TrainingData(labels_map_class)
    document_class = DocumentClass(training_class)
    vectorizer = get_unpickle_file("%s/vectorizer.pkl" % model_dir)
    ch2_selector = get_unpickle_file("%s/selector.pkl" % model_dir)
   
    naive_bayes_model = get_unpickle_file("%s/naive_bayes.pkl" % model_dir)
  

    out_file = open("%s/ecoc_predictions.csv" % (output_dir), "w")

    document_files = [f for f in os.listdir(documents_dir) if os.path.isfile(os.path.join(documents_dir, f))] 
    
    for document_file in document_files:
        print (document_file)
        test_data = document_class.get_paragraphs(os.path.join(documents_dir, document_file))
        
        X_test = vectorizer.transform(test_data)
        X_test_sf = ch2_selector.transform(X_test)
        
        predictions_naive_bayes_str = get_predictions(labels_map_class, naive_bayes_model, X_test)
        predictions_naive_bayes_probability = get_predictions_probability(labels_map_class, naive_bayes_model, X_test)
        processed_test_data, processed_predictions, processed_probabilities = do_post_processing(test_data, predictions_naive_bayes_str, predictions_naive_bayes_probability)
        write_predictions(document_file, processed_test_data, processed_predictions, processed_probabilities, out_file)
        

    out_file.close()

    return

label_maps_file =sys.argv[1]
model_dir = sys.argv[2]
documents_dir = sys.argv[3]
output_dir = sys.argv[4]

os.system("mkdir %s" % (output_dir))
do_predictions(label_maps_file,model_dir, documents_dir, output_dir)