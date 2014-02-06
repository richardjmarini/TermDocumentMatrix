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

from itertools import izip
from math import sqrt

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
