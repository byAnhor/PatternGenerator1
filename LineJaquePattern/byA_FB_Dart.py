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

class byA_FB_Dart(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)
        self._freeze("byA_FB_Dart")

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        super(byA_FB_Dart, self).addToGroup(drawing, svggroup, **extra)

class byA_FrontDart(byA_FB_Dart):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_Dart.__init__(self,**kwargs)

        p1 = self._parent._dicoConstruction['FrontDartBustLine_mark']
        p2 = self._parent._dicoConstruction['FrontDartWaistLine_dart2']
        p3 = self._parent._dicoConstruction['FrontDartWaistLine_dart3']

        self._upMiddleLine = byA_Line(P1=p1, P2=p2)
        self._upSideLine = byA_Line(P1=p1, P2=p3)
        self._downMiddleCurve = byA_CubicBezier(P1=p1, C1=p1, C2=p1, P2=p1)
        self._downSideCurve = byA_CubicBezier(P1=p1, C1=p1, C2=p1, P2=p1)

        self._constructionLine.append(('_upMiddleLine',self._upMiddleLine, ''))
        self._constructionLine.append(('_upSideLine',self._upSideLine, ''))
        self._constructionCurve.append(('_downMiddleCurve',self._downMiddleCurve, ''))
        self._constructionCurve.append(('_downSideCurve',self._downSideCurve, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_FrontDart")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_FrontDart, self).addToGroup("Front", drawing, svggroup, **extra)

class byA_BackDart(byA_FB_Dart):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_Dart.__init__(self,**kwargs)

        p1 = self._parent._dicoConstruction['BackDartBustLine_mark']
        p2 = self._parent._dicoConstruction['BackDartWaistLine_dart2']
        p3 = self._parent._dicoConstruction['BackDartWaistLine_dart3']
        p4 = self._parent._dicoConstruction['BackDartBustLine_markDownToHipLine']
        p4bis = byA_Point(c=p4+complex(0,-25))

        self._upMiddleLine = byA_Line(P1=p1, P2=p2)
        self._upSideLine = byA_Line(P1=p1, P2=p3)
        self._downMiddleLine =  byA_Line(P1=p4bis, P2=p2)
        self._downSideLine = byA_Line(P1=p4bis, P2=p3)

        self._constructionLine.append(('_upMiddleLine',self._upMiddleLine, ''))
        self._constructionLine.append(('_upSideLine',self._upSideLine, ''))
        self._constructionLine.append(('_downMiddleLine',self._downMiddleLine, ''))
        self._constructionLine.append(('_downSideLine',self._downSideLine, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_BackDart")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_BackDart, self).addToGroup("Back", drawing, svggroup, **extra)

if __name__ == '__main__':
    None
