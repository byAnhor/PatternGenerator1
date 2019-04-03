"""
Created on Fri Mar 22 11:04:19 2019

@author: byAnhor
"""
from math import sqrt
import numpy as np
from byA_SVGUtils.byA_Point import byA_Point
from byA_SVGUtils.byA_Line import byA_Line
from byA_SVGUtils.byA_CubicBezier import byA_CubicBezier
from byA_PatternStep import byA_PatternStep

PXCM = 1.0/35.43307
HORIZONTAL_MARGIN_MM = 50
VERTICAL_MARGIN_MM = 50
a0Size = np.array((841,1189))

class byA_FB_Dart(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)
        self._freeze(self.__class__.__name__+"_Parent")

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        super(byA_FB_Dart, self).addToGroup(drawing, svggroup, **extra)

class byA_FrontDart(byA_FB_Dart):

     def __init__(self,**kwargs):
        """Constructor
        """
        self.__class__.__bases__[0].__init__(self,**kwargs)

        p1 = self._parent._dicoConstruction['FrontDartBustLine_mark']
        p2 = self._parent._dicoConstruction['FrontDartWaistLine_dart2']
        p3 = self._parent._dicoConstruction['FrontDartWaistLine_dart3']
        p4 = self._parent._dicoConstruction['FrontDartBustLine_markDownToHipLine']
        
        self._upMiddleLine = byA_Line(P1=p1, P2=p2)
        p1CoeffA,p1CoeffB = self._upMiddleLine.equationLine()
        val15mm = 15 # A ajuster (+ pour les plus grandes tailles) : plus un soutien gorge est pointu, moins cette valeur est importante
        self._down15mm = byA_Point(c=(p1.toRI() + val15mm * complex(1,p1CoeffA) / (sqrt(1+p1CoeffA**2))))
        
        self._upSideLine = byA_Line(P1=self._down15mm, P2=p3)
        self._downMiddleLine = byA_Line(P1=p4, P2=p3)
        self._downSideLine = byA_Line(P1=p4, P2=p2)

        downMiddleLineLenght = self._downMiddleLine.lenght()
        downMiddleLineX = abs(self._downMiddleLine._to._x - self._downMiddleLine._from._x)
        downMiddleLineY = abs(self._downMiddleLine._to._y - self._downMiddleLine._from._y)

        print "downMiddleLineX ", downMiddleLineX
        val8cm = 80 * downMiddleLineX / 14.375; #  14.375 is the downMiddleLineX for size 38
        
        self._8cmMiddle = byA_Point(x=p3._x+(downMiddleLineX*val8cm/downMiddleLineLenght),y=p3._y+(downMiddleLineY*val8cm/downMiddleLineLenght))
        self._6mmMiddle = byA_Point(x=self._8cmMiddle._x+6,y=self._8cmMiddle._y)

        pFromBefore = p3
        pThroughBefore = self._6mmMiddle
        pTo = p4
        assert isinstance(pFromBefore, byA_Point)
        assert isinstance(pTo, byA_Point)
        assert isinstance(pThroughBefore, byA_Point)
        pFromRot = byA_Point(c=pFromBefore)
        pFromRot.rotate(90, complex(pTo._x, pTo._y))
        pThroughRot = byA_Point(c=pThroughBefore)
        pThroughRot.rotate(90, complex(pTo._x, pTo._y))
        pToCoeffA,pToCoeffB = byA_Line(P1=pTo, P2=pThroughRot).equationLine()
        t = 1.0-(80.0/downMiddleLineLenght)
        for x in range(1,10):
            t = x/10.0
            p1Py = pTo._y
            p2Py = (pThroughRot._y - pTo._y*(1-t)**3 - 3*p1Py*t*(1-t)**2 - pFromRot._y*t**3) / (3*t**2*(1-t))
            p2Px = (p2Py-pToCoeffB)/pToCoeffA
            p1Px = (pThroughRot._x - pTo._x*(1-t)**3 - 3*p2Px*t**2*(1-t) - pFromRot._x*t**3) / (3*t*(1-t)**2)
            bezierRot = byA_CubicBezier(P1 = pTo, C1 = byA_Point(x=p1Px,y=p1Py), C2 = byA_Point(x=p2Px,y=p2Py), P2 = pFromRot)
            self._downSideCurve = bezierRot#.rotated(-90, complex(pTo._x, pTo._y))
            self._constructionPoint.append(('C1',byA_Point(x=p1Px,y=p1Py), 'C1'+str(x)))
            self._constructionPoint.append(('C2',byA_Point(x=p2Px,y=p2Py), 'C2'+str(x)))
            self._finalCurve.append(('_downSideCurve',self._downSideCurve, ''))
        self._finalCurve.append(('_downSideCurve',self._downSideCurve, ''))
 

        self._downMiddleCurve = byA_CubicBezier(P1=p1, C1=p1, C2=p1, P2=p1)

        self._finalLine.append(('_upMiddleLine',self._upMiddleLine, ''))
        self._constructionPoint.append(('_down15mm',self._down15mm, 'F'))
        self._finalLine.append(('_upSideLine',self._upSideLine, ''))
        self._constructionLine.append(('_downMiddleLine',self._downMiddleLine, ''))
        self._constructionLine.append(('_downSideLine',self._downSideLine, ''))
        self._finalCurve.append(('_downMiddleCurve',self._downMiddleCurve, ''))
        self._constructionPoint.append(('_8cmMiddle',self._8cmMiddle, '8'))
        self._constructionPoint.append(('_6mmMiddle',self._6mmMiddle, '6'))
        self._constructionPoint.append(('pThroughRot',pThroughRot, 'pThroughRot'))
        self._finalCurve.append(('_downSideCurve',self._downSideCurve, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze(self.__class__.__name__)

     def addToGroup(self, drawing, svggroup, **extra):
         super(self.__class__, self).addToGroup("Front", drawing, svggroup, **extra)

class byA_BackDart(byA_FB_Dart):

     def __init__(self,**kwargs):
        """Constructor
        """
        self.__class__.__bases__[0].__init__(self,**kwargs)

        p1 = self._parent._dicoConstruction['BackDartBustLine_mark']
        p2 = self._parent._dicoConstruction['BackDartWaistLine_dart2']
        p3 = self._parent._dicoConstruction['BackDartWaistLine_dart3']
        p4 = self._parent._dicoConstruction['BackDartBustLine_markDownToHipLine']
        p4bis = byA_Point(c=p4+complex(0,-25))

        self._upMiddleLine = byA_Line(P1=p1, P2=p2)
        self._upSideLine = byA_Line(P1=p1, P2=p3)
        self._downMiddleLine =  byA_Line(P1=p4bis, P2=p2)
        self._downSideLine = byA_Line(P1=p4bis, P2=p3)

        self._finalLine.append(('_upMiddleLine',self._upMiddleLine, ''))
        self._finalLine.append(('_upSideLine',self._upSideLine, ''))
        self._finalLine.append(('_downMiddleLine',self._downMiddleLine, ''))
        self._finalLine.append(('_downSideLine',self._downSideLine, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze(self.__class__.__name__)

     def addToGroup(self, drawing, svggroup, **extra):
         super(self.__class__, self).addToGroup("Back", drawing, svggroup, **extra)

if __name__ == '__main__':
    None
