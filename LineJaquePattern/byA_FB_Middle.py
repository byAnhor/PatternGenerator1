"""
Created on Fri Mar 22 11:04:19 2019

@author: byAnhor
"""
import numpy as np
import subprocess
import svgwrite 
from svgpathtools import Line
from byA_SVGUtils.byA_FrozenClass import byA_FrozenClass
from byA_SVGUtils.byA_Point import byA_Point
from byA_SVGUtils.byA_Line import byA_Line

PXCM = 1.0/35.43307
HORIZONTAL_MARGIN_MM = 50
VERTICAL_MARGIN_MM = 50
a0Size = np.array((841,1189))

class byA_FB_Middle(byA_FrozenClass):
    
     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent')
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        self._freeze("byA_FB_Middle")

     def toRI(self):
        """Point as a complex
        """
        return self._verticalLine.toRI()
        
     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """        
        id = extra.pop("id")
        extra['id'] = id+self._stature
        svggroup.add(self._verticalLine.toSVGWrite(drawing, **extra))
        nomenclatureId = "nomenclatureMiddle"+frontorback+self._stature
        nomenclature = drawing.text(self._nomenclature, id=nomenclatureId, insert=(self._hipsPoint._x, self._hipsPoint._y))
        svggroup.add(nomenclature)
        drawing.save()
        textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id="+nomenclatureId, "--query-width", self._filename]))
        nomenclature.translate(0, (self._verticalLine.lenght()+textw)/2)
        nomenclature.rotate(-90 if frontorback=="Front" else 90, (self._hipsPoint._x, self._hipsPoint._y))
        nomenclature.attribs['class'] = 'nomenclature'
        
class byA_MiddleFront(byA_FB_Middle):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_Middle.__init__(self,**kwargs)
        self._hipsPoint = byA_Point(x=self._sheetSize[0]-HORIZONTAL_MARGIN_MM, y=VERTICAL_MARGIN_MM) 
        self._topPoint = byA_Point(x=self._sheetSize[0]-HORIZONTAL_MARGIN_MM, y=self._sheetSize[1]-VERTICAL_MARGIN_MM)
        self._verticalLine = byA_Line(P1=self._hipsPoint, P2=self._topPoint)
        self._nomenclature = "Milieu devant"
        if (self._parent is not None):
           self._parent._dicoPoints['MiddleFront_hipsPoint'] = self._hipsPoint 
           self._parent._dicoPoints['MiddleFront_topPoint'] = self._topPoint 
        self._freeze("byA_MiddleFront")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_MiddleFront, self).addToGroup("Front", drawing, svggroup, **extra)

class byA_MiddleBack(byA_FB_Middle):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_Middle.__init__(self,**kwargs)
        self._hipsPoint = byA_Point(x=HORIZONTAL_MARGIN_MM, y=VERTICAL_MARGIN_MM) 
        self._topPoint = byA_Point(x=HORIZONTAL_MARGIN_MM, y=self._sheetSize[1]-VERTICAL_MARGIN_MM)
        self._verticalLine = byA_Line(P1=self._hipsPoint, P2=self._topPoint)
        self._nomenclature = "Milieu dos"
        if (self._parent is not None):
           self._parent._dicoPoints['MiddleBack_hipsPoint'] = self._hipsPoint 
           self._parent._dicoPoints['MiddleBack_topPoint'] = self._topPoint 
        self._freeze("byA_MiddleBack")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_MiddleBack, self).addToGroup("Back", drawing, svggroup, **extra)

if __name__ == '__main__':
    None
