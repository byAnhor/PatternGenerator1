# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 15:18:06 2017

@author: orhanda
"""
import svgwrite  
from byA_FrozenClass import byA_FrozenClass
from byA_PatternArea import byA_PatternArea

PXCM = 1.0/35.43307

class byA_SVGFile(byA_FrozenClass):
    def __init__(self, filename, size, **extra):
        byA_FrozenClass.__init__(self)
        strokes = extra.pop("strokes")
        self._svg_drawing = svgwrite.Drawing(filename, size, **extra)
        self._svg_size = size
        w = str(self._svg_size[0]).replace("cm","")
        h = str(self._svg_size[1]).replace("cm","")
        self._svg_drawing.viewbox(width=str(w), height=str(h))
        self._freeze("byA_SVGFile")

        svgStyle = svgwrite.container.Style()
        svgStyle['id'] = "patternStyles"
        svgStyle.append(' .pointCaption {fill: black; font-size:' + str(5*PXCM) + ';}')
        svgStyle.append(' line.base {stroke-width:' + str(3*PXCM) + '; opacity:0.1}')
        svgStyle.append(' path.base {stroke-width:' + str(3*PXCM) + '; opacity:0.1}')
        svgStyle.append(' line.bodice {stroke-width:' + str(3*PXCM) + '}')
        svgStyle.append(' path.bodice {stroke-width:' + str(3*PXCM) + '}')
        svgStyle.append(' line.abdomen {stroke-width:' + str(4.5*PXCM) + '; opacity:0.1; stroke-dasharray:' + str(0.15) +','+ str(0.05) + '}')
        svgStyle.append(' path.abdomen {stroke-width:' + str(4.5*PXCM) + '; opacity:0.1; stroke-dasharray:' + str(0.15) +','+ str(0.05) + '}')
        svgStyle.append(' line.coat {stroke-width:' + str(6*PXCM) + ';}')
        svgStyle.append(' path.coat {stroke-width:' + str(6*PXCM) + ';}')
        svgStyle.append(' line.sleeve {stroke-width:' + str(3*PXCM) + ';}')
        svgStyle.append(' path.sleeve {stroke-width:' + str(3*PXCM) + ';}')
        
        for sizeFigure, sizeTxt in enumerate(('thin', 'normal', 'bold')):
            svgStyle.append(' line.' + sizeTxt + "{stroke-width : " + str((sizeFigure+1)*PXCM) + "; stroke-dasharray:" + str(0.05) +','+ str(0.05) + '}')
            svgStyle.append(' path.' + sizeTxt + "{stroke-width : " + str((sizeFigure+1)*PXCM) + "; stroke-dasharray:" + str(0.05) +','+ str(0.05) + '}')
        for s in strokes:
            svgStyle.append(' line.' + str(s) + "{stroke : " + str(s) + ";}")
            svgStyle.append(' path.' + str(s) + "{stroke : " + str(s) + ";}")
        svgStyle.append(' path.onePdfSheet {stroke:orange; stroke-width:0.02;}')            
        self._svg_drawing.add(svgStyle)
        
    def add(self, group):
        assert isinstance(group, byA_PatternArea) 
        self._svg_drawing.add(group._g)
        return self
        
    def save(self):
        self._svg_drawing.save()

if __name__ == '__main__':
    
    test1 = byA_SVGFile(filename = "test.svg", size = (str(10)+'cm', str(10)+'cm'), profile='full', strokes=['black', 'red', 'blue', 'green', 'cyan', 'orange', 'pink', 'purple', 'darkblue', 'olive', 'magenta'])
    

