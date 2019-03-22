# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 11:22:36 2019

@author: orhanda
"""
import math
from byA_FrozenClass import byA_FrozenClass

class byA_Point(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._name = kwargs.get('name', "")
        if 'c' not in kwargs:
            self._x = kwargs.get('x', 0)
            self._y = kwargs.get('y', 0)
        else:
            c = kwargs.get('c', 0+0j)
            if isinstance(c, complex):
                self._x = c.real
                self._y = c.imag
            elif isinstance(c, byA_Point):
                self._x = c._x
                self._y = c._y
            else:
                self._x = 0.0
                self._y = 0.0
        self._freeze("byA_Point")
    
     def toRI(self):
        """Point as a complex
        """
        return complex(self._x,self._y)

     def toSVGWrite(self, drawing, **extra):
        """to the svgwrite syntax
        """
        return drawing.circle(center=(self._x,self._y), r=3, **extra)

if __name__ == '__main__':

    pt1 = byA_Point(x=0,y=0,name="O")
    pt2 = byA_Point(x=5,y=10,name="A")
    print pt1, pt2
    print pt1.toRI(), pt2.toRI()
    
    