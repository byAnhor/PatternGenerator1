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

class byA_BackBodiceLenghtLine(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent', None)
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        p1 = self._parent._dicoPoints['WaistLine_middleBackPoint']
        self._middleBackPoint = byA_Point(x=p1._x, y=p1._y-self._parent._dicoMesures['Longueurmilieudos'+self._stature]) 
        p2 = byA_Point(x=self._middleBackPoint._x+200, y=self._middleBackPoint._y)
        self._horizontalLine = byA_Line(P1=self._middleBackPoint, P2=p2)
        self._nomenclature = ""
        if (self._parent is not None):
           self._parent._dicoPoints['BackBodiceLenghtLine_middleBackPoint'] = self._middleBackPoint 
        self._freeze("byA_BackBodiceLenghtLine")

     def toRI(self):
        """Point as a complex
        """
        return self._horizontalLine.toRI()

     def addToGroup(self, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        id = extra.pop("id")
        extra['id'] = id+self._stature
        svggroup.add(self._horizontalLine.toSVGWrite(drawing, **extra))
        nomenclature = drawing.text(self._nomenclature, id="nomenclatureBackBodiceLenghtLine"+self._stature, insert=(self._middleBackPoint._x, self._middleBackPoint._y))
        svggroup.add(nomenclature)
        drawing.save()
        textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id=nomenclatureBackBodiceLenghtLine"+self._stature, "--query-width", self._filename]))
        nomenclature.translate((self._horizontalLine.lenght()-textw)/2, 0)
        nomenclature.attribs['class'] = 'nomenclature'

if __name__ == '__main__':
    None
