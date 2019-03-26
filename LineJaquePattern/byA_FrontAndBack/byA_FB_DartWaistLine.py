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
from byA_PatternStep import byA_PatternStep

PXCM = 1.0/35.43307
HORIZONTAL_MARGIN_MM = 50
VERTICAL_MARGIN_MM = 50
a0Size = np.array((841,1189))

class byA_FB_DartWaistLine(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)
        self._freeze("byA_FB_DartWaistLine")

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """        
        super(byA_FB_DartWaistLine, self).addToGroup(drawing, svggroup, **extra)

class byA_FrontDartWaistLine(byA_FB_DartWaistLine):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_DartWaistLine.__init__(self,**kwargs)

        taille = (self._parent._dicoMesures['Ceinture'+self._stature] + 30) / 2.0
        # a comparer avec ce qui a deja ete calcule dans byA_FrontDartBustLine + byA_BackDartBustLine
        bustP1 = self._parent._dicoConstruction['BustLine_middleFrontPoint']
        bustP2 = self._parent._dicoConstruction['FrontBustLineMark_mark']
        bustCompare = byA_Line(P1=bustP1,P2=bustP2).lenght()
        bustP3 = self._parent._dicoConstruction['BustLine_middleBackPoint']
        bustP4 = self._parent._dicoConstruction['BackBustLineMark_mark']
        bustCompare += byA_Line(P1=bustP3,P2=bustP4).lenght()
        ppMark = self._parent._dicoConstruction['FrontDartBustLine_mark']
        aMark = self._parent._dicoConstruction['FrontBustLineMark_mark']
        waistMark = self._parent._dicoConstruction['WaistLine_middleFrontPoint']
        self._dart1 = byA_Point(x=aMark._x-((taille - bustCompare)/4.0-5), y=waistMark._y)
        self._dart2 = byA_Point(x=ppMark._x-0.5*((taille - bustCompare)/4.0+5), y=waistMark._y)
        self._dart3 = byA_Point(x=ppMark._x+0.5*((taille - bustCompare)/4.0+5), y=waistMark._y)

        self._constructionPoint.append(('_dart1',self._dart1, 'd1'))
        self._constructionPoint.append(('_dart2',self._dart2, 'd2'))
        self._constructionPoint.append(('_dart3',self._dart3, 'd3'))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_FrontDartWaistLine")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_FrontDartWaistLine, self).addToGroup("Front", drawing, svggroup, **extra)

class byA_BackDartWaistLine(byA_FB_DartWaistLine):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_DartWaistLine.__init__(self,**kwargs)
        
        taille = (self._parent._dicoMesures['Ceinture'+self._stature] + 30) / 2.0
        # a comparer avec ce qui a deja ete calcule dans byA_FrontDartBustLine + byA_BackDartBustLine
        bustP1 = self._parent._dicoConstruction['BustLine_middleFrontPoint']
        bustP2 = self._parent._dicoConstruction['FrontBustLineMark_mark']
        bustCompare = byA_Line(P1=bustP1,P2=bustP2).lenght()
        bustP3 = self._parent._dicoConstruction['BustLine_middleBackPoint']
        bustP4 = self._parent._dicoConstruction['BackBustLineMark_mark']
        bustCompare += byA_Line(P1=bustP3,P2=bustP4).lenght()
        ppMark = self._parent._dicoConstruction['BackDartBustLine_mark']
        bMark = self._parent._dicoConstruction['BackBustLineMark_mark']
        waistMark = self._parent._dicoConstruction['WaistLine_middleBackPoint']
        self._dart1 = byA_Point(x=bMark._x+((taille - bustCompare)/4.0-5), y=waistMark._y)
        self._dart2 = byA_Point(x=ppMark._x-0.5*((taille - bustCompare)/4.0+5), y=waistMark._y)
        self._dart3 = byA_Point(x=ppMark._x+0.5*((taille - bustCompare)/4.0+5), y=waistMark._y)

        self._constructionPoint.append(('_dart1',self._dart1, 'd1'))
        self._constructionPoint.append(('_dart2',self._dart2, 'd2'))
        self._constructionPoint.append(('_dart3',self._dart3, 'd3'))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_BackDartWaistLine")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_BackDartWaistLine, self).addToGroup("Back", drawing, svggroup, **extra)

if __name__ == '__main__':
    None
    