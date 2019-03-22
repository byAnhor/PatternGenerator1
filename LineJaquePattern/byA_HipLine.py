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

class byA_HipLine(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent', None)
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        self._middleBackPoint = byA_Point(x=HORIZONTAL_MARGIN_MM, y=self._sheetSize[1]-VERTICAL_MARGIN_MM) 
        self._middleFrontPoint = byA_Point(x=self._sheetSize[0]-HORIZONTAL_MARGIN_MM, y=self._sheetSize[1]-VERTICAL_MARGIN_MM)
        self._horizontalLine = byA_Line(P1=self._middleBackPoint, P2=self._middleFrontPoint)
        self._nomenclature = "Ligne de hanches"
        if (self._parent is not None):
           self._parent._dicoPoints['HipLine_middleBackPoint'] = self._middleBackPoint 
           self._parent._dicoPoints['HipLine_middleFrontPoint'] = self._middleFrontPoint 
        self._freeze("byA_HipLine")

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
        nomenclature = drawing.text(self._nomenclature, id="nomenclatureHipLine"+self._stature, insert=(self._middleBackPoint._x, self._middleBackPoint._y))
        svggroup.add(nomenclature)
        drawing.save()
        textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id=nomenclatureHipLine"+self._stature, "--query-width", self._filename]))
        nomenclature.translate((self._horizontalLine.lenght()-textw)/2, 0)
        nomenclature.attribs['class'] = 'nomenclature'

if __name__ == '__main__':
    
    w = str(a0Size[0]).replace("cm","")
    h = str(a0Size[1]).replace("cm","")
    filename = "test_HipLine.svg"
    svgDrawing = svgwrite.Drawing(filename, [str(int(w))+'cm',str(int(h))+'cm'], profile='full')
    svgDrawing.viewbox(width=str(int(w)), height=str(int(h)))
    groupHipLine = svgwrite.container.Group(id="groupHipLine", debug=False)
    svgDrawing.add(groupHipLine)

    myHipLine = byA_HipLine(stature='46', sheetSize=a0Size, filename=filename)
   
    myHipLine.addToGroup(svgDrawing, groupHipLine, id="hipLine", stroke='yellow', stroke_width=3)
    svgDrawing.save()

