# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 16:21:05 2017

@author: orhanda
"""
from svgpathtools import CubicBezier, Path
from byA_FrozenClass import byA_FrozenClass
from byA_Point import byA_Point
from byA_Line import byA_Line

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
        self._svgpathtools = CubicBezier(self._from.toRI(), self._fromcontrol.toRI(), self._tocontrol.toRI(), self._to.toRI())
        self._freeze("byA_CubicBezier")

    def toSVGWrite(self, drawing, **extra):
        """to the svgwrite syntax
        """
        return drawing.path(d=self.toStr(), **extra)

    def toStr(self):
        return Path(self._svgpathtools).d()

    def reverse(self):
        return byA_CubicBezier(P1=self._to, C1=self._tocontrol, C2=self._fromcontrol, P2=self._from)

    def rotate(self, degre, origin=None):
        self._svgpathtools = self._svgpathtools.rotated(degre, origin)
        self._from.rotate(degre, origin)
        self._fromcontrol.rotate(degre, origin)
        self._tocontrol.rotate(degre, origin)
        self._to.rotate(degre, origin)
        
    def rotated(self, degre, origin=None):
        res = byA_CubicBezier(P1=self._from,C1=self._fromcontrol,C2=self._tocontrol,P2=self._to)
        res.rotate(degre, origin)
        return res

    def split(self, t):
        P12 = self._from + t*(self._fromcontrol - self._from)
        P23 = self._fromcontrol + t*(self._tocontrol - self._fromcontrol)
        P34 = self._tocontrol + t*(self._to - self._tocontrol)
        P123 = P12 + t*(P23-P12)
        P234 = P23 + t*(P34-P23)
        P1234 = P123 + t*(P234-P123)
        return (byA_CubicBezier(P1 = self._from, C1 = P12, C2 = P123, P2 = P1234),
                byA_CubicBezier(P1 = P1234, C1 = P234, C2 = P34, P2 = self._to))
    
    def lenght(self):
        line = byA_Line(P1=self._from,P2=self._to)
        l = line.lenght()
        points = self.courbe_bezier_3([self._from,self._fromcontrol,self._tocontrol,self._to],l*10)
        res = 0
        for point in range(0, len(points)-1):
            line = byA_Line(P1=points[point],P2=points[point+1])
            res += line.lenght()
        return res
        
    def combinaison_lineaire(self, A,B,u,v):
        assert isinstance(A, byA_Point)
        assert isinstance(B, byA_Point)
        return byA_Point(x = A._x*u+B._x*v, y = A._y*u+B._y*v)

    def point_bezier_3(self, points_control,t):
        x=(1-t)**2
        y=t*t
        A = self.combinaison_lineaire(points_control[0],points_control[1],(1-t)*x,3*t*x)
        B = self.combinaison_lineaire(points_control[2],points_control[3],3*y*(1-t),y*t)
        return byA_Point(x = A._x+B._x, y = A._y+B._y)

    def courbe_bezier_3(self, points_control,N):
        if len(points_control) != 4:
            raise SystemExit("4 points de controle")
        dt = 1.0/N
        t = dt
        points_courbe = [points_control[0]]
        while t < 1.0:
            points_courbe.append(self.point_bezier_3(points_control,t))
            t += dt
        points_courbe.append(points_control[3])
        return points_courbe

if __name__ == '__main__':

    pt1 = byA_Point(x=0,y=0,name="1")
    pt2 = byA_Point(x=5,y=10,name="2")
    pt3 = byA_Point(x=25,y=10,name="3")
    pt4 = byA_Point(x=15,y=30,name="4")
    cb = byA_CubicBezier(P1=pt1,P2=pt2,C1=pt3,C2=pt4)
    print cb.toStr()
