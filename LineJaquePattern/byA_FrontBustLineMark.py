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

class byA_FrontBustLineMark(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent', None)
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
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
        id = extra.pop("id")
        extra['id'] = id+"ToHipLine"+self._stature
        svggroup.add(self._verticalToHipLine.toSVGWrite(drawing, **extra))
        nomenclature = drawing.text(self._nomenclature, id="nomenclatureFrontBustLineMark", insert=(self._mark._x, self._mark._y))
        svggroup.add(nomenclature)
        drawing.save()
        textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id=nomenclatureFrontBustLineMark", "--query-width", self._filename]))
        nomenclature.translate(textw/2,textw/2)
        nomenclature.attribs['class'] = 'nomenclature'

if __name__ == '__main__':
    
    w = str(a0Size[0]).replace("cm","")
    h = str(a0Size[1]).replace("cm","")
    filename = "test_WaistLine.svg"
    svgDrawing = svgwrite.Drawing(filename, [str(int(w))+'cm',str(int(h))+'cm'], profile='full')
    svgDrawing.viewbox(width=str(int(w)), height=str(int(h)))
    groupWaistLine = svgwrite.container.Group(id="groupWaistLine", debug=False)
    svgDrawing.add(groupWaistLine)

    myWaistLine = byA_FrontBustLineMark(stature='46', sheetSize=a0Size, filename=filename)
   
    myWaistLine.addToGroup(svgDrawing, groupWaistLine, id="WaistLine", stroke='yellow', stroke_width=3)
    svgDrawing.save()

