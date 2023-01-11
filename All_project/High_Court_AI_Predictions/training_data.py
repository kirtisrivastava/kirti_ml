import csv
import numpy as np
import re

class TrainingData():

    def __init__(self, label_maps_class, delimiter=','):
        self.label_maps_class = label_maps_class 
        self.delimiter = delimiter
        self.regex = re.compile("[.?!,\":;()&%|<>\(#\)\\\~]", re.UNICODE)
        return

    def do_cleaning(self, input_str):
        input_str = self.regex.sub(' ', input_str.decode('utf-8').lower())
        input_str = " ".join(input_str.split())
        return input_str

    def load_training_data(self, filename, label_index=0, data_index=1, do_cleaning=1):

        data = []
        labels = []

        with open(filename) as tsv:
            for line in csv.reader(tsv, delimiter=self.delimiter):
                if len(line) < label_index or len(line) < data_index:
                    print ("Incorrect line:", line)
                    continue

                label_data = self.label_maps_class.get_label_value(line[label_index])
                text_data = line[data_index]
                if do_cleaning:
                    text_data = self.do_cleaning(text_data)

                data.append(text_data)
                labels.append(label_data)

        return data, np.array(labels)
