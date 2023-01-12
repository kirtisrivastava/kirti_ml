import csv
from mikemaccana.docx import opendocx, getdocumenttext 

import numpy as np
import re

import os

import textwrap
from itertools import groupby
import os.path

from PIL import Image, ImageEnhance, ImageFilter
from pptx import Presentation
import zipfile
import sys
from tika import parser

class DocumentClass():

    def __init__(self, training_class):
        self.training_class = training_class 
        return

    def get_paragraphs(self, filename, min_characters=3):
        if filename.endswith('.txt'):
            pass
        elif filename.endswith('.docx'):
            return self.docxpattern(filename)           
                
        elif filename.endswith('.pdf'):            
            return self.pdfpattern(filename)   
            
        elif os.path.splitext(filename )[1]  in [".png" , ".jpg" , ".gif" , ".tga" , ".tiff" , ".bmp"]:
            return self.imagepattern(filename)

       
            

        elif filename.endswith(".pptx"):
            return self.pptxpattern(filename)    
            
        elif filename.endswith(".xlsx"):
            return self.xlsxpattern(filename)
            
        elif os.path.splitext(filename )[1]  in [".zip" , ".rar" ]:
            return self.zippattern(filename)   
        
        return  

    def  docxpattern(self,filename,min_characters=3):
        document = opendocx(filename)
        paratextlist = getdocumenttext(document)
        
        original_list=[]
        newparatextlist = []
        for paratext in paratextlist:
            encoded_text = paratext.encode("utf-8")                
            cleaned_text = self.training_class.do_cleaning(encoded_text)

            if len(cleaned_text) <= min_characters:
                continue                    
            newparatextlist.append(cleaned_text)
            
            original_list.append(encoded_text)

        return newparatextlist



    def pdfpattern(self,filename,min_characters=3):

        os.system("pdftotext %s output.txt"%filename)
            
            # converting textfile to paargraph               
        with open("output.txt") as f:
            list_para=[]
            for k, sec in groupby(f,key=lambda x: bool(x.strip())):
                if k:
                    list_para.append(list(sec))
        #flattening the list 
        paratextlist = [item for sublist in list_para for item in sublist]
        
        original_list=[]
        newparatextlist = []
        for paratext in paratextlist :
            
            encoded_text = paratext.encode("utf-8")
            
            cleaned_text = self.training_class.do_cleaning(encoded_text)
            if len(cleaned_text) <= min_characters:
                continue              
            newparatextlist.append(cleaned_text)
           
            original_list.append(paratext)

        return newparatextlist

    def imagepattern(self,filename,min_characters=3):
        

        os.system('"pdf2txtocrcmd\pdf2txtocr.exe" -layout %s 03.txt'%filename)
        # converting textfile to paargraph
        with open("03.txt", encoding="utf8") as f:
            list_para=[]
            for k, sec in groupby(f,key=lambda x: bool(x.strip())):
                if k:
                    list_para.append(list(sec))
        print (list_para)
        #flattening the list 
        paratextlist = [item for sublist in list_para for item in sublist]
                
        

        original_list=[]
        newparatextlist = []
        for paratext in paratextlist :                
            cleaned_text = self.training_class.do_cleaning(paratext)
            if len(cleaned_text) <= min_characters:
                continue              
            newparatextlist.append(cleaned_text)
            
            original_list.append(paratext)
       

        return newparatextlist


    def docpattern(self,filename,min_characters=3):
        wordapp = win32com.client.gencache.EnsureDispatch("Word.Application")
        save_path = 'E:/kirti/'
        
        filename =  os.path.join('E:', os.sep, 'kirti', 'harat_law_project', filename)
                               
        wordapp.Documents.Open(filename)
        docastxt = filename.rstrip('doc') + 'txt'
        completeName = os.path.join(save_path, docastxt)
        wordapp.ActiveDocument.SaveAs(completeName, FileFormat=win32com.client.constants.wdFormatTextLineBreaks)
        wordapp.ActiveWindow.Close()
    
        file = os.path.splitext(filename )[0] +'.txt'
        # converting textfile to paragraph
        with open(file) as f:
                list_para=[]
                for k, sec in groupby(f,key=lambda x: bool(x.strip())):
                    if k:       
                        list_para.append(list(sec))
        
        #flattening the list        
        paratextlist = [item for sublist in list_para for item in sublist]
        
        original_list=[]
        newparatextlist = []
        for paratext in paratextlist :
            decoded_text = paratext.decode('windows-1252')
            encoded_text = decoded_text.encode("utf-8")
            
            cleaned_text = self.training_class.do_cleaning(encoded_text)
            if len(cleaned_text) <= min_characters:
                continue              
            newparatextlist.append(cleaned_text)
           
            original_list.append(paratext)

        return newparatextlist


    def pptxpattern(self,filename,min_characters=3):
        prs = Presentation(filename)
        paratextlist = []
        l= open('input.txt','wb')
        
        text = parser.from_file(filename)
        l.write(text['content'].replace(u'\xa0', ' ').encode('utf-8'))
        # converting textfile to paragraph
        with open("input.txt") as l:
            list_para=[]
            for k, sec in groupby(l,key=lambda x: bool(x.strip())):
                if k:
                    list_para.append(list(sec))
        #flattening the list 
        paratextlist = [item for sublist in list_para for item in sublist]
        
         
        original_list=[]
        newparatextlist = []
        for paratext in paratextlist:                
                           
            cleaned_text = self.training_class.do_cleaning(paratext)
            if len(cleaned_text) <= min_characters:
                continue                    
            newparatextlist.append(cleaned_text)                
            original_list.append(paratext)
            l.close()

        return newparatextlist


    def xlsxpattern(self,filename,min_characters=3):
        f = open('in.txt',"w")
        text = parser.from_file(filename)
        f.write(text['content'].replace(u'\xa0', ' ').encode('utf-8'))
        # converting textfile to paragraph
        with open("in.txt") as f:
            list_para=[]
            for k, sec in groupby(f,key=lambda x: bool(x.strip())):
                if k:
                    list_para.append(list(sec))
        print (list_para)
        #flattening the list 
        paratextlist = [item for sublist in list_para for item in sublist]   
        original_list=[]
        newparatextlist = []
        for paratext in paratextlist :                
            cleaned_text = self.training_class.do_cleaning(paratext)
            if len(cleaned_text) <= min_characters:
                continue              
            newparatextlist.append(cleaned_text)
            
            original_list.append(paratext)
        f.close()

        return newparatextlist


    def zippattern(self,filename,min_characters=3):
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall('E:/kirti/harat_law_project')
        for filename in zip_ref.namelist():
            if filename.endswith('.docx'):
                return self.docxpattern(filename)
            elif filename.endswith('.pdf'):
                return self.pdfpattern(filename)
            elif os.path.splitext(filename )[1]  in [".png" , ".jpg" , ".gif" , ".tga" , ".tiff" , ".bmp"]: 
                # appending all coming images
                images = map(Image.open, zip_ref.namelist())
                widths, heights = zip(*(i.size for i in images))

                total_width = sum(widths)
                max_height = max(heights)

                new_im = Image.new('RGB', (total_width, max_height))

                x_offset = 0
                for im in images:
                    new_im.paste(im, (x_offset,0))
                    x_offset += im.size[0]

                new_im.save('test.jpg')


                return self.imagepattern('test.jpg')

            elif filename.endswith(".doc"):
                return self.docpattern(filename)

            elif filename.endswith(".pptx"):
                return self.pptxpattern(filename)

            elif  filename.endswith(".xlsx"):
                return self.xlsxpattern(filename)

        zip_ref.close()

        return newparatextlist




#C:\Python27\Lib\site-packages\