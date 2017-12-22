# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 21:30:08 2017

@author: orhanda
"""
from svgpathtools import Path
from byA_FrozenClass import byA_FrozenClass
from byA_Point import byA_Point
from byA_Line import byA_Line
from byA_CubicBezier import byA_CubicBezier

class byA_Path(byA_FrozenClass):
    def __init__(self, *segments, **kw):
        byA_FrozenClass.__init__(self)
        self._segments = Path()
        for p in segments:
            assert isinstance(p, byA_Line) or isinstance(p, byA_CubicBezier)  
            if isinstance(p, byA_Line):
                self.insert(-1, p)   
            if isinstance(p, byA_CubicBezier):
                self.insert(-1, p)   
        if 'closed' in kw:
            self._segments.closed = kw['closed']  # DEPRECATED
        self._freeze("byA_Path")
    def insert(self, index, value):
        assert isinstance(value, byA_Line) or isinstance(value, byA_CubicBezier)  
        if isinstance(value, byA_Line):
            self._segments.insert(index, value._svgline)   
        if isinstance(value, byA_CubicBezier):
            self._segments.insert(index, value._svgcubicbezier)   
    def append(self, value):
        assert isinstance(value, byA_Line) or isinstance(value, byA_CubicBezier)  
        if isinstance(value, byA_Line):
            self._segments.append(value._svgline)   
        if isinstance(value, byA_CubicBezier):
            self._segments.append(value._cubicbezier)   
    def toStr(self):
        return self._segments.d()

if __name__ == '__main__':

    pt1 = byA_Point(x=10,y=10)
    pt2 = byA_Point(x=20,y=15)
    pt3 = byA_Point(x=30,y=5)
    a = byA_Line(P1=pt1, P2=pt2)
    print a.toStr()
    c = byA_CubicBezier(P1=pt1, C1=pt3, C2=pt3, P2=pt2)
    print c.toStr()
    p = byA_Path(a, c)
    print p.toStr()