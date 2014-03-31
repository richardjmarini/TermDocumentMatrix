#!/usr/bin/env python
#---------------------------------------------------------------------------
#   Author: Richard J. Marini (richardjmarini@gmail.com)
#   Date: 02/05/2014
#   Name: Vespse (Vector Space Search Engine)
#   Description:  A simple Vector space search engine 
#   Development Resources:
#      http://en.wikipedia.org/wiki/Vector_space_model
#      http://en.wikipedia.org/wiki/Tf-idf
#      http://en.wikipedia.org/wiki/Cosine_similarity
#      http://en.wikipedia.org/wiki/Norm_%28mathematics%29
#
#   License:
#      Vespse is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 2 of the License, or
#      any later version.
#
#      Vespse is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Vespe.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------------------------------------------

from itertools import izip
from math import sqrt, log
from itertools import chain, izip
from hashlib import md5
from sets import Set
from sys import exit

from nltk import word_tokenize, corpus
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class Vector(object):

   def __init__(self, elements):

      super(Vector, self).__init__()
      self.elements= elements

   def __repr__(self):

      return repr(self.elements)
    
   def norm(self):
      """
         ||x||:= sqrt( sum( x[i]^2 ) )
      """
      norm= sqrt(sum([frequency * frequency for frequency in self.elements]))

      return norm

   def dot(self, vector):
      """
      computers inner dot product of vectors
      """

      dot= sum([frequency1 * frequency2 for frequency1, frequency2 in izip(self.elements, vector)])

      return dot

   def cosine(self, vector):
      """
         sum( d[i] * q[i] ) / ( ||d|| * ||q|| )
         where:
            ||q||= sqrt( sum ( q[i]^2 ) )
      """
      try:
         cosine= self.dot(vector) / (self.norm() * Vector(vector).norm())
      except ZeroDivisionError:
         cosine= 0.0

      return cosine


class Document(object):

   #stopwords= ("of", "in", "a", "the", "got", "into", "is", "it", "and", "-", ",", ".", "\n")
   stopwords= stopwords.words('english') #+ ['aly', 'alley', 'arc', 'arcade', 'ave', 'avenue', 'bch', 'beach', 'bg', 'burg', 'bgs', 'burgs', 'blf', 'bluff', 'blvd', 'boulevard', 'bnd', 'bend', 'br', 'branch', 'brg', 'bridge', 'brk', 'brook', 'brks', 'brooks', 'btm', 'bottom', 'byp', 'bypass', 'byu', 'bayou', 'cir', 'circle', 'cirs', 'circles', 'clb', 'club', 'clf', 'cliff', 'clfs', 'cliffs', 'cmn', 'common', 'cor', 'corner', 'cors', 'corners', 'cp', 'camp', 'cpe', 'cape', 'cres', 'crescent', 'crk', 'creek', 'crse', 'course', 'crst', 'crest', 'cswy', 'causeway', 'ct', 'court', 'ctr', 'center', 'ctrs', 'centers', 'cts', 'courts', 'curv', 'curve', 'cv', 'cove', 'cvs', 'coves', 'cyn', 'canyon', 'dl', 'dale', 'dm', 'dam', 'ln', 'lane', 'rd', 'road', 'st', 'street', 'terr', 'terrace', 'xing', 'crossing'] + ['academy', 'acad.', 'association', 'assn.', 'assn', 'associates', 'assoc.', 'college', 'coll.', 'company', 'co.', 'corporation', 'corp.', 'doing business as', 'd.b.a.', 'dba', 'incorporated', 'inc.', 'institute/institution', 'inst.', 'limited', 'ltd.', 'ltd', 'limited liability company (or partnership)', 'llc', 'llc (llp)', 'public limited company', 'plc', 'manufacturing', 'mfg.', 'mfg', 'publishing', 'pubg.', 'pubg', 'publications', 'pub., pubs., pubs', 'press', 'pr.', 'university', 'univ.', 'u.', 'uni.']


   def __init__(self, text, id= None):

      super(Document, self).__init__()

      self.text= text
      self.id= id if id else md5(text).hexdigest() 

      stemmer= PorterStemmer()
      self.tokens= filter(lambda word: stemmer.stem(word.lower()).lower() not in self.stopwords,  word_tokenize(self.text))

   def __repr__(self):
  
      return repr(self.text)


class TermDocumentMatrix(dict):

   def __init__(self): #, *text):

      super(TermDocumentMatrix, self).__init__()

   def add(self, text, id= None):
     
      document= Document(text, id)

      self[document.id]= document

   def remove(self, id):

      del self[id]

   def index(self):

      (self.terms, self.matrix)= self.decompose(self.values())
    
   def decompose(self, documents):

      terms= list(Set(chain.from_iterable([document.tokens for document in documents])))

      matrix= [map(lambda term: self.term_frequency(term, document.tokens) * self.inverse_document_frequency(term, documents), terms) for document in documents]

      return (terms, matrix)

   @staticmethod
   def inverse_document_frequency(term, documents):
      """
         measures term commonality of term across documents

         log(  |D| / | {d e D | t e d} |
         where:
            |D|= number of documents
            1 + | {d e D | t e d} |= number of documents containing term
      """
      inverse_document_frequency= log(len(documents) / float(1 + sum([1 if term in document.tokens else 0 for document in documents])))

      return inverse_document_frequency

   @staticmethod
   def term_frequency(term, tokens):
      """
      measures number of occurences of term in document
      """

      term_frequency= tokens.count(term)

      return term_frequency

   def display(self):
      """
      displays the term relavance matrix for each document in the collection
      """

      doc_id= 0 
      for id, document in self.items():
         print "\n----------------------------------------"
         print "id:", id
         print "text:", document
         print "terms:",
         term_id= 0
         for term in self.terms:
            print "\t", term, self.matrix[doc_id][term_id]
            term_id+= 1
         doc_id+= 1
      print

   def find(self, query):
      """
      queries the document set and calculates realvance to query termss
      """

      query_vector= Vector(map(lambda term: Document(query).tokens.count(term), self.terms))

      cosines= [query_vector.cosine(vector) for vector in self.matrix]

      for result in izip(cosines, self.items()):
         yield result
