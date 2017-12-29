# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:58:14 2017

@author: orhanda
"""

class byA_FrozenClass(object):
  """ When a class herits from this mother class, it cannot create new attributes that have not been 
      already declared in __init__ method   
  """
  __isFrozen = False
  def __init__(self, *args, **kwargs): pass
  def __setattr__(self, attr, value):
    print attr, value
    if self.__isFrozen and not hasattr(self, attr):
      raise TypeError("%r is a frozen class, please declare attribute %r in __init__" % (self.__class__.__name__, attr))
    super(byA_FrozenClass, self).__setattr__(attr, value)

  def _freeze(self, instance):
    if (self.__class__.__name__ == instance):
      self.__isFrozen = True
