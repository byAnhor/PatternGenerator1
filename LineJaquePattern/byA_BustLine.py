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

class byA_BustLine(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent', None)
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        p1 = self._parent._dicoPoints['WaistLine_middleBackPoint']
        p2 = self._parent._dicoPoints['WaistLine_middleFrontPoint']
        self._middleBackPoint = byA_Point(x=p1._x, y=p1._y-20-self._parent._dicoMesures['Hauteurdusousbras'+self._stature]) 
        self._middleFrontPoint = byA_Point(x=p2._x, y=p2._y-20-self._parent._dicoMesures['Hauteurdusousbras'+self._stature]) 
        self._horizontalLine = byA_Line(P1=self._middleBackPoint, P2=self._middleFrontPoint)
        self._nomenclature = "Ligne de poitrine"
        if (self._parent is not None):
           self._parent._dicoPoints['BustLine_middleBackPoint'] = self._middleBackPoint 
           self._parent._dicoPoints['BustLine_middleFrontPoint'] = self._middleFrontPoint 
        self._freeze("byA_BustLine")

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
        nomenclature = drawing.text(self._nomenclature, id="nomenclatureBustLine"+self._stature, insert=(self._middleBackPoint._x, self._middleBackPoint._y))
        svggroup.add(nomenclature)
        drawing.save()
        textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id=nomenclatureBustLine"+self._stature, "--query-width", self._filename]))
        nomenclature.translate((self._horizontalLine.lenght()-textw)/2, 0)
        nomenclature.attribs['class'] = 'nomenclature'

if __name__ == '__main__':
    
    w = str(a0Size[0]).replace("cm","")
    h = str(a0Size[1]).replace("cm","")
    filename = "test_BustLine.svg"
    svgDrawing = svgwrite.Drawing(filename, [str(int(w))+'cm',str(int(h))+'cm'], profile='full')
    svgDrawing.viewbox(width=str(int(w)), height=str(int(h)))
    groupBustLine = svgwrite.container.Group(id="groupBustLine", debug=False)
    svgDrawing.add(groupBustLine)

    myBustLine = byA_BustLine(stature='46', sheetSize=a0Size, filename=filename)
   
    myBustLine.addToGroup(svgDrawing, groupBustLine, id="BustLine", stroke='yellow', stroke_width=3)
    svgDrawing.save()

