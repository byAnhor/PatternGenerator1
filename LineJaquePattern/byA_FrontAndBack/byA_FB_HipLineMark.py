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

class byA_FB_HipLineMark(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)
        self._freeze("byA_FB_HipLineMark")

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """        
        super(byA_FB_HipLineMark, self).addToGroup(drawing, svggroup, **extra)

class byA_FrontHipLineMark(byA_FB_HipLineMark):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_HipLineMark.__init__(self,**kwargs)

        bassin = (self._parent._dicoMesures['Bassin'+self._stature] + 40) / 2.0
        # a comparer avec ce qui a deja ete calcule dans byA_FrontBustLineMark + byA_BackBustLineMark
        bustP1 = self._parent._dicoConstruction['BustLine_middleFrontPoint']
        bustP2 = self._parent._dicoConstruction['FrontBustLineMark_mark']
        bustCompare = byA_Line(P1=bustP1,P2=bustP2).lenght()
        bustP3 = self._parent._dicoConstruction['BustLine_middleBackPoint']
        bustP4 = self._parent._dicoConstruction['BackBustLineMark_mark']
        bustCompare += byA_Line(P1=bustP3,P2=bustP4).lenght()
        tmpMark = self._parent._dicoConstruction['FrontBustLineMark_markDownToHipLine']
        self._mark = byA_Point(x=tmpMark._x-(bassin - bustCompare)/2.0, y=tmpMark._y) 

        self._constructionPoint.append(('_mark',self._mark, 'Mf'))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_FrontHipLineMark")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_FrontHipLineMark, self).addToGroup("Front", drawing, svggroup, **extra)

class byA_BackHipLineMark(byA_FB_HipLineMark):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_HipLineMark.__init__(self,**kwargs)

        bassin = (self._parent._dicoMesures['Bassin'+self._stature] + 40) / 2.0
        # a comparer avec ce qui a deja ete calcule dans byA_FrontBustLineMark + byA_BackBustLineMark
        bustP1 = self._parent._dicoConstruction['BustLine_middleFrontPoint']
        bustP2 = self._parent._dicoConstruction['FrontBustLineMark_mark']
        bustCompare = byA_Line(P1=bustP1,P2=bustP2).lenght()
        bustP3 = self._parent._dicoConstruction['BustLine_middleBackPoint']
        bustP4 = self._parent._dicoConstruction['BackBustLineMark_mark']
        bustCompare += byA_Line(P1=bustP3,P2=bustP4).lenght()
        tmpMark = self._parent._dicoConstruction['BackBustLineMark_markDownToHipLine']
        self._mark = byA_Point(x=tmpMark._x+(bassin - bustCompare)/2.0, y=tmpMark._y) 

        self._constructionPoint.append(('_mark',self._mark, 'Mb'))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_BackHipLineMark")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_BackHipLineMark, self).addToGroup("Back", drawing, svggroup, **extra)
        
if __name__ == '__main__':
    None
    


