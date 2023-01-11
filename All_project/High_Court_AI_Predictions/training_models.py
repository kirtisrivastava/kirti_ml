
# Usage: python training_models.py train_file test_file label_map_file model_dir 

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
from training_data import TrainingData

DO_DEBUG = 0 
NUM_FEATURES_PER_CLASSSES = 20

def get_vectorize_features(model_file, train_data, test_data): 
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
    X_train = vectorizer.fit_transform(train_data)
    X_test = vectorizer.transform(test_data)
    pickle.dump(vectorizer, open("%s.pkl" % model_file, "wb"))
    return vectorizer, X_train, X_test

def get_selected_features(model_file, vectorizer, X_train, Y_train, X_test, num_features):
    feature_names = vectorizer.get_feature_names()
    ch2 = SelectKBest(chi2, num_features)
    X_train_sf = ch2.fit_transform(X_train, Y_train)
    X_test_sf = ch2.transform(X_test)
    pickle.dump(ch2, open("%s.pkl" % model_file, "wb"))
    selected_feature_names = [feature_names[i] for i in ch2.get_support(indices=True)]
    return ch2, selected_feature_names, X_train_sf, X_test_sf

def print_metrics(model_name, Y_test, Y_predictions):
    score = metrics.accuracy_score(Y_test, Y_predictions)
    print ("%s Accuracy, %f" % (model_name, score))

def ecoc_model(model_file, num_classes, X_train, Y_train, X_test):
    ecoc = OutputCodeClassifier(LinearSVC(), n_jobs=6, code_size=num_classes*2)
    ecoc.fit(X_train, Y_train)
    pickle.dump(ecoc, open("%s.pkl" % model_file, "wb"))
    predictions = ecoc.predict(X_test)
    return predictions

def naive_bayes_model(model_file, num_classes, X_train, Y_train, X_test):
    naive_bayes = MultinomialNB(alpha=0.1, fit_prior=False)
    naive_bayes.fit(X_train, Y_train)
    pickle.dump(naive_bayes, open("%s.pkl" % model_file, "wb"))
    predictions = naive_bayes.predict(X_test)
    return predictions

def build_models(train_file, test_file, label_maps_file, model_dir):

    # Loading data
    labels_map_class = LabelMapping(label_maps_file) 
    training_class = TrainingData(labels_map_class)
    train_data, Y_train = training_class.load_training_data(train_file)
    test_data, Y_test = training_class.load_training_data(test_file)

    # Vectorize and do feature selection
    vectorizer, X_train, X_test = get_vectorize_features("%s/vectorizer" % model_dir, train_data, test_data)
    num_features = labels_map_class.get_num_classes() * NUM_FEATURES_PER_CLASSSES 
    ch2, selected_feature_names, X_train_sf, X_test_sf = get_selected_features("%s/selector" % model_dir,\
                    vectorizer, X_train, Y_train, X_test, num_features)
    if DO_DEBUG:
        print ("Selected Features:", selected_feature_names)

    # Build and save models
    num_classes = labels_map_class.get_num_classes()
    ecoc_predictions = ecoc_model("%s/ecoc" % model_dir, num_classes, X_train, Y_train, X_test)
    ecoc_sf_predictions = ecoc_model("%s/ecoc_sf" % model_dir, num_classes, X_train_sf, Y_train, X_test_sf)
    naive_bayes_predictions = naive_bayes_model("%s/naive_bayes" % model_dir, num_classes, X_train, Y_train, X_test)
    naive_bayes_sf_predictions = naive_bayes_model("%s/naive_bayes_sf" % model_dir, num_classes, X_train_sf, Y_train, X_test_sf)

    # Print metrics
    print_metrics("ecoc", Y_test, ecoc_predictions)
    print_metrics("ecoc_sf", Y_test, ecoc_sf_predictions)
    print_metrics("naive_bayes", Y_test, naive_bayes_predictions)
    print_metrics("naive_bayes_sf", Y_test, naive_bayes_sf_predictions)

    return

train_file = sys.argv[1]
test_file = sys.argv[2]
label_maps_file = sys.argv[3]
model_dir = sys.argv[4]
os.system("mkdir -p %s" % model_dir)
build_models(train_file, test_file, label_maps_file, model_dir)
