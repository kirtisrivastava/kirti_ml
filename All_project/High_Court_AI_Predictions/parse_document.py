import csv
from mikemaccana.docx import opendocx, getdocumenttext 
import numpy as np
import re

class DocumentClass():

    def __init__(self, training_class):
        self.training_class = training_class 
        return

    def get_paragraphs(self, filename, min_characters=10):

        document = opendocx(filename)
        paratextlist = getdocumenttext(document)

        newparatextlist = []
        for paratext in paratextlist:
            encoded_text = paratext.encode("utf-8")
            cleaned_text = self.training_class.do_cleaning(encoded_text)
            if len(cleaned_text) <= min_characters:
                continue
            newparatextlist.append(cleaned_text)

        return newparatextlist
