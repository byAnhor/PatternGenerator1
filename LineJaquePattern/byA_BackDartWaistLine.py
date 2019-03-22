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

class byA_BackDartWaistLine(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent', None)
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        
        taille = (self._parent._dicoMesures['Ceinture'+self._stature] + 30) / 2.0
        # a comparer avec ce qui a deja ete calcule dans byA_FrontDartBustLine + byA_BackDartBustLine
        bustP1 = self._parent._dicoPoints['BustLine_middleFrontPoint']
        bustP2 = self._parent._dicoPoints['FrontBustLineMark_mark']
        bustCompare = byA_Line(P1=bustP1,P2=bustP2).lenght()
        bustP3 = self._parent._dicoPoints['BustLine_middleBackPoint']
        bustP4 = self._parent._dicoPoints['BackBustLineMark_mark']
        bustCompare += byA_Line(P1=bustP3,P2=bustP4).lenght()
        ppMark = self._parent._dicoPoints['BackDartBustLineMark_mark']
        bMark = self._parent._dicoPoints['BackBustLineMark_mark']
        waistMark = self._parent._dicoPoints['WaistLine_middleBackPoint']
        self._dart1 = byA_Point(x=bMark._x+((taille - bustCompare)/4.0-5), y=waistMark._y)
        self._dart2 = byA_Point(x=ppMark._x-0.5*((taille - bustCompare)/4.0+5), y=waistMark._y)
        self._dart3 = byA_Point(x=ppMark._x+0.5*((taille - bustCompare)/4.0+5), y=waistMark._y)
        if (self._parent is not None):
           self._parent._dicoPoints['BackDartWaistLineMark_dart1'] = self._dart1
           self._parent._dicoPoints['BackDartWaistLineMark_dart2'] = self._dart2
           self._parent._dicoPoints['BackDartWaistLineMark_dart3'] = self._dart3
        self._freeze("byA_BackDartWaistLine")

     def toRI(self):
        """Point as a complex
        """
        return self._dart1.toRI(),self._dart2.toRI(),self._dart3.toRI(), 

     def addToGroup(self, drawing, svggroup, **extra):
        """add a line to a SVG group
        """     
        oldid = extra.pop("id")
        extra['id'] = oldid+'Dart1'+self._stature
        svggroup.add(self._dart1.toSVGWrite(drawing, **extra))
        extra.pop("id")
        extra['id'] = oldid+'Dart2'+self._stature
        svggroup.add(self._dart2.toSVGWrite(drawing, **extra))
        extra.pop("id")
        extra['id'] = oldid+'Dart3'+self._stature
        svggroup.add(self._dart3.toSVGWrite(drawing, **extra))

if __name__ == '__main__':
    None
    