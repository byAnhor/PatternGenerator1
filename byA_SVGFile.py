# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 15:18:06 2017

@author: orhanda
"""
import svgwrite  
import subprocess
from byA_FrozenClass import byA_FrozenClass
from byA_PatternArea import byA_PatternArea

PXCM = 1.0/35.43307

class byA_SVGFile(byA_FrozenClass):
    def __init__(self, filename, size, **extra):
        byA_FrozenClass.__init__(self)
        strokes = extra.pop("strokes")
        self._svg_size = size
        w = str(self._svg_size[0]).replace("cm","")
        h = str(self._svg_size[1]).replace("cm","")
        self._svg_drawing = svgwrite.Drawing(filename, [str(10*w)+'cm',str(10*h)+'cm'], **extra)
        self._svg_drawing.viewbox(width=str(10*w), height=str(10*h))
        self._areas = list()
        self._freeze("byA_SVGFile")

        svgStyle = svgwrite.container.Style()
        svgStyle['id'] = "patternStyles"
        svgStyle.append(' .nofill {fill:none;}')
        svgStyle.append(' .pointCaption {fill: black; font-family: Verdana; font-size:' + str(5*PXCM) + ';}')
        svgStyle.append(' .pointCircle {fill: green;}')
        svgStyle.append(' line.base {stroke-width:' + str(1*PXCM) + '; opacity:0.1}')
        svgStyle.append(' path.base {stroke-width:' + str(1*PXCM) + '; opacity:0.1; stroke_linejoin:round}')
        svgStyle.append(' line.bodiceadjust {stroke-width:' + str(1*PXCM) + '; stroke_linejoin:round}')
        svgStyle.append(' path.bodiceadjust {stroke-width:' + str(1*PXCM) + '; stroke_linejoin:round}')
        svgStyle.append(' line.elarg {stroke-width:' + str(1*PXCM) + '; stroke_linejoin:round}')
        svgStyle.append(' path.elarg {stroke-width:' + str(1*PXCM) + '; stroke_linejoin:round}')
        svgStyle.append(' line.abdomen {stroke-width:' + str(4.5*PXCM) + '; opacity:0.1; stroke-dasharray:' + str(0.15) +','+ str(0.05) + '}')
        svgStyle.append(' path.abdomen {stroke-width:' + str(4.5*PXCM) + '; opacity:0.1; stroke-dasharray:' + str(0.15) +','+ str(0.05) + '}')
        svgStyle.append(' line.coat {stroke-width:' + str(6*PXCM) + ';}')
        svgStyle.append(' path.coat {stroke-width:' + str(6*PXCM) + ';}')
        
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
        self._areas.append(group)
        self._svg_drawing.add(group._g)
        return self
        
    def save(self):
        self._svg_drawing.save()

    def query(self, area):
        res = dict()
        for q in ["x","y","width","height"]:
            res[q+"_"+area.get_id()]=float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                                       "--query-id="+area.get_id(),
                                       "--query-"+q,
                                       self._svg_drawing.filename]))
        area._inkscapeQuery = res
        return res
        
    def resizepagetocontent(self):
        None
        #subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
        #                         "-z --verb=FitCanvasToSelectionOrDrawing --verb=FileSave "+self._svg_drawing.filename])

if __name__ == '__main__':
    
    test1 = byA_SVGFile(filename = "test.svg", size = (str(10)+'cm', str(10)+'cm'), profile='full', strokes=['black', 'red', 'blue', 'green', 'cyan', 'orange', 'pink', 'purple', 'darkblue', 'olive', 'magenta'])
    

