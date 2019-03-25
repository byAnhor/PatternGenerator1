"""
Created on Fri Mar 22 11:04:19 2019

@author: byAnhor
"""
import numpy as np
import subprocess
import svgwrite 
from svgpathtools import Line
from byA_SVGUtils.byA_Point import byA_Point
from byA_SVGUtils.byA_Line import byA_Line
from byA_SVGUtils.byA_CubicBezier import byA_CubicBezier
from byA_PatternStep import byA_PatternStep

PXCM = 1.0/35.43307
HORIZONTAL_MARGIN_MM = 50
VERTICAL_MARGIN_MM = 50
a0Size = np.array((841,1189))

class byA_FrontSideCurve(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)
        
        waistToHip = self._parent._dicoConstruction['FrontSideLine_waistToHip']
        pFromBefore = self._parent._dicoConstruction['FrontDartWaistLine_dart1']
        pThroughBefore = self._parent._dicoConstruction['FrontSideLine_1cm']
        pTo = self._parent._dicoConstruction['FrontHipLineMark_mark']
        assert isinstance(pFromBefore, byA_Point)
        assert isinstance(pTo, byA_Point)
        assert isinstance(pThroughBefore, byA_Point)
        pFromRot = byA_Point(c=pFromBefore)
        pFromRot.rotate(-90, complex(pTo._x, pTo._y))
        pThroughRot = byA_Point(c=pThroughBefore)
        pThroughRot.rotate(-90, complex(pTo._x, pTo._y))
        pToCoeffA,pToCoeffB = byA_Line(P1=pTo, P2=pThroughRot).equationLine()
        t = 1.0-(80.0/waistToHip.lenght())
        p1Py = pTo._y
        p2Py = (pThroughRot._y - pTo._y*(1-t)**3 - 3*p1Py*t*(1-t)**2 - pFromRot._y*t**3) / (3*t**2*(1-t))
        p2Px = (p2Py-pToCoeffB)/pToCoeffA
        p1Px = (pThroughRot._x - pTo._x*(1-t)**3 - 3*p2Px*t**2*(1-t) - pFromRot._x*t**3) / (3*t*(1-t)**2)
        bezierRot = byA_CubicBezier(P1 = pTo, C1 = byA_Point(x=p1Px,y=p1Py), C2 = byA_Point(x=p2Px,y=p2Py), P2 = pFromRot)
        self._waistToHipCurve = bezierRot.rotated(90, complex(pTo._x, pTo._y))

        self._finalCurve.append(('_waistToHipCurve',self._waistToHipCurve, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_FrontSideCurve")

     def toRI(self):
        """Point as a complex
        """
        return self._waistToHipCurve.toRI() 

     def addToGroup(self, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        oldid = extra.pop("id")
        extra['id'] = oldid+'WaistToHipCurve'+self._stature
        svggroup.add(self._waistToHipCurve.toSVGWrite(drawing, **extra))

if __name__ == '__main__':
    None
    