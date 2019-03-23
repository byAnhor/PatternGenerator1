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

class byA_FB_BodiceLenghtLine(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent')
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        self._freeze("byA_FB_BodiceLenghtLine")

     def toRI(self):
        """Point as a complex
        """
        return self._horizontalLine.toRI()

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        id = extra.pop("id")
        extra['id'] = id+self._stature
        svggroup.add(self._horizontalLine.toSVGWrite(drawing, **extra))
        nomenclatureId = "nomenclatureBodiceLenghtLine"+frontorback+self._stature
        nomenclature = drawing.text(self._nomenclature, id=nomenclatureId, insert=(self._middlePoint._x, self._middlePoint._y))
        svggroup.add(nomenclature)
        drawing.save()
        textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id="+nomenclatureId, "--query-width", self._filename]))
        nomenclature.translate((self._horizontalLine.lenght()-textw)/2, 0)
        nomenclature.attribs['class'] = 'nomenclature'

class byA_FrontBodiceLenghtLine(byA_FB_BodiceLenghtLine):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_BodiceLenghtLine.__init__(self,**kwargs)

        p1 = self._parent._dicoPoints['WaistLine_middleFrontPoint']
        self._middlePoint = byA_Point(x=p1._x, y=p1._y-self._parent._dicoMesures['Longueurcorsagedevant'+self._stature]) 
        p2 = byA_Point(x=self._middlePoint._x-200, y=self._middlePoint._y)
        self._horizontalLine = byA_Line(P1=self._middlePoint, P2=p2)
        
        self._nomenclature = ""
        if (self._parent is not None):
           self._parent._dicoPoints['FrontBodiceLenghtLine_middleFrontPoint'] = self._middlePoint 
        self._freeze("byA_FrontBodiceLenghtLine")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_FrontBodiceLenghtLine, self).addToGroup("Front", drawing, svggroup, **extra)

class byA_BackBodiceLenghtLine(byA_FB_BodiceLenghtLine):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_BodiceLenghtLine.__init__(self,**kwargs)

        p1 = self._parent._dicoPoints['WaistLine_middleBackPoint']
        self._middlePoint = byA_Point(x=p1._x, y=p1._y-self._parent._dicoMesures['Longueurmilieudos'+self._stature]) 
        p2 = byA_Point(x=self._middlePoint._x+200, y=self._middlePoint._y)
        self._horizontalLine = byA_Line(P1=self._middlePoint, P2=p2)

        self._nomenclature = ""
        if (self._parent is not None):
           self._parent._dicoPoints['BackBodiceLenghtLine_middleBackPoint'] = self._middlePoint 
        self._freeze("byA_BackBodiceLenghtLine")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_BackBodiceLenghtLine, self).addToGroup("Back", drawing, svggroup, **extra)

if __name__ == '__main__':
    None
