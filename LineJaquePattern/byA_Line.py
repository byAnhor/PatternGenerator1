# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 11:31:58 2019

@author: orhanda
"""
from math import sqrt
import svgwrite 
from svgpathtools import Line
from byA_FrozenClass import byA_FrozenClass
from byA_Point import byA_Point

class byA_Line(byA_FrozenClass):
    
     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._from = kwargs.get('P1')
        self._to = kwargs.get('P2')
        assert isinstance(self._from, byA_Point)
        assert isinstance(self._to, byA_Point)
        self._svgpathtools = Line(self._from.toRI(), self._to.toRI())
        self._freeze("byA_Line")

     def toRI(self):
        """Point as a complex
        """
        return complex(self._from.toRI()), complex(self._to.toRI())

     def toSVGWrite(self, drawing, **extra):
        """to the svgwrite syntax
        """
        return drawing.line((self._from._x,self._from._y),(self._to._x,self._to._y), **extra)

     def lenght(self):
        """to the svgwrite syntax
        """
        return sqrt((self._from.toRI().real - self._to.toRI().real )**2 + (self._from.toRI().imag - self._to.toRI().imag )**2)

if __name__ == '__main__':

    ptO = byA_Point(x=0,y=0,name="O")
    ptA = byA_Point(x=5,y=10,name="A")
    lineAO = byA_Line(P1 = ptO, P2 = ptA)
    print lineAO.toRI()