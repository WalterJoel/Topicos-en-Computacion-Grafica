#!/usr/bin/env python
# -*- coding: utf-8 -*-
#con los comentarios puedo utilizar ñ y tildes
import operator
import re # Para poder limpiar el texto usando exp regulares
import nltk
import csv
import sys 
import os
import math
from math import log
from time import time
from nltk.stem.porter import*
reload(sys) 
sys.setdefaultencoding("utf-8")
from nltk.tokenize import sent_tokenize, word_tokenize  #Para tokenizar las palabras
from nltk.corpus import stopwords                       #Para las palabras vacias
from textblob import TextBlob as tb
import unicodedata  
from nltk.stem.lancaster import LancasterStemmer



def freq(word, doc):
    return doc.count(word)

def word_count(doc):
    return len(doc)

def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))


def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
    return 1 + count


def idf(word, list_of_docs):
    return math.log(len(list_of_docs) /
            float(num_docs_containing(word, list_of_docs)))


def tf_idf(word, doc, list_of_docs):
    return (tf(word, doc) * idf(word, list_of_docs))

class ProcesarTexto:
    # La libreria ofrece palabras en ingles para (STOPWORDS)
    #english_words    = set(stopwords.words('english'))
    english_words    =nltk.corpus.stopwords.words('english')
    new_stop_words   = ['also','many','certain'] #Extiendo mis stop english_words
    english_words.extend(new_stop_words)
    list_news        = []  
    total_news       = 0
    path             = ''
    # Nuevo Porter Stemmer 
    stemmer          = LancasterStemmer()    
    def __init__(self,nombreCarpeta):
        # Nombre de la carpeta donde estas todos los archivos
        self.path       = nombreCarpeta
        self.total_news = 0
    def abrir_carpeta(self):
        for filename in os.listdir(self.path):
            #Ruta exacta para abrir cada *.txt
            pathname   = os.path.join(self.path, filename) 
            #Abro el txt
            new        = open(pathname,'r')
            #Paso a un string el txt
            texto_temp = new.read()
            #Convierto a string
            texto_temp = str(texto_temp)
            #Convierto a minusculas
            texto_temp = texto_temp.lower()
            #Quito numeros y caracteres con exp regular
            texto_temp = re.sub('[^a-z ' ']',' ',texto_temp)
            self.list_news.append(texto_temp)
            self.total_news = self.total_news + 1
            #print texto_temp
    def tokenize(self):
        cont   = 0
        cont2  = 0 
        result = 0
        list_prioridades = [] 
        docs = {}
        palabras = []
        while cont < self.total_news:
            # Separo por comas
            string_temp =  self.list_news[cont].split()
            #print string_temp
            # Quito palabras vacias 
            texto_limpio = self.quitar_palabras_vacias(string_temp)
            #print texto_limpio
            # Diccionario donde almaceno
            docs[cont] = {'freq': {}, 'tf': {}, 'idf': {},
                        'tf-idf': {}, 'tokens': []}
            #divido por comas
            for token in texto_limpio:
                token = self.stemmer.stem(str(token))
                if(token in palabras):
                    pass
                else:
                    palabras.append(token)
                # Utilizo el algoritmo de Porter para Radizalizar cada palabra
                linea = token.split(',')
                #print linea 
                #Frecuencia para cada palabra 
                docs[cont]['freq'][token] = freq(token, texto_limpio)
                #Frecuencia TF
                docs[cont]['tf'][token]   = tf(token, texto_limpio)
                docs[cont]['tokens']      = texto_limpio
                #print str(linea)
            cont = cont + 1
        #print palabras
        outFile = open("example.words.js", 'a')        
        #Haciendo el calculo para todos
        while cont2 < self.total_news:
            for token in docs[cont2]['tf']:
                # Frecuencia I
                docs[cont2]['idf'][token] = idf(token, texto_limpio)
                # TF*IDF para cada token
                docs[cont2]['tf-idf'][token] = tf_idf(token, docs[cont2]['tokens'], texto_limpio)
            cont2 = cont2+1
        #Genero mi JAVASCRIPT
        cont3=0
        javascript = {}
        outFile.write("var words = ["+"\n")
        while cont3 < self.total_news:
            #ordeno de mayor a menor
            #print sorted(docs[cont3]['tf-idf'].values(),reverse=True)
            #sorted(docs[cont3]['tf-idf'].values(),reverse=True)
            for token in docs[cont3]['tf-idf']:
                if(docs[cont3]['tf-idf'][token]!= float(0.0)):
                    javascript["palabra"] = token
                    javascript["tf-idf"]  = docs[cont3]['tf-idf'][token]
                    #outFile.write("{"+"text:"+"'"+token+"',"+"size:"+str(docs[cont3]['tf-idf'][token]) +"}," +"\n")
            cont3 = cont3+1
        cont3=0
        sorted(javascript['palabra'].values(),reverse=True)
        while cont3 < self.total_news:
            #ordeno de mayor a menor
            for token in javascript:
                print token
                outFile.write("{"+"text:"+"'"+token+"',"+"size:"+str(javascript['tf-idf']) +"}," +"\n")
            cont3 = cont3+1
        outFile.write("];")
        outFile.close()
    def quitar_palabras_vacias(self,string_tokenizado):
        string_temp = []
        for w in string_tokenizado:
            # si la palabra no esta dentro de la lista de spanish_words qiere decir q no es vacia y la agrego
            if w not in self.english_words:
                string_temp.append(w)
        return string_temp

def main():
    objetoProcesar = ProcesarTexto("rd") # Recibo como parametro la carpeta donde estan los archivos 
    objetoProcesar.abrir_carpeta()
    objetoProcesar.tokenize()
main()

