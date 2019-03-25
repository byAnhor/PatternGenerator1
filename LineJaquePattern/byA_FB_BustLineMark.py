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

class byA_FB_BustLineMark(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)
        self._freeze("byA_FB_BustLineMark")

     def toRI(self):
        """Point as a complex
        """
        return self._mark.toRI()

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """        
        super(byA_FB_BustLineMark, self).addToGroup(drawing, svggroup, **extra)
  
class byA_FrontBustLineMark(byA_FB_BustLineMark):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_BustLineMark.__init__(self,**kwargs)

        p1 = self._parent._dicoConstruction['BustLine_middleFrontPoint']
        delta = (self._parent._dicoMesures['Poitrine'+self._stature] + 80) / 4.0
        if (self._parent._dicoMesures['Poitrine'+self._stature] > 1250):
            delta = delta + 30
        elif (self._parent._dicoMesures['Poitrine'+self._stature] > 110): 
            delta = delta + 25
        elif (self._parent._dicoMesures['Poitrine'+self._stature] > 95): 
            delta = delta + 20
        else:
            delta = delta + 15
        self._mark = byA_Point(x=p1._x-delta, y=p1._y) 
        p2 = self._parent._dicoConstruction['HipLine_middleFrontPoint'] 
        self._markDownToHipLine = byA_Point(x=p1._x-delta, y=p2._y)
        self._verticalToHipLine = byA_Line(P1=self._mark, P2=self._markDownToHipLine)

        self._constructionPoint.append(('_mark',self._mark, ''))
        self._constructionPoint.append(('_markDownToHipLine',self._markDownToHipLine, ''))
        self._constructionLine.append(('_verticalToHipLine',self._verticalToHipLine, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_FrontBustLineMark")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_FrontBustLineMark, self).addToGroup("Front", drawing, svggroup, **extra)


class byA_BackBustLineMark(byA_FB_BustLineMark):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_BustLineMark.__init__(self,**kwargs)

        p1 = self._parent._dicoConstruction['BustLine_middleBackPoint']
        delta = (self._parent._dicoMesures['Poitrine'+self._stature] + 80) / 4.0
        if (self._parent._dicoMesures['Poitrine'+self._stature] > 1250):
            delta = delta - 30
        elif (self._parent._dicoMesures['Poitrine'+self._stature] > 110): 
            delta = delta - 25
        elif (self._parent._dicoMesures['Poitrine'+self._stature] > 95): 
            delta = delta - 20
        else:
            delta = delta - 15
        self._mark = byA_Point(x=p1._x+delta, y=p1._y) 
        p2 = self._parent._dicoConstruction['HipLine_middleBackPoint'] 
        self._markDownToHipLine = byA_Point(x=p1._x+delta, y=p2._y)
        self._verticalToHipLine = byA_Line(P1=self._mark, P2=self._markDownToHipLine)

        self._constructionPoint.append(('_mark',self._mark, ''))
        self._constructionPoint.append(('_markDownToHipLine',self._markDownToHipLine, ''))
        self._constructionLine.append(('_verticalToHipLine',self._verticalToHipLine, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_BackBustLineMark")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_BackBustLineMark, self).addToGroup("Back", drawing, svggroup, **extra)

if __name__ == '__main__':
    None

