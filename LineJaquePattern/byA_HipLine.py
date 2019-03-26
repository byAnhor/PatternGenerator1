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

class byA_HipLine(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)

        self._middleBackPoint = byA_Point(x=HORIZONTAL_MARGIN_MM, y=self._sheetSize[1]-VERTICAL_MARGIN_MM) 
        self._middleFrontPoint = byA_Point(x=self._sheetSize[0]-HORIZONTAL_MARGIN_MM, y=self._sheetSize[1]-VERTICAL_MARGIN_MM)
        self._horizontalLine = byA_Line(P1=self._middleBackPoint, P2=self._middleFrontPoint)

        self._constructionPoint.append(('_middleBackPoint',self._middleBackPoint, 'Rh'))
        self._constructionPoint.append(('_middleFrontPoint',self._middleFrontPoint, 'Lh'))
        self._constructionLine.append(('_horizontalLine',self._horizontalLine, 'Ligne de hanches'))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_HipLine")

     def addToGroup(self, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        oldid = extra.get("id")
        super(byA_HipLine, self).addToGroup(drawing, svggroup, **extra)
        for elem in svggroup.elements:
            if (elem.get_id() == oldid + '_horizontalLine' + '_Nomenclature'):
                textw = self._query[elem.get_id()]
                elem.translate((self._horizontalLine.lenght()-textw)/2, 0)

if __name__ == '__main__':
    None
