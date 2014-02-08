#!/usr/bin/env python
"""
   Author: Richard J. Marini (richardjmarini@gmail.com)
   Date: 02/05/2014
   Description:  Vector space search engine 
   Development Resources:
      http://en.wikipedia.org/wiki/Vector_space_model
      http://en.wikipedia.org/wiki/Tf-idf
      http://en.wikipedia.org/wiki/Cosine_similarity
      http://en.wikipedia.org/wiki/Norm_%28mathematics%29
"""

from nltk import word_tokenize, corpus
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from hashlib import md5

class Document(object):

   #stopwords= ("of", "in", "a", "the", "got", "into", "is", "it", "and", "-", ",", ".", "\n")
   stopwords= stopwords.words('english')

   def __init__(self, text):

      super(Document, self).__init__()

      self.text= text
      self.id= md5(text).hexdigest()

      stemmer= PorterStemmer()
      self.tokens= filter(lambda word: stemmer.stem(word.lower()) not in self.stopwords,  word_tokenize(self.text))

   def __repr__(self):
  
      return repr(self.text)
