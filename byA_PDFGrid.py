# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 10:16:29 2017

@author: orhanda
"""
import math
import copy
import svgwrite  
from svgpathtools import parse_path, Line
from byA_FrozenClass import byA_FrozenClass
from byA_Path import byA_Path
from byA_Point import byA_Point
from byA_Line import byA_Line

CMPX = 1.0
PXCM = 1.0/35.43307

class byA_PDFGrid(byA_FrozenClass):
    def __init__(self,**kwargs):
        super(byA_PDFGrid, self).__init__(self)
        self._onePDFSize = kwargs.get('PDFSize', None)
        if (self._onePDFSize is None):
            onePDFWidth = kwargs.get('PDFWidth', 21)
            onePDFHeight = kwargs.get('PDFHeight', 29.7)
            self._onePDFSize = [onePDFWidth, onePDFHeight]
            
        w = self._onePDFSize[0]
        h = self._onePDFSize[1]
        
        paths = list()
        rectpath = ("M0,0v{}v{}h{}h{}v{}v{}h{}z"
         "".format(0.5*h, 0.5*h, 0.5*w, 0.5*w, 
                   -0.5*h, -0.5*h, -0.5*w))
        paths.append(rectpath)
        for id,x in enumerate([1,1.1]):
            tickpath = ("M0,{}l{},{}M0,{}l{},{}M{},0l{},{}M{},{}0l{},{}"
                        "".format(x, x, -x, h-x, x, x, w-x, x, x, w-x, h, x, -x))
            paths.append(tickpath)
        parsedPath = parse_path(paths[0]+paths[1]+paths[2])
        self._onePDFSheetPath = byA_Path()
        for p in parsedPath:
            assert(isinstance(p, Line))
            p1 = byA_Point(c=p.start) 
            p2 = byA_Point(c=p.end) 
            self._onePDFSheetPath.append(byA_Line(P1=p1,P2=p2))
        self._allPDFSheetPaths = None
        self._freeze("byA_PDFGrid")
        
    def replicate(self, width, height):
        pdfHeight = self._onePDFSize[1]
        pdfWidth = self._onePDFSize[0]
        self._allPDFSheetPaths = list();
        for y in range(0,int(math.ceil(PXCM*height/pdfHeight))):
            for x in range(0,int(math.ceil(PXCM*width/pdfWidth))):
                self._allPDFSheetPaths.append([copy.deepcopy(self._onePDFSheetPath), "sheet_" + str(x) + "_" + str(y), "translate("+str(x*CMPX*pdfWidth)+","+str(y*CMPX*pdfHeight)+")"])
        
if __name__ == '__main__':
    
    width = int(2000)
    height = int(1200)

    test = byA_PDFGrid()
    test.replicate(width=width, height=height)
    print test._allPDFSheetPaths
    
    print "width = ", width, " x height = ", height
    svgFile = svgwrite.Drawing("test.svg", profile='full', size = (str(width)+'cm', str(height)+'cm'))
    svgFile.viewbox(width=str(width), height=str(height))

    for x in test._allPDFSheetPaths:
        path = svgFile.path(d=x[0].toStr(), id=x[1], fill = 'none')
        path.translate(x[2][0], x[2][1])
        svgFile.add(path)
        svgFile.save()


    