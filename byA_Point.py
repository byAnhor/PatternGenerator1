# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:47:50 2017

@author: orhanda
"""
import math

class byA_Point():
    def __init__(self,**kwargs):
        self._name = kwargs.get('name', "O")
        if 'c' not in kwargs:
            self._x = kwargs.get('x', 0)
            self._y = kwargs.get('y', 0)
        else:
            c = kwargs.get('c', 0+0j)
            self._x = c.real
            self._y = c.imag
        self._drawn = kwargs.get('drawn', False)
        #print "Point", self._name," (", getattr(self,'_x'), ",", getattr(self,'_y'), ")"
    def __add__(self, other):  # Equivalent of + operator
        return byA_Point(x=self._x + other._x, y=self._y + other._y, name=self._name, drawn = self._drawn)
    def __sub__(self, other):  # Equivalent of - operator
        return byA_Point(x=self._x - other._x, y=self._y - other._y, name=self._name, drawn = self._drawn)
    def __mul__(self, other):  # Equivalent of * operator
        return byA_Point(x=self._x * other, y=self._y * other, name=self._name, drawn = self._drawn)
    def __rmul__(self, other):  # Equivalent of * operator
        return byA_Point(x=self._x * other, y=self._y * other, name=self._name, drawn = self._drawn)
    def translate(self, dx, dy):  
        self._x += dx
        self._y += dy
    def rotate(self, degre, centerot = None):  # Equivalent of * operator
        if centerot is None:
            x = self._x * math.cos(math.radians(degre)) - self._y * math.sin(math.radians(degre))
            y = self._x * math.sin(math.radians(degre)) + self._y * math.cos(math.radians(degre))
            self._x = x
            self._y = y
        else:
            self.translate(-centerot._x,-centerot._y)
            self.rotate(degre)
            self.translate(centerot._x,centerot._y)
    def toRI(self):
        return complex(self._x,self._y)

if __name__ == '__main__':

    pt1 = byA_Point(x=0,y=0,name="O")
    pt2 = byA_Point(x=5,y=10,name="A")
    pt3 = pt1+2*pt2
    print pt1.toRI()
    print pt2.toRI()
    print pt3.toRI()
    
    