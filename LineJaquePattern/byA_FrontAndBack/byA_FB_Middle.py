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

class byA_FB_Middle(byA_PatternStep):
    
     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)
        self._freeze(self.__class__.__name__+"_Parent")

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """        
        super(byA_FB_Middle, self).addToGroup(drawing, svggroup, **extra)
        
class byA_MiddleFront(byA_FB_Middle):

     def __init__(self,**kwargs):
        """Constructor
        """
        self.__class__.__bases__[0].__init__(self,**kwargs)
        
        self._hipsPoint = byA_Point(x=self._sheetSize[0]-HORIZONTAL_MARGIN_MM, y=VERTICAL_MARGIN_MM) 
        self._topPoint = byA_Point(x=self._sheetSize[0]-HORIZONTAL_MARGIN_MM, y=self._sheetSize[1]-VERTICAL_MARGIN_MM)
        self._verticalLine = byA_Line(P1=self._hipsPoint, P2=self._topPoint)
        
        self._constructionPoint.append(('_hipsPoint',self._hipsPoint, 'O'))
        self._constructionPoint.append(('_topPoint',self._topPoint, ''))
        self._finalLine.append(('_verticalLine',self._verticalLine, 'Milieu devant'))
        
        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze(self.__class__.__name__)

     def addToGroup(self, drawing, svggroup, **extra):
         oldid = extra.get("id")
         super(self.__class__, self).addToGroup("Front", drawing, svggroup, **extra)
         for elem in svggroup.elements:
            if (elem.get_id() == oldid + self._stature + '_verticalLine' + '_Nomenclature'):
                 textw = self._query[elem.get_id()]
                 elem.translate(0, (self._verticalLine.lenght()+textw)/2)
                 elem.rotate(-90, (self._hipsPoint._x, self._hipsPoint._y))

class byA_MiddleBack(byA_FB_Middle):

     def __init__(self,**kwargs):
        """Constructor
        """
        self.__class__.__bases__[0].__init__(self,**kwargs)
        
        self._hipsPoint = byA_Point(x=HORIZONTAL_MARGIN_MM, y=VERTICAL_MARGIN_MM) 
        self._topPoint = byA_Point(x=HORIZONTAL_MARGIN_MM, y=self._sheetSize[1]-VERTICAL_MARGIN_MM)
        self._verticalLine = byA_Line(P1=self._hipsPoint, P2=self._topPoint)
        
        self._constructionPoint.append(('_hipsPoint',self._hipsPoint, 'O'))
        self._constructionPoint.append(('_topPoint',self._topPoint, ''))
        self._finalLine.append(('_verticalLine',self._verticalLine, 'Milieu dos'))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze(self.__class__.__name__)

     def addToGroup(self, drawing, svggroup, **extra):
         oldid = extra.get("id")
         super(self.__class__, self).addToGroup("Back", drawing, svggroup, **extra)
         for elem in svggroup.elements:
            if (elem.get_id() == oldid + self._stature + '_verticalLine' + '_Nomenclature'):
                 textw = self._query[elem.get_id()]
                 elem.translate(0, (self._verticalLine.lenght()-textw)/2)
                 elem.rotate(90, (self._hipsPoint._x, self._hipsPoint._y))

if __name__ == '__main__':
    None
