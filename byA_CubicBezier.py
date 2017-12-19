# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 16:21:05 2017

@author: orhanda
"""
from svgpathtools import CubicBezier, Path
from byA_FrozenClass import byA_FrozenClass
from byA_Point import byA_Point

class byA_CubicBezier(byA_FrozenClass):
    def __init__(self,**kwargs):
        super(byA_CubicBezier, self).__init__(self)
        self._from = kwargs.get('P1')
        self._fromcontrol = kwargs.get('C1')
        self._tocontrol = kwargs.get('C2')
        self._to = kwargs.get('P2')
        assert isinstance(self._from, byA_Point)
        assert isinstance(self._fromcontrol, byA_Point)
        assert isinstance(self._tocontrol, byA_Point)
        assert isinstance(self._to, byA_Point)
        self._svgcubicbezier = CubicBezier(self._from.toRI(), self._fromcontrol.toRI(), self._tocontrol.toRI(), self._to.toRI())
        self._freeze("byA_CubicBezier")
    def toStr(self):
        return Path(self._svgcubicbezier).d()
    def reverse(self):
        return byA_CubicBezier(P1=self._to, C1=self._tocontrol, C2=self._fromcontrol, P2=self._from)
    def split(self, t):
        P12 = self._from + t*(self._fromcontrol - self._from)
        P23 = self._fromcontrol + t*(self._tocontrol - self._fromcontrol)
        P34 = self._tocontrol + t*(self._to - self._tocontrol)
        P123 = P12 + t*(P23-P12)
        P234 = P23 + t*(P34-P23)
        P1234 = P123 + t*(P234-P123)
        return (byA_CubicBezier(P1 = self._from, C1 = P12, C2 = P123, P2 = P1234),
                byA_CubicBezier(P1 = P1234, C1 = P234, C2 = P34, P2 = self._to))

if __name__ == '__main__':

    pt1 = byA_Point(x=0,y=0,name="1")
    pt2 = byA_Point(x=5,y=10,name="2")
    pt3 = byA_Point(x=25,y=10,name="3")
    pt4 = byA_Point(x=15,y=30,name="4")
    cb = byA_CubicBezier(P1=pt1,P2=pt2,C1=pt3,C2=pt4)
    print cb.toStr()
