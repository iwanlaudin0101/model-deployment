# coding=utf-8
import time
import re
import string
import joblib
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.sequence import pad_sequences
from app import model, tokenizer, history


def text_cleaning(doc):
    """
    Buat teks menjadi huruf kecil, hapus teks dalam tanda kurung siku, hapus tautan,
    hapus tanda baca dan hapus kata-kata yang mengandung angka.
    """

    doc = doc.lower()
    doc = re.sub('\[.*?\]', '', doc)
    doc = re.sub('https?://\S+|www\.\S+', '', doc)
    doc = re.sub('<.*?>+', '', doc)
    doc = re.sub('[%s]' % re.escape(string.punctuation), '', doc)
    doc = re.sub('\n', ' ', doc)
    doc = re.sub('\w*\d\w*', '', doc)
    return doc

def stopwordsRemoval(doc):
    """
    Fungsi ini digunakan untuk mengfilter kata pada corpus
    dan mengembalikan kata-kata penting dari tiap-tiap dokumen.
    """

    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokenizer = tokenizer.tokenize(doc)
    listStopwords = set(stopwords.words('indonesian')+stopwords.words('english'))
    filtered = [s for s in tokenizer if s not in listStopwords]
    docFiltered = ' '.join(filtered)
    return docFiltered

class MakePredict:
    
    def __init__(self, document=None):
        self.documet = document
        self.result = {'article':[], 'class':[], 'predict':[]}

    def preprocessing(self):
        
        if isinstance(self.documet, pd.DataFrame):
            textCleaning = self.documet['article'].apply(lambda x: text_cleaning(x))
            filtered = textCleaning.apply(lambda x: stopwordsRemoval(x))
        else:
            textCleaning = text_cleaning(self.documet)
            filtered = [stopwordsRemoval(textCleaning)]

        
        return filtered

    def sequncesPadding(self):
        pprocss = self.preprocessing()

        seq_of_integer = tokenizer.texts_to_sequences(pprocss)
        seq_padding = pad_sequences(seq_of_integer, maxlen=200, padding='post')
        
        return seq_padding

    def inputPredict(self):
        fitures = self.sequncesPadding()
        predict = model.predict(np.array(fitures))
        predict = [round(i*100, 2) for i in predict[0]]
        
        return predict

    def filePredict(self):
        labels = np.array(['hiburan', 'olahraga', 'showbiz', 'tajuk utama', 'teknologi'])
        fitures = self.sequncesPadding()
        
        for i in range(len(fitures)):
            predict = model.predict(np.array([fitures[i]]))
            predicted_label = labels[np.argmax(predict)]

            self.result['article'].append(self.documet['article'].iloc[i][:50])
            self.result['class'].append(self.documet['category'].iloc[i])
            self.result['predict'].append(predicted_label)

        return self.result

    def history(self):
        return history