# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:45:41 2017

@author: byAnhor
"""
from svgpathtools import svg2paths, Path, Line, QuadraticBezier, CubicBezier, Arc, parse_path
from byA_FrozenClass import byA_FrozenClass
from byA_Point import byA_Point

class byA_Line(byA_FrozenClass):
    def __init__(self,**kwargs):
        byA_FrozenClass.__init__(self)
        self._from = kwargs.get('P1')
        self._to = kwargs.get('P2')
        assert isinstance(self._from, byA_Point)
        assert isinstance(self._to, byA_Point)
        self._svgline = Line(self._from.toRI(), self._to.toRI())
        self._freeze("byA_Line")
    def toStr(self):
        return Path(self._svgline).d()

if __name__ == '__main__':

    pt1 = byA_Point(x=0,y=0,name="O")
    pt2 = byA_Point(x=5,y=10,name="A")
    lineAO = byA_Line(P1 = pt1, P2 = pt2)
    print lineAO.toStr()