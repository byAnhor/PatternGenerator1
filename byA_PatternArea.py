# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 15:18:06 2017

@author: orhanda
"""
import svgwrite  
from svgwrite import cm, mm
from svgpathtools import CubicBezier
from svgpathtools import Path
from svgpathtools import Line
from svgpathtools import parse_path
from byA_FrozenClass import byA_FrozenClass

PXCM = 1.0/35.43307

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class byA_PatternArea(byA_FrozenClass):
    def __init__(self, id, **extra):
        self._subAreas = list()
        self._data = dict()
        self._id = id
        self._g = svgwrite.container.Group(id=id, **extra)
        self._g['class'] = "nofill"
        self._inkscapeQuery = None
        self._freeze("byA_PatternArea")
        
    def get_id(self):
        return self._g.get_id()
    def set_id(self, val):
        self._g["id"] = val
        
    def add(self, something):
        if (isinstance(something, svgwrite.shapes.Circle) or
            isinstance(something, svgwrite.shapes.Line) or
            isinstance(something, svgwrite.text.Text) or
            isinstance(something, svgwrite.path.Path)):
            self._g.add(something)
        else:
            self._subAreas.append(something)
            self._g.add(something._g)
        return self
        
    def add_subarea(self, subareaId):
        subarea = byA_PatternArea(self._g.get_id()+subareaId)
        self.add(subarea)
        return subarea
        
    def get_subarea_by_ids(self, pieceId, elargId=None):
        for pieceArea in self._subAreas:
            if pieceId in pieceArea._g.get_id():
                if elargId is None: return pieceArea
                for elargArea in pieceArea._subAreas:
                    if elargId in elargArea._g.get_id():
                        return elargArea
        return None

    def add_circle(self, x, y, r, **extra):
        svgcircle = svgwrite.shapes.Circle(center=(x*PXCM*cm, y*PXCM*cm), r=str(r*PXCM)+'cm', **extra)
        self.add(svgcircle)
        
    def add_text(self, text, x, y, **extra):
        svgtext = svgwrite.text.Text(text, insert=(x*PXCM*cm, y*PXCM*cm), **extra)
        self.add(svgtext)

    def add_line(self, x1, y1, x2, y2, **extra):
        svgline = svgwrite.shapes.Line(start = (x1*PXCM*cm, y1*PXCM*cm), end = (x2*PXCM*cm, y2*PXCM*cm), **extra)
        self.add(svgline)

    def add_path(self, d, **extra):
        svgpath = svgwrite.path.Path(d = d, **extra)
        self.add(svgpath)
        
    def rotate(self, angle, center):
        self._g.rotate(angle, center)

    def translate(self, tx, ty):
        self._g.translate(tx, ty)

    def scale(self, sx, sy):
        self._g.scale(sx, sy)

    def replace_point(self, ptbefore, ptafter):
        pathstr = self._g.elements[0].tostring()
        pathstr = pathstr.split('"')[3]
        pathbefore = parse_path(pathstr)
        pathafter = Path()
        for i in pathbefore:
            if isinstance(i, Line):
                if (isclose(i.start.real, ptbefore._x) and isclose(i.start.imag, ptbefore._y)):
                    i.start = ptafter._x+1j*ptafter._y
                if (isclose(i.end.real, ptbefore._x) and isclose(i.end.imag, ptbefore._y)):
                    i.end = ptafter._x+1j*ptafter._y
            pathafter.append(i)
        self.add(svgwrite.path.Path(d=pathafter.d()))
        
    def getX(self):
        return self._inkscapeQuery["x_"+self.get_id()]
    def getY(self):
        return self._inkscapeQuery["y_"+self.get_id()]
    def getW(self):
        return self._inkscapeQuery["width_"+self.get_id()]
    def getH(self):
        return self._inkscapeQuery["height_"+self.get_id()]
        
        
if __name__ == '__main__':
    
    test1 = byA_PatternArea(id = 'test1')
    print test1
    test2 = byA_PatternArea(id = 'test2')
    print test2
    test1.add(test2)
    print test1
    

