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

class byA_FB_BodiceLenghtLine(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)
        self._freeze(self.__class__.__name__+"_Parent")

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        super(byA_FB_BodiceLenghtLine, self).addToGroup(drawing, svggroup, **extra)

class byA_FrontBodiceLenghtLine(byA_FB_BodiceLenghtLine):

     def __init__(self,**kwargs):
        """Constructor
        """
        self.__class__.__bases__[0].__init__(self,**kwargs)

        p1 = self._parent._dicoConstruction['WaistLine_middleFrontPoint']
        self._middlePoint = byA_Point(x=p1._x, y=p1._y-self._parent._dicoMesures['Longueurcorsagedevant'+self._stature]) 
        p2 = byA_Point(x=self._middlePoint._x-200, y=self._middlePoint._y)
        self._horizontalLine = byA_Line(P1=self._middlePoint, P2=p2)
        self._constructionPoint.append(('_middlePoint',self._middlePoint, 'G'))
        self._constructionLine.append(('_horizontalLine',self._horizontalLine, 'coucou'))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze(self.__class__.__name__)

     def addToGroup(self, drawing, svggroup, **extra):
         super(self.__class__, self).addToGroup("Front", drawing, svggroup, **extra)

class byA_BackBodiceLenghtLine(byA_FB_BodiceLenghtLine):

     def __init__(self,**kwargs):
        """Constructor
        """
        self.__class__.__bases__[0].__init__(self,**kwargs)

        p1 = self._parent._dicoConstruction['WaistLine_middleBackPoint']
        self._middlePoint = byA_Point(x=p1._x, y=p1._y-self._parent._dicoMesures['Longueurmilieudos'+self._stature]) 
        p2 = byA_Point(x=self._middlePoint._x+200, y=self._middlePoint._y)
        self._horizontalLine = byA_Line(P1=self._middlePoint, P2=p2)

        self._constructionPoint.append(('_middlePoint',self._middlePoint, 'G'))
        self._constructionLine.append(('_horizontalLine',self._horizontalLine, 'coucou'))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze(self.__class__.__name__)

     def addToGroup(self, drawing, svggroup, **extra):
         super(self.__class__, self).addToGroup("Back", drawing, svggroup, **extra)

if __name__ == '__main__':
    None
