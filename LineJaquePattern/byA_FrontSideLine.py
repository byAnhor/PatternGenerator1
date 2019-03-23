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

class byA_FrontSideLine(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent', None)
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        
        aMark = self._parent._dicoPoints['FrontBustLineMark_mark']
        waistMark = self._parent._dicoPoints['FrontDartWaistLineMark_dart1']
        hipMark = self._parent._dicoPoints['FrontHipLineMark_mark']

        self._bustToWaist = byA_Line(P1=aMark, P2=waistMark)
        self._waistToHip = byA_Line(P1=waistMark, P2=hipMark)
        waistToHipLenght = self._waistToHip.lenght()
        waistToHipX = abs(self._waistToHip._to._x - self._waistToHip._from._x)
        waistToHipY = abs(self._waistToHip._to._y - self._waistToHip._from._y)
        self._8cm = byA_Point(x=waistMark._x-(waistToHipX*80/waistToHipLenght),y=waistMark._y+(waistToHipY*80/waistToHipLenght))
        self._1cm = byA_Point(x=self._8cm._x-10,y=self._8cm._y)

        if (self._parent is not None):
           self._parent._dicoPoints['FrontSideLine_bustToWaist'] = self._bustToWaist
           self._parent._dicoPoints['FrontSideLine_waistToHip'] = self._waistToHip
           self._parent._dicoPoints['FrontSideLine_8cm'] = self._8cm
           self._parent._dicoPoints['FrontSideLine_1cm'] = self._1cm
        self._freeze("byA_FrontSideLine")

     def toRI(self):
        """Point as a complex
        """
        return self._bustToWaist.toRI(),self._waistToHip.toRI(),self._8cm.toRI(),self._1cm.toRI()

     def addToGroup(self, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        oldid = extra.pop("id")
        extra['id'] = oldid+'BustToWaist'+self._stature
        svggroup.add(self._bustToWaist.toSVGWrite(drawing, **extra))
        extra.pop("id")
        extra['id'] = oldid+'WaistToHip'+self._stature
        svggroup.add(self._waistToHip.toSVGWrite(drawing, **extra))
        extra.pop("id")
        extra['id'] = oldid+'1cm'+self._stature
        svggroup.add(self._1cm.toSVGWrite(drawing, **extra))

if __name__ == '__main__':
    None
    