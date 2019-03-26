"""
Created on Fri Mar 22 11:04:19 2019

@author: byAnhor
"""
import numpy as np
import svgwrite
import subprocess
from byA_SVGUtils.byA_FrozenClass import byA_FrozenClass

PXCM = 1.0/35.43307
HORIZONTAL_MARGIN_MM = 50
VERTICAL_MARGIN_MM = 50
a0Size = np.array((841,1189))

class byA_PatternStep(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._parent = kwargs.get('parent', None)
        self._filename = kwargs.get('filename')
        self._stature = kwargs.get('stature', '')
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        w = str(self._sheetSize[0]).replace("cm","")
        h = str(self._sheetSize[1]).replace("cm","")
        self._tmpFilename = "tmp.svg"
        self._tmpSvg = svgwrite.Drawing(self._tmpFilename, [str(int(w))+'cm',str(int(h))+'cm'], profile='full')
        self._tmpSvg.viewbox(width=str(int(w)), height=str(int(h)))
        svgStyle = svgwrite.container.Style()
        svgStyle.append(' text.nomenclature {font-family: cursive;}')
        svgStyle.append(' text.nomenclature {font-size:' + str(200*PXCM) + ';}')
        self._tmpSvg.add(svgStyle)

        self._query = dict()
        
        self._constructionLine = list()
        self._constructionPoint = list()
        self._constructionCurve = list()
        self._finalLine = list()
        self._finalPoint = list()
        self._finalCurve = list()
        
        self._freeze("byA_PatternStep")

     def fillDicoPoints(self, unicId, parent):
        if (parent is not None):
            alldata = self._constructionPoint+self._finalPoint
            alldata += self._constructionLine+self._finalLine
            alldata += self._constructionCurve+self._finalCurve
            for x in alldata:
                parent._dicoConstruction[unicId+x[0]] = x[1] 

     def addToGroup(self, drawing, svggroup, **extra):
        """add a line to a SVG group
        """       
        oldid = extra.pop("id") 
        
        for pt in self._constructionPoint:
            extra['id'] = oldid + pt[0]
            extra['class_'] = 'constructionPoint stature'+self._stature
            svggroup.add(pt[1].toSVGWrite(drawing, **extra))
            if (pt[2] != ''):
                nomenclatureId = extra['id']+"_Nomenclature"
                nomenclature = drawing.text(pt[2], id=nomenclatureId, insert=(pt[1]._x, pt[1]._y))
                nomenclature.attribs['class'] = 'nomenclature'
                svggroup.add(nomenclature)
                self._tmpSvg.add(nomenclature)
                self._tmpSvg.save()
                textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                                                            "--query-id="+nomenclatureId, "--query-width", self._tmpFilename]))
                nomenclature.translate(0, textw)
            extra.pop("id")
                
        for ln in self._constructionLine:
            extra['id'] = oldid + ln[0]
            extra['class_'] = 'constructionLine stature'+self._stature
            svggroup.add(ln[1].toSVGWrite(drawing, **extra))
            if (ln[2] != ''):
                nomenclatureId = extra['id']+"_Nomenclature"
                nomenclature = drawing.text(ln[2], id=nomenclatureId, insert=(ln[1]._from._x, ln[1]._from._y))
                nomenclature.attribs['class'] = 'nomenclature'
                svggroup.add(nomenclature)
                self._tmpSvg.add(nomenclature)
                self._tmpSvg.save()
                textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                                                            "--query-id="+nomenclatureId, "--query-width", self._tmpFilename]))
                self._query[nomenclatureId] = textw
            extra.pop("id")

        for cb in self._constructionCurve:
            extra['id'] = oldid + cb[0]
            extra['class_'] = 'constructionCurve stature'+self._stature
            svggroup.add(cb[1].toSVGWrite(drawing, **extra))
            extra.pop("id")

        for pt in self._finalPoint:
            extra['id'] = oldid + pt[0]
            extra['class_'] = 'finalPoint stature'+self._stature
            svggroup.add(pt[1].toSVGWrite(drawing, **extra))
            if (pt[2] != ''):
                nomenclatureId = extra['id']+"_Nomenclature"
                nomenclature = drawing.text(pt[2], id=nomenclatureId, insert=(pt[1]._x, pt[1]._y))
                nomenclature.attribs['class'] = 'nomenclature'
                svggroup.add(nomenclature)
                self._tmpSvg.add(nomenclature)
                self._tmpSvg.save()
                textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                                                            "--query-id="+nomenclatureId, "--query-width", self._tmpFilename]))
                nomenclature.translate(0, textw)
            extra.pop("id")
            
        for ln in self._finalLine:
            extra['id'] = oldid + ln[0]
            extra['class_'] = 'finalLine stature'+self._stature
            svggroup.add(ln[1].toSVGWrite(drawing, **extra))
            if (ln[2] != ''):
                nomenclatureId = extra['id']+"_Nomenclature"
                nomenclature = drawing.text(ln[2], id=nomenclatureId, insert=(ln[1]._from._x, ln[1]._from._y))
                nomenclature.attribs['class'] = 'nomenclature'
                svggroup.add(nomenclature)
                self._tmpSvg.add(nomenclature)
                self._tmpSvg.save()
                textw=PXCM * float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                                                            "--query-id="+nomenclatureId, "--query-width", self._tmpFilename]))
                self._query[nomenclatureId] = textw
            extra.pop("id")

        for cb in self._finalCurve:
            extra['id'] = oldid + cb[0]
            extra['class_'] = 'finalCurve stature'+self._stature
            svggroup.add(cb[1].toSVGWrite(drawing, **extra))
            extra.pop("id")

if __name__ == '__main__':
    None
    