"""
Created on Fri Mar 22 11:04:19 2019

@author: byAnhor
"""
import numpy as np
import subprocess
import svgwrite 
from svgpathtools import Line
from byA_FrozenClass import byA_FrozenClass
from byA_Point import byA_Point
from byA_Line import byA_Line

PXCM = 1.0/35.43307
HORIZONTAL_MARGIN_MM = 50
VERTICAL_MARGIN_MM = 50
a0Size = np.array((841,1189))

class byA_FrontHipLineMark(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent', None)
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        bassin = (self._parent._dicoMesures['Bassin'+self._stature] + 40) / 2.0
        # a comparer avec ce qui a deja ete calcule dans byA_FrontBustLineMark + byA_BackBustLineMark
        bustP1 = self._parent._dicoPoints['BustLine_middleFrontPoint']
        bustP2 = self._parent._dicoPoints['FrontBustLineMark_mark']
        bustCompare = byA_Line(P1=bustP1,P2=bustP2).lenght()
        bustP3 = self._parent._dicoPoints['BustLine_middleBackPoint']
        bustP4 = self._parent._dicoPoints['BackBustLineMark_mark']
        bustCompare += byA_Line(P1=bustP3,P2=bustP4).lenght()
        tmpMark = self._parent._dicoPoints['FrontHipLineMark_tmpMark']
        self._mark = byA_Point(x=tmpMark._x-(bassin - bustCompare)/2.0, y=tmpMark._y) 
        self._nomenclature = "C'"
        if (self._parent is not None):
           self._parent._dicoPoints['FrontHipLineMark_mark'] = self._mark
        self._freeze("byA_FrontHipLineMark")

     def toRI(self):
        """Point as a complex
        """
        return self._mark.toRI()

     def addToGroup(self, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        id = extra.pop("id")
        extra['id'] = id+self._stature
        svggroup.add(self._mark.toSVGWrite(drawing, **extra))
        nomenclature = drawing.text(self._nomenclature, id="nomenclatureFrontHipLineMark"+self._stature, insert=(self._mark._x, self._mark._y))
        svggroup.add(nomenclature)
        drawing.save()
        textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id=nomenclatureFrontHipLineMark"+self._stature, "--query-width", self._filename]))
        nomenclature.translate(textw/2,textw/2)
        nomenclature.attribs['class'] = 'nomenclature'

if __name__ == '__main__':
    None
    


