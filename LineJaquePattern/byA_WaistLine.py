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

class byA_WaistLine(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)

        tableVal = self._parent._dicoMesures['Hauteurdubassin'+self._stature]
        p1 = self._parent._dicoConstruction['HipLine_middleBackPoint']
        p2 = self._parent._dicoConstruction['HipLine_middleFrontPoint']
        self._middleBackPoint = byA_Point(x=p1._x, y=p1._y-tableVal) 
        self._middleFrontPoint = byA_Point(x=p2._x, y=p2._y-tableVal) 
        self._horizontalLine = byA_Line(P1=self._middleBackPoint, P2=self._middleFrontPoint)

        self._constructionPoint.append(('_middleBackPoint',self._middleBackPoint , ''))
        self._constructionPoint.append(('_middleFrontPoint',self._middleFrontPoint, ''))
        self._constructionLine.append(('_horizontalLine',self._horizontalLine, 'Ligne de taille'))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze("byA_WaistLine")

     def addToGroup(self, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        oldid = extra.get("id")
        super(byA_WaistLine, self).addToGroup(drawing, svggroup, **extra)
        for elem in svggroup.elements:
            if (elem.get_id() == oldid + '_horizontalLine' + '_Nomenclature'):
                textw = self._query[elem.get_id()]
                elem.translate((self._horizontalLine.lenght()-textw)/2, 0)

if __name__ == '__main__':
    None
