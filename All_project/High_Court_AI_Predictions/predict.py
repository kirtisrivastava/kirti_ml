
# Usage: python predict.py model_dir 

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
    return pickle.load(open("%s.pkl" % model_file, "rb"))

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
        outfile.write("%s,%s,%f,%s\n" % (document_filename, predictions_str[i], np.max(predictions_prob[i]), test_data[i]))
    return

def do_predictions(label_maps_file, model_dir, documents_dir, output_dir):

    # Loading data
    labels_map_class = LabelMapping(label_maps_file) 
    training_class = TrainingData(labels_map_class)
    document_class = DocumentClass(training_class)
    vectorizer = get_unpickle_file("%s/vectorizer" % model_dir)
    ch2_selector = get_unpickle_file("%s/selector" % model_dir)
    ecoc_model = get_unpickle_file("%s/ecoc" % model_dir)
    ecoc_sf_model = get_unpickle_file("%s/ecoc_sf" % model_dir)
    naive_bayes_model = get_unpickle_file("%s/naive_bayes" % model_dir)
    naive_bayes_sf_model = get_unpickle_file("%s/naive_bayes_sf" % model_dir)

    out_file = open("%s/ecoc_predictions.csv" % (output_dir), "w")

    document_files = [f for f in os.listdir(documents_dir) if os.path.isfile(os.path.join(documents_dir, f))] 
    for document_file in document_files:
        print (document_file)
        test_data = document_class.get_paragraphs(os.path.join(documents_dir, document_file))
        X_test = vectorizer.transform(test_data)
        X_test_sf = ch2_selector.transform(X_test)
        predictions_ecoc_str = get_predictions(labels_map_class, ecoc_model, X_test)
        predictions_naive_bayes_str = get_predictions(labels_map_class, naive_bayes_model, X_test)
        predictions_naive_bayes_probability = get_predictions_probability(labels_map_class, naive_bayes_model, X_test)
        write_predictions(document_file, test_data, predictions_naive_bayes_str, predictions_naive_bayes_probability, out_file)
    out_file.close()

    return

label_maps_file = sys.argv[1]
model_dir = sys.argv[2]
documents_dir = sys.argv[3]
output_dir = sys.argv[4]

os.system("mkdir %s" % (output_dir))
do_predictions(label_maps_file, model_dir, documents_dir, output_dir)
