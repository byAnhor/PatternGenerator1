# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 15:18:06 2017

@author: orhanda
"""
import svgwrite  
from svgwrite import cm, mm
from byA_FrozenClass import byA_FrozenClass

PXCM = 1.0/35.43307

class byA_PatternArea(byA_FrozenClass):
    def __init__(self, id, **extra):
        self._id = id
        self._g = svgwrite.container.Group(id=id, **extra)
        self._freeze("byA_PatternArea")
        
    def add(self, something):
        if (isinstance(something, svgwrite.shapes.Circle)):
            self._g.add(something)
        elif (isinstance(something, svgwrite.text.Text)):
            self._g.add(something)
        else:
            self._g.add(something._g)
        return self
        
    def add_subarea(self, subareaId):
        subarea = byA_PatternArea(self._g.get_id()+subareaId)
        self.add(subarea)
        return subarea

    def add_circle(self, x, y, r, **extra):
        svgcircle = svgwrite.shapes.Circle(center=(x*PXCM*cm, y*PXCM*cm), r=str(r*PXCM)+'cm', **extra)
        self.add(svgcircle)
        
    def add_text(self, text, x, y, **extra):
        svgtext = svgwrite.text.Text(text, insert=(x*PXCM*cm, y*PXCM*cm), **extra)
        self.add(svgtext)

if __name__ == '__main__':
    
    test1 = byA_PatternArea(id = 'test1')
    print test1
    test2 = byA_PatternArea(id = 'test2')
    print test2
    test1.add(test2)
    print test1
    

