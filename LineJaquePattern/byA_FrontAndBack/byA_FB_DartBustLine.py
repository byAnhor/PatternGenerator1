"""
Created on Fri Mar 22 11:04:19 2019

@author: byAnhor
"""
import numpy as np
from byA_SVGUtils.byA_Point import byA_Point
from byA_SVGUtils.byA_Line import byA_Line
from byA_PatternStep import byA_PatternStep

PXCM = 1.0/35.43307
HORIZONTAL_MARGIN_MM = 50
VERTICAL_MARGIN_MM = 50
a0Size = np.array((841,1189))

class byA_FB_DartBustLine(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)
        self._freeze(self.__class__.__name__+"_Parent")

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """        
        super(byA_FB_DartBustLine, self).addToGroup(drawing, svggroup, **extra)

class byA_FrontDartBustLine(byA_FB_DartBustLine):

     def __init__(self,**kwargs):
        """Constructor
        """
        self.__class__.__bases__[0].__init__(self,**kwargs)

        p1 = self._parent._dicoConstruction['BustLine_middleFrontPoint']
        delta = (self._parent._dicoMesures['Ecartementdessaillantsdepoitrine'+self._stature]) / 2.0
        self._mark = byA_Point(x=p1._x-delta, y=p1._y) 
        p2 = self._parent._dicoConstruction['HipLine_middleFrontPoint'] 
        self._markDownToHipLine = byA_Point(x=p1._x-delta, y=p2._y)
        self._verticalToHipLine = byA_Line(P1=self._mark, P2=self._markDownToHipLine)

        self._constructionPoint.append(('_mark',self._mark, 'PP'))
        self._constructionPoint.append(('_markDownToHipLine',self._markDownToHipLine, 'PPh'))
        self._constructionLine.append(('_verticalToHipLine',self._verticalToHipLine, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze(self.__class__.__name__)

     def addToGroup(self, drawing, svggroup, **extra):
         super(self.__class__, self).addToGroup("Front", drawing, svggroup, **extra)

class byA_BackDartBustLine(byA_FB_DartBustLine):

     def __init__(self,**kwargs):
        """Constructor
        """
        self.__class__.__bases__[0].__init__(self,**kwargs)

        p1 = self._parent._dicoConstruction['BustLine_middleBackPoint']
        delta = (self._parent._dicoMesures['Ecartementdessaillantsdepoitrine'+self._stature]) / 2.0 - 5
        self._mark = byA_Point(x=p1._x+delta, y=p1._y) 
        p2 = self._parent._dicoConstruction['HipLine_middleBackPoint'] 
        self._markDownToHipLine = byA_Point(x=p1._x+delta, y=p2._y)
        self._verticalToHipLine = byA_Line(P1=self._mark, P2=self._markDownToHipLine)
        
        self._constructionPoint.append(('_mark',self._mark, 'PP'))
        self._constructionPoint.append(('_markDownToHipLine',self._markDownToHipLine, 'PPh'))
        self._constructionLine.append(('_verticalToHipLine',self._verticalToHipLine, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze(self.__class__.__name__)

     def addToGroup(self, drawing, svggroup, **extra):
         super(self.__class__, self).addToGroup("Back", drawing, svggroup, **extra)

if __name__ == '__main__':
    None
    