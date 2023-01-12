import csv
import sys

class LabelMapping():

    def __init__(self, label_map_filename, key_index=0, value_index=1, delimiter=','):
        self.label_map_filename = label_map_filename 
        self.delimiter = delimiter
        self.label_key_index = key_index 
        self.label_value_index = value_index
        self.num_classes = 0
        self.label_map_key_to_value = {}
        self.label_map_value_to_key = {}
        if self.load_label_and_inverse_mapping() == 1:
            sys.exit(1)

    def load_label_and_inverse_mapping(self):
        if not self.label_map_filename:
            return 1 

        with open(self.label_map_filename) as tsv:
            for line in csv.reader(tsv, delimiter=self.delimiter):
                if len(line) < self.label_key_index or len(line) < self.label_value_index:
                    print "load_label_and_inverse_mapping: Continuing, ignoring incorrect line", line
                    continue

                key = line[0]
                value = int(line[1])

                if not key or not value:
                    print "load_label_and_inverse_mapping: Continuing, key or value is None", line
                    continue

                if key in self.label_map_key_to_value:
                    print "load_label_and_inverse_mapping: Terminating, Duplicate key found:", key
                    return 1
                    
                if value in self.label_map_value_to_key: 
                    print "load_label_and_inverse_mapping: Terminating, Duplicate value found:", value 
                    return 1

                if value == 0:
                    print "load_label_and_inverse_mapping: Terminating, Zero value found, should start from 1", key, value 
                    return 1

                self.label_map_key_to_value[key] = value
                self.label_map_value_to_key[value] = key

        self.num_classes = len(self.label_map_key_to_value)

        return 0 

    def get_label_value(self, label_str):
        if label_str in self.label_map_key_to_value:
            return self.label_map_key_to_value[label_str]

        print "get_label_value: Continuing, label not found for key:", key 
        return -1

    def get_label_string(self, label_value):
        if label_value in self.label_map_value_to_key:
            return self.label_map_value_to_key[label_value]

        print "get_label_string: Continuing, label not found for value:", value 
        return -1

    def get_num_classes(self):
        return self.num_classes
