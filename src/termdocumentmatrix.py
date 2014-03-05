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

from itertools import chain, izip
from sets import Set
from math import sqrt, log

from document import Document
from vector import Vector

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
