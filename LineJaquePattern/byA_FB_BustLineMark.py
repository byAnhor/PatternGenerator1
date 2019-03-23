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

class byA_FB_BustLineMark(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent', None)
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        self._freeze("byA_FB_BustLineMark")

     def toRI(self):
        """Point as a complex
        """
        return self._mark.toRI()

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """        
        id = extra.pop("id")
        extra['id'] = id+self._stature
        svggroup.add(self._mark.toSVGWrite(drawing, **extra))
        id = extra.pop("id")
        extra['id'] = id+"ToHipLine"+self._stature
        svggroup.add(self._verticalToHipLine.toSVGWrite(drawing, **extra))

        nomenclatureId = "nomenclatureBustLineMark"+frontorback+self._stature
        nomenclature = drawing.text(self._nomenclature, id=nomenclatureId, insert=(self._mark._x, self._mark._y))
        svggroup.add(nomenclature)
        drawing.save()
        textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id="+nomenclatureId, "--query-width", self._filename]))
        nomenclature.translate(textw/2,textw/2)
        nomenclature.attribs['class'] = 'nomenclature'
  

class byA_FrontBustLineMark(byA_FB_BustLineMark):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_BustLineMark.__init__(self,**kwargs)

        p1 = self._parent._dicoPoints['BustLine_middleFrontPoint']
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
        p2 = self._parent._dicoPoints['HipLine_middleFrontPoint'] 
        downToHipLine = byA_Point(x=p1._x-delta, y=p2._y)
        self._verticalToHipLine = byA_Line(P1=self._mark, P2=downToHipLine)
        self._nomenclature = "A"
        if (self._parent is not None):
           self._parent._dicoPoints['FrontBustLineMark_mark'] = self._mark
           self._parent._dicoPoints['FrontHipLineMark_tmpMark'] = downToHipLine 
        self._freeze("byA_FrontBustLineMark")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_FrontBustLineMark, self).addToGroup("Front", drawing, svggroup, **extra)


class byA_BackBustLineMark(byA_FB_BustLineMark):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FB_BustLineMark.__init__(self,**kwargs)

        p1 = self._parent._dicoPoints['BustLine_middleBackPoint']
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
        p2 = self._parent._dicoPoints['HipLine_middleBackPoint'] 
        downToHipLine = byA_Point(x=p1._x+delta, y=p2._y)
        self._verticalToHipLine = byA_Line(P1=self._mark, P2=downToHipLine)
        self._nomenclature = "B"
        if (self._parent is not None):
           self._parent._dicoPoints['BackBustLineMark_mark'] = self._mark 
           self._parent._dicoPoints['BackHipLineMark_tmpMark'] = downToHipLine 
        self._freeze("byA_BackBustLineMark")

     def addToGroup(self, drawing, svggroup, **extra):
         super(byA_BackBustLineMark, self).addToGroup("Back", drawing, svggroup, **extra)

if __name__ == '__main__':
    None

