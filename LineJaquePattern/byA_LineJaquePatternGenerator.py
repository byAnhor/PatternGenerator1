"""
Created on Fri Mar 22 11:04:19 2019

@author: byAnhor
"""
import numpy as np
import svgwrite 
import csv
from byA_FrozenClass import byA_FrozenClass
from byA_MiddleFront import byA_MiddleFront
from byA_MiddleBack import byA_MiddleBack
from byA_HipLine import byA_HipLine
from byA_WaistLine import byA_WaistLine
from byA_BustLine import byA_BustLine
from byA_BackBustLineMark import byA_BackBustLineMark
from byA_FrontBustLineMark import byA_FrontBustLineMark
from byA_BackHipLineMark import byA_BackHipLineMark
from byA_FrontHipLineMark import byA_FrontHipLineMark
from byA_FrontBodiceLenghtLine import byA_FrontBodiceLenghtLine
from byA_BackBodiceLenghtLine import byA_BackBodiceLenghtLine

class byA_LineJaquePatternGenerator(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._liststatures = kwargs.get('liststatures', '')
        self._currentStature = None
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        self._filename = kwargs.get('filename', 'pattern.svg')
        self._dicoPoints = dict()
        self._dicoMesures = kwargs.get('dicoMesures', a0Size)        
        w = str(self._sheetSize[0]).replace("cm","")
        h = str(self._sheetSize[1]).replace("cm","")
        self._svgDrawing = svgwrite.Drawing(self._filename, [str(int(w))+'cm',str(int(h))+'cm'], profile='full')
        self._svgDrawing.viewbox(width=str(int(w)), height=str(int(h)))
        self._Stature = dict()
        self._MiddleFront = dict()
        self._MiddleBack = dict()
        self._HipLine = dict()
        self._WaistLine = dict()
        self._BustLine = dict()
        self._FrontBustLineMark = dict()
        self._BackBustLineMark = dict()
        self._FrontHipLineMark = dict()
        self._BackHipLineMark = dict()
        self._FrontBodiceLenghtLine = dict()
        self._BackBodiceLenghtLine = dict()
        self._freeze("byA_LineJaquePatternGenerator")

     def set_currentStature(self, stature):
        self._currentStature = stature
        self._Stature[self._currentStature] = svgwrite.container.Group(id="groupStature"+self._currentStature)
        self._svgDrawing.add(self._Stature[self._currentStature])
        self._svgDrawing.save()
         
     def trace_MiddleFront(self):
        self._MiddleFront[self._currentStature] = byA_MiddleFront(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupMiddleFront = svgwrite.container.Group(id="groupMiddleFront"+self._currentStature)
        self._Stature[self._currentStature].add(groupMiddleFront)
        self._MiddleFront[self._currentStature].addToGroup(self._svgDrawing, groupMiddleFront, id="middleFront", stroke='red', stroke_width=3)
        self._svgDrawing.save()
        
     def trace_MiddleBack(self):
        self._MiddleBack[self._currentStature] = byA_MiddleBack(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupMiddleBack = svgwrite.container.Group(id="groupMiddleBack"+self._currentStature, debug=False)
        self._Stature[self._currentStature].add(groupMiddleBack)
        self._MiddleBack[self._currentStature].addToGroup(self._svgDrawing, groupMiddleBack, id="middleBack", stroke='green', stroke_width=3)
        self._svgDrawing.save()

     def trace_HipLine(self):
        self._HipLine[self._currentStature] = byA_HipLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupHipLine = svgwrite.container.Group(id="groupHipLine"+self._currentStature, debug=False)
        self._Stature[self._currentStature].add(groupHipLine)
        self._HipLine[self._currentStature].addToGroup(self._svgDrawing, groupHipLine, id="hipLine", stroke='yellow', stroke_width=3)
        self._svgDrawing.save()

     def trace_WaistLine(self):
        self._WaistLine[self._currentStature] = byA_WaistLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupWaistLine = svgwrite.container.Group(id="groupWaistLine"+self._currentStature, debug=False)
        self._Stature[self._currentStature].add(groupWaistLine)
        self._WaistLine[self._currentStature].addToGroup(self._svgDrawing, groupWaistLine, id="waistLine", stroke='orange', stroke_width=3)
        self._svgDrawing.save()

     def trace_BustLine(self):
        self._BustLine[self._currentStature] = byA_BustLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBustLine = svgwrite.container.Group(id="groupBustLine"+self._currentStature, debug=False)
        self._Stature[self._currentStature].add(groupBustLine)
        self._BustLine[self._currentStature].addToGroup(self._svgDrawing, groupBustLine, id="bustLine", stroke='pink', stroke_width=3)
        self._svgDrawing.save()
        
     def mark_FrontBustLine(self):
        self._FrontBustLineMark[self._currentStature] = byA_FrontBustLineMark(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBustLine = None
        for elem in self._Stature[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupBustLine")):
                groupBustLine = elem
        self._FrontBustLineMark[self._currentStature].addToGroup(self._svgDrawing, groupBustLine, id="frontBustMark", fill='grey', stroke='grey', stroke_width=1)
        self._svgDrawing.save()

     def mark_BackBustLine(self):
        self._BackBustLineMark[self._currentStature] = byA_BackBustLineMark(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBustLine = None
        for elem in self._Stature[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupBustLine")):
                groupBustLine = elem
        self._BackBustLineMark[self._currentStature].addToGroup(self._svgDrawing, groupBustLine, id="backBustMark", fill='grey', stroke='grey', stroke_width=1)
        self._svgDrawing.save()

     def mark_FrontHipLine(self):
        self._FrontHipLineMark[self._currentStature] = byA_FrontHipLineMark(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupHipLine = None
        for elem in self._Stature[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupHipLine")):
                groupHipLine = elem
        self._FrontHipLineMark[self._currentStature].addToGroup(self._svgDrawing, groupHipLine, id="frontHipMark", fill='grey', stroke='grey', stroke_width=1)
        self._svgDrawing.save()

     def mark_BackHipLine(self):
        self._BackHipLineMark[self._currentStature] = byA_BackHipLineMark(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupHipLine = None
        for elem in self._Stature[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupHipLine")):
                groupHipLine = elem
        self._BackHipLineMark[self._currentStature].addToGroup(self._svgDrawing, groupHipLine, id="backHipMark", fill='grey', stroke='grey', stroke_width=1)
        self._svgDrawing.save()

     def trace_FrontBodiceLenght(self):
        self._FrontBodiceLenghtLine[self._currentStature] = byA_FrontBodiceLenghtLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupFrontBodiceLenghtLine = svgwrite.container.Group(id="groupFrontBodiceLenghtLine"+self._currentStature, debug=False)
        self._Stature[self._currentStature].add(groupFrontBodiceLenghtLine)
        self._FrontBodiceLenghtLine[self._currentStature].addToGroup(self._svgDrawing, groupFrontBodiceLenghtLine, id="frontBodiceLenghtLine", fill='grey', stroke='grey', stroke_width='0.5', stroke_dasharray="4,1")
        self._svgDrawing.save()

     def trace_BackBodiceLenght(self):
        self._BackBodiceLenghtLine[self._currentStature] = byA_BackBodiceLenghtLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBackBodiceLenghtLine = svgwrite.container.Group(id="groupBackBodiceLenghtLine"+self._currentStature, debug=False)
        self._Stature[self._currentStature].add(groupBackBodiceLenghtLine)
        self._BackBodiceLenghtLine[self._currentStature].addToGroup(self._svgDrawing, groupBackBodiceLenghtLine, id="backBodiceLenghtLine", fill='grey', stroke='grey', stroke_width='0.5', stroke_dasharray="4,1")
        self._svgDrawing.save()
        
     def trace_AllStatures(self):
        for stature in self._liststatures: 
            print stature
            pattern.set_currentStature(stature)
            pattern.trace_MiddleFront()
            pattern.trace_MiddleBack()
            pattern.trace_HipLine()
            pattern.trace_WaistLine()
            pattern.trace_BustLine()
            pattern.mark_FrontBustLine()
            pattern.mark_BackBustLine()
            pattern.mark_FrontHipLine()
            pattern.mark_BackHipLine()
            pattern.trace_FrontBodiceLenght()
            pattern.trace_BackBodiceLenght()

     def save(self):
         self._svgDrawing.save()

if __name__ == '__main__':
    
    a0Size = np.array((841,1189))
    squarePaperSheet = np.array((1200,1200))
    
    listStatures = list();
    dicoMesures = dict();
    with open('tableaumensurations.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for nbRow,curRow in enumerate(spamreader):
            if (nbRow == 0):
                for x in curRow:
                    listStatures.append(x)
                listStatures = listStatures[1:]
            else:
                for idx,stature in enumerate(listStatures):
                    dicoMesures[curRow[0].replace(" ","")+str(stature)] = float(curRow[idx+1])

    pattern = byA_LineJaquePatternGenerator(dicoMesures=dicoMesures, liststatures=listStatures, sheetSize=a0Size, filename = "test_LineJaquePatternGenerator.svg")
    pattern.trace_AllStatures()
    pattern.save()
    
    print pattern._dicoPoints


import math
from matplotlib.pyplot import *
import copy
from svgwrite import cm, mm
from svgpathtools import svg2paths, Path, Line, QuadraticBezier, CubicBezier, Arc, parse_path
from pyx import *
import subprocess
from PyPDF2 import PdfFileWriter
from PIL import Image
from fpdf import FPDF
from byA_FrozenClass import byA_FrozenClass
from byA_Point import byA_Point
from byA_Line import byA_Line
from byA_Path import byA_Path
from byA_CubicBezier import byA_CubicBezier
from byA_PDFGrid import byA_PDFGrid
from byA_PatternArea import byA_PatternArea
from byA_SVGFile import byA_SVGFile

def makePdf(pdfFileName, listPages, w, h):

    cover = Image.open(str(listPages[0]))
    width, height = cover.size

    pdfA4 = FPDF(orientation = 'P', unit = 'cm', format='A4')
    for n,page in enumerate(listPages):
        print n
        pdfA4.add_page()
        pdfA4.image(name = str(page), x = 0, y = 0, w = w, h = h, type = 'PNG')
    pdfA4.output('tmp.pdf', 'F')

    inFile = PdfFileReader(open('tmp.pdf', "rb"))
    outFile = PdfFileWriter()
    outFile.setPageLayout("/SinglePage")
    for page_number in range(inFile.getNumPages()):
        curPage = inFile.getPage(page_number)
        curPage.mediaBox.upperLeft = (-50,870)
        outFile.addPage(curPage)
    outputStream = file(pdfFileName, "wb")
    outFile.write(outputStream)

PXCM = 1.0/35.43307

# résolution de l'équation du troisième degré par la méthode de Cardan 
 
            

class byA_PatternGenerator(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        
        # According to Become a pattern drafter (Claire Wargnier)
        self._stature = self.inclusive_range(110,6,11)#11)
        self._back_waist_lenght = self.inclusive_range(26.0, 1.5, len(self._stature))
        self._front_waist_lenght = self.inclusive_range(23.6, 1.4, len(self._stature))
        self._bust_measurement = self.inclusive_range(58, 2, len(self._stature))
        self._waist_measurement = self.inclusive_range(53, 1, len(self._stature))
        self._hips_measurement = self.inclusive_range(64, 2, len(self._stature))
        self._neckline_measurement = self.inclusive_range(28.2, 0.7, len(self._stature))
        self._shoulder_lenght = self.inclusive_range(8.7, 0.4, len(self._stature))
        self._crossback_measurement = self.inclusive_range(23, 1, len(self._stature))
        self._crossfront_measurement = self.inclusive_range(22, 1, len(self._stature))
        self._arm_lenght = self.inclusive_range(38, 2, len(self._stature))
        self._arm_circumference = self.inclusive_range(18.0, 0.6, len(self._stature))
        self._shoulder_to_elbow_lenght = self.inclusive_range(22, 1, len(self._stature))
        self._wrist_circumference = [13.5,14,14,14.5,14.5]
        self._waist_to_hips = self.inclusive_range(12, 1, len(self._stature))
        self._riser_measurement = self.inclusive_range(18.8, 0.8, len(self._stature))
        self._waist_to_knee = self.inclusive_range(37, 2, len(self._stature))
        self._knee_circumference = self.inclusive_range(25, 1, len(self._stature))
        self._crotch_measurement = self.inclusive_range(48.4, 3.4, len(self._stature))
        self._waist_to_floor = self.inclusive_range(67.2, 4.2, len(self._stature))
        self._trouser_bottom_width = self.inclusive_range(29.5, 0.5, len(self._stature))
        self._head_length = np.append([19.5], self.inclusive_range(20, 1, len(self._stature)-1))
        self._head_circumference = [53,54,54,55,55]
        self._face_circumference = self.inclusive_range(48, 1, len(self._stature))
        self.display()
        self._svg_file = None
        self._working_area = None 
        self._clean_area = None 
        self._cur_stature_area = None
        self._all_points_area = None
        self._strokes = ['black', 'red', 'blue', 'green', 'cyan', 'orange', 'pink', 'purple', 'darkblue', 'olive', 'magenta']
        self._basic_bodice_enlargement = kwargs.get('basic_bodice_enlargement', False)
        self._points = dict()
        self._freeze("byA_PatternGenerator")

     def inclusive_range(self, start, step, nb):
        res = [start]
        for elem in range(0,nb-1):
            res = np.append(res, [res[-1]+step])
        return res

     def open_svg(self, path, size):
        width = int(size[0])
        height = int(size[1])
        print "width = ", width, " x height = ", height
        self._svg_file = byA_SVGFile(filename=path, size = (str(width)+'cm', str(height)+'cm'), profile='full', strokes=self._strokes)
                
     def save_svg(self):
        self._svg_file.save()
        
     def create_areas(self):
         self._working_area = byA_PatternArea(id="WorkingArea")
         self._svg_file.add(self._working_area)
         self._clean_area = byA_PatternArea(id="CleanArea")
         self._svg_file.add(self._clean_area)
         
     def fill_working_area(self, statureIdx, allPieces, allElarg):
         statureAreaStr = "Stature"+str(statureIdx)
         pattern._cur_stature_area = byA_PatternArea(id=statureAreaStr)
         self._working_area.add(pattern._cur_stature_area)
         for pieceId,piece in enumerate(allPieces):
            pieceArea = byA_PatternArea(id=statureAreaStr+piece)
            pattern._cur_stature_area.add(pieceArea)
            pointsArea = byA_PatternArea(id=statureAreaStr+piece+"Points")
            pieceArea.add(pointsArea)
            for elargId,elarg in enumerate(allElarg):
                elargArea = byA_PatternArea(id=statureAreaStr+piece+elarg)
                pieceArea.add(elargArea)
         
 
     def place_base_points(self):
        # Base, points
        self._points.clear()
        self._points['A'] = byA_Point(x=0, y=0, name="A")
        self._points['Bback'] = byA_Point(x=0, y=-self._back_waist_lenght[curStatureIdx], name = "B") + self._points['A'] 
        self._points['Cfront'] = byA_Point(x=0, y=-(self._front_waist_lenght[curStatureIdx]-1.25), name = "C") + self._points['A'] 
        self._points['Dback'] = byA_Point(x=-0.25*self._bust_measurement[curStatureIdx], y=0, name = "D") + self._points['A'] 
        self._points['E'] = byA_Point(x=0, y=-0.25*(self._back_waist_lenght[curStatureIdx]+self._front_waist_lenght[curStatureIdx]), name = "E") + self._points['Dback'] 
        self._points['F'] = byA_Point(x=self._points['A']._x, y=self._points['E']._y, name="F")
        self._points['G'] = byA_Point(x=0.5*(self._points['F']._x+self._points['Cfront']._x), y=0.5*(self._points['F']._y+self._points['Cfront']._y), name = "G")
        self._points['Hback'] = byA_Point(x=-(0.8+self._neckline_measurement[curStatureIdx]/6), y=0, name = "H") + self._points['Bback']
        self._points['Iback'] = byA_Point(x=0, y=-(0.25*(self._points['Bback']._x-self._points['Hback']._x)), name = "I") + self._points['Hback']
        self._points['Jfront'] = byA_Point(x=self._points['Hback']._x, y=self._points['Cfront']._y, name = "J")
        self._points['Kback'] = byA_Point(x=self._points['Hback']._x, y=self._points['Jfront']._y+(self._points['Iback']._y-self._points['Jfront']._y)/3.0, name = "K")
        #IL**2 = IL**2 + KL**2
        kl = math.sqrt(self._shoulder_lenght[curStatureIdx]**2-(self._points['Iback']._y-self._points['Kback']._y)**2)
        self._points['Lback'] = byA_Point(x=-kl, y=0, name = "L") + self._points['Kback']
        self._points['Mback'] = byA_Point(x=-0.5*self._crossback_measurement[curStatureIdx], y=0, name = "M") + self._points['G']
        self._points['Nfront'] = byA_Point(x=-0.5*self._crossfront_measurement[curStatureIdx], y=0, name = "N") + self._points['G']
        self._points['Ifront'] = byA_Point(x=0, y=0.5, name = "I'") + self._points['Iback']
        self._points['Lfront'] = byA_Point(x=0, y=0.5, name = "L'") + self._points['Lback']
        self._points['Dfront'] = byA_Point(x=0.75, y=0, name = "D'") + self._points['Dback']
        self._points['Afront'] = byA_Point(x=0, y=self._front_waist_lenght[curStatureIdx], name = "A'") + self._points['Cfront']
        self._points['Oback'] = byA_Point(x=0.5*(self._points['A']._x+self._points['Dback']._x), y=0.5*(self._points['A']._y+self._points['Dback']._y), name = "O")
        self._points['Odart'] = byA_Point(x=self._points['Oback']._x, y=self._points['F']._y, name = "O2")
        
        frontarea = self._cur_stature_area.get_subarea_by_ids("Front", "Points")
        backarea = self._cur_stature_area.get_subarea_by_ids("Back", "Points")
        for pointKey, pointValue in self._points.items():
            if "front" not in pointKey:
                self.draw_point(backarea, pointValue)
            elif "back" not in pointKey:
                self.draw_point(frontarea, pointValue)

     def draw_base_curves_front(self):
        area = self._cur_stature_area.get_subarea_by_ids("Front", "Base")

        pattern.compute_front_neckline_base_curve()
        pattern.compute_front_armhole_base_curve()
        pattern.compute_front_waist_base_curve()

        line1 = byA_Line(P1=self._points['A'], P2=self._points['Cfront'])        
        line2 = byA_Line(P1=self._points['Ifront'], P2=self._points['Lfront'])  
        line3 = byA_Line(P1=self._points['E'], P2=self._points['Dfront'])  
        line4 = byA_Line(P1=self._points['Afront'], P2=self._points['A'])  
        paths = byA_Path(line1,area._data["_front_neckline_base_curve"],line2, area._data["_front_armhole_base_curve"],line3, area._data['_front_waist_base_curve'], line4, closed=True)
        area.add_path(paths.toStr(), id = area.get_id() + "Curve", stroke_linejoin = 'round', class_='base '+str(self._strokes[curStatureIdx]))

        self.draw_line(area, self._points['Cfront'], self._points['Jfront'], curStatureIdx, 'thin')
        self.draw_line(area, self._points['Jfront'], self._points['Ifront'], curStatureIdx, 'thin')
        self.draw_line(area, self._points['E'], self._points['F'], curStatureIdx, 'thin')
        self.draw_line(area, self._points['A'], self._points['Dfront'], curStatureIdx, 'thin')
        self.draw_line(area, self._points['G'], self._points['Nfront'], curStatureIdx, 'thin')

     def draw_base_curves_back(self):
        frontarea = self._cur_stature_area.get_subarea_by_ids("Front", "Base")
        area = self._cur_stature_area.get_subarea_by_ids("Back", "Base")

        pattern.compute_back_neckline_base_curve()
        pattern.compute_back_armhole_base_curve()
        
        line1 = byA_Line(P1=self._points['A'], P2=self._points['Bback'])        
        line2 = byA_Line(P1=self._points['Iback'], P2=self._points['Lback'])  
        line3 = byA_Line(P1=self._points['E'], P2=self._points['Dback'])  
        line4 = byA_Line(P1=self._points['Dback'], P2=self._points['A'])  
        paths = byA_Path(line1,area._data["_back_neckline_base_curve"],line2, area._data["_back_armhole_base_curve"],line3, line4, closed=True)
        area.add_path(paths.toStr(), id = area.get_id() + "Curve", stroke_linejoin = 'round', class_='base '+str(self._strokes[curStatureIdx]))
        
        self.draw_line(area, self._points['Bback'], self._points['Hback'], curStatureIdx, 'thin')
        self.draw_line(area, self._points['Hback'], self._points['Iback'], curStatureIdx, 'thin')
        self.draw_line(area, self._points['Kback'], self._points['Lback'], curStatureIdx, 'thin')
        self.draw_line(area, self._points['E'], self._points['F'], curStatureIdx, 'thin')
        self.draw_line(area, self._points['G'], self._points['Mback'], curStatureIdx, 'thin')
        self.draw_line(area, self._points['Oback'], self._points['Odart'], curStatureIdx, 'thin')

        # Base, dart
        ad2lenght = self.get_distance(pattern._points['Dback'], pattern._points['A'])
        pince = 0.5*self._waist_measurement[curStatureIdx] - frontarea._data['_front_waist_base_curve_lenght'] - ad2lenght
        pattern._points['Pback'] = byA_Point(x=-0.5*pince, y=0, name = "P") + pattern._points['Oback']
        pattern._points['Qback'] = byA_Point(x=+0.5*pince, y=0, name = "Q") + pattern._points['Oback']
        pattern.draw_line(area, pattern._points['Odart'], pattern._points['Pback'], curStatureIdx, 'thin')
        pattern.draw_line(area, pattern._points['Odart'], pattern._points['Qback'], curStatureIdx, 'thin')

     def get_equation_line(self, src, dst):
        assert isinstance(src, byA_Point)
        assert isinstance(dst, byA_Point)
        assert not src._x == dst._x
        # y = ax+b
        # src._y = a*src._x + b
        # dst._y = a*dst._x + b
        a = (src._y-dst._y)/(src._x - dst._x)
        return [a, src._y-a*src._x]
        
     def get_distance(self, src, dst):
        assert isinstance(src, byA_Point)
        assert isinstance(dst, byA_Point)
        return math.sqrt((src._y-dst._y)**2+(src._x-dst._x)**2)
        
     def combinaison_lineaire(self, A,B,u,v):
        assert isinstance(A, byA_Point)
        assert isinstance(B, byA_Point)
        return byA_Point(x = A._x*u+B._x*v, y = A._y*u+B._y*v)
    
     def interpolation_lineaire(self, A,B,t):
        return combinaison_lineaire(A,B,t,1-t)

     def point_bezier_3(self, points_control,t):
        x=(1-t)**2
        y=t*t
        A = self.combinaison_lineaire(points_control[0],points_control[1],(1-t)*x,3*t*x)
        B = self.combinaison_lineaire(points_control[2],points_control[3],3*y*(1-t),y*t)
        return byA_Point(x = A._x+B._x, y = A._y+B._y)
    
     def courbe_bezier_3(self, points_control,N):
        if len(points_control) != 4:
            raise SystemExit("4 points de controle")
        dt = 1.0/N
        t = dt
        points_courbe = [points_control[0]]
        while t < 1.0:
            points_courbe.append(self.point_bezier_3(points_control,t))
            t += dt
        points_courbe.append(points_control[3])
        return points_courbe

     def racines(self,abj,n): 
        """calcule les n racines n-ièmes du nombre""" 
        # on utilise les racines de l'unité 
        module = math.sqrt(abj.real*abj.real+abj.imag*abj.imag)
        if abj.real==0 and abj.y==0: 
            argument = 0 
        elif abj.real==0 and abj.y>0: 
            argument = math.pi/2 
        elif abj.real==0 and abj.y<0: 
            argument = -math.pi/2 
        elif abj.real>0: 
            argument = math.atan(abj.imag/abj.real) 
        else:
            argument = math.pi-math.atan(abj.imag/(-abj.real)) 
        return [complex(module**(1.0/n) *math.cos((k*2*math.pi+argument)/n),module**(1.0/n)*math.sin((k*2*math.pi+argument)/n)) for k in range(0,n) ] 
 
     def cardan(self, a,b,c,d): 
        """ a, b, c, d sont les coefficients initiaux de l'équation""" 
        # on commence par mettre sous forme canonique 
        b,c,d=b/a,c/a,d/a 
        p=c-b*b/(3.0+0j) 
        q=d-b*c/(3.0+0j)-(b**3)/(27.0+0j)+(b**3)/(9.0+0j) 
        B,C= q,-p*p*p/(27.0+0j) 
        D=B*B-(4.0+0j)*C 
        R=self.racines(D, 2) 
        U=(-B+R[0])/(2.0+0j) 
        roots=self.racines(U, 3) 
        sol1=[u-p/((3.0+0j)*u) for u in roots] 
        sol2=[z-b/(3.0+0j) for z in sol1] 
        return sol2 
     
     def resolution(self, a,b,c,d): 
        """Résout l'équation az^3+bz^2+c^z+d=0""" 
        # les coefficients peuvent être entiers, réels ou complexes 
        # Dans tous les cas on convertit en complexes pour commencer 
        if isinstance(a,float) or isinstance(a,int): 
            a=float(a)+0j 
        if isinstance(b,float) or isinstance (b,int): 
            b=float(b)+0j 
        if isinstance(c,float) or isinstance(c,int): 
            c=float(c)+0j 
        if isinstance(d,float) or isinstance(d,int): 
            d=float(d)+0j 
        Z = self.cardan(a,b,c,d) 
        P0=a*Z[0]**3+b*(Z[0]**2)+c*Z[0]+d 
        P1=a*Z[1]**3+b*(Z[1]**2)+c*Z[1]+d 
        P2=a*Z[2]**3+b*(Z[2]**2)+c*Z[2]+d 
        return Z
        
     def get_sub_curves(self, P0, P1, P2, P3, t):
        assert isinstance(P0, byA_Point)
        assert isinstance(P1, byA_Point)
        assert isinstance(P2, byA_Point)
        assert isinstance(P3, byA_Point)
        P11t = byA_Point(x=(1-t)*P0._x+t*P1._x,y=(1-t)*P0._y+t*P1._y, name="") 
        P12t = byA_Point(x=(1-t)*P1._x+t*P2._x,y=(1-t)*P1._y+t*P2._y, name="") 
        P13t = byA_Point(x=(1-t)*P2._x+t*P3._x,y=(1-t)*P2._y+t*P3._y, name="")
        P21t = byA_Point(x=(1-t)*P11t._x+t*P12t._x,y=(1-t)*P11t._y+t*P12t._y, name="")
        P22t = byA_Point(x=(1-t)*P12t._x+t*P13t._x,y=(1-t)*P12t._y+t*P13t._y, name="")
        P31t = byA_Point(x=(1-t)*P21t._x+t*P22t._x,y=(1-t)*P21t._y+t*P22t._y, name="")
        return (P0, P11t, P21t, P31t),(P31t, P22t, P13t, P3)            
        
     def get_curve_distance(self, src, P1, P2, dst):
        assert isinstance(src, byA_Point)
        assert isinstance(dst, byA_Point)
        assert isinstance(P1, byA_Point)
        assert isinstance(P2, byA_Point)
        l = self.get_distance(src,dst)
        points = self.courbe_bezier_3([src,P1,P2,dst],l*10)
        res = 0
        for point in range(0, len(points)-1):
            res += self.get_distance(points[point], points[point+1])
        return res
        
     def compute_curve_from_to_through(self, pFrom, pThrough, pTo, t, pFromCoeffA, pFromCoeffB, svgId, svgStroke):
        assert isinstance(pFrom, byA_Point)
        assert isinstance(pTo, byA_Point)
        assert isinstance(pThrough, byA_Point)

        P2y = pTo._y
        P1y = (pThrough._y - pFrom._y*(1-t)**3 - 3*P2y*t**2*(1-t) - pTo._y*t**3) / (3*t*(1-t)**2)
        P1x = (pFrom._x * (1+pFromCoeffA**2) + pFromCoeffA*pFromCoeffB - pFromCoeffA*P1y)
        P2x = (pThrough._x - pFrom._x*(1-t)**3 - 3*P1x*t*(1-t)**2 - pTo._x*t**3) / (3*t**2*(1-t))
        bezier = byA_CubicBezier(P1 = pFrom, C1 = byA_Point(x=P1x,y=P1y), C2 = byA_Point(x=P2x,y=P2y), P2 = pTo)
        dist = self.get_curve_distance(pFrom, byA_Point(x=P1x, y=P1y), byA_Point(x=P2x, y=P2y), pTo)
        return bezier, dist

     def draw_point(self, area, src):
        assert isinstance(src, byA_Point)
        subarea = area.add_subarea("Spot"+src._name)
        subarea.add_circle(src._x, src._y, 0.03, class_='pointCircle')
        subarea.add_text(src._name, src._x+0.03, src._y-0.03, class_='pointCaption')
        src._drawn = True

     def draw_line(self, area, src, dst, svgId, mycls, drawExtrem=False):
        assert isinstance(src, byA_Point)
        assert isinstance(dst, byA_Point)
        area.add_line(src._x, src._y, dst._x, dst._y, id = str(src._name)+str(dst._name)+str(svgId), class_=mycls)
        if drawExtrem:
            if not src._drawn: 
                self.draw_point(area, src)
            if not dst._drawn: 
                self.draw_point(area, dst)

     def compute_front_neckline_base_curve(self):
        g = self._cur_stature_area.get_subarea_by_ids("Front", "Base")
        
        # front
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lback'],pattern._points['Iback'])
        bh = pattern._points['Bback']._x-pattern._points['Hback']._x;
        delta = 0.1*bh

        g._data["_front_neckline_base_curve"] = byA_CubicBezier(P1 = self._points['Cfront'],
                              C1 = byA_Point(x=0.2*self._points['Cfront']._x+0.8*self._points['Jfront']._x,y=self._points['Jfront']._y),
                              C2 = byA_Point(x=self._points['Ifront']._x+delta,y=self._points['Ifront']._y-delta/equaLIa), 
                              P2 = self._points['Ifront'])        

     def compute_back_neckline_base_curve(self):
        g = self._cur_stature_area.get_subarea_by_ids("Back", "Base")

         # back
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lback'],pattern._points['Iback'])
        bh = pattern._points['Bback']._x-pattern._points['Hback']._x;
        delta = 0.02*bh
        
        g._data["_back_neckline_base_curve"] = byA_CubicBezier(P1 = self._points['Bback'],
                              C1 = byA_Point(x=0.1*self._points['Bback']._x+0.9*self._points['Hback']._x,y=self._points['Hback']._y),
                              C2 = byA_Point(x=self._points['Iback']._x+delta,y=self._points['Iback']._y-delta/equaLIa), 
                              P2 = self._points['Iback'])        

     def compute_front_neckline_bodice_adjustement_curve(self):
        g = self._cur_stature_area.get_subarea_by_ids("Front", "BodiceAdjust")

        # front
        self._points['Cbafront'] = byA_Point(x=0, y=0.75, name = "C'") + self._points['Cfront']
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lfront'],pattern._points['Ifront'])
        angle = math.atan(equaLIa)
        # cos(angle) = dx/0.25cm
        # sin(angle) = dy/0.25cm
        dx = 0.25*math.cos(angle)
        dy = 0.25*math.sin(angle)
        self._points['Ibafront'] = byA_Point(x=-dx, y=-dy, name = "") + self._points['Ifront']
        bh = pattern._points['Cbafront']._x-pattern._points['Ibafront']._x;
        delta = 0.1*bh
        g._data["_front_neckline_bodice_adjustement_curve"] = byA_CubicBezier(P1 = self._points['Cbafront'],
                              C1 = byA_Point(x=0.2*self._points['Cbafront']._x+0.8*self._points['Ibafront']._x,y=self._points['Cbafront']._y),
                              C2 = byA_Point(x=self._points['Ibafront']._x+delta,y=self._points['Ibafront']._y-delta/equaLIa), 
                              P2 = self._points['Ibafront'])        
        
     def compute_back_neckline_bodice_adjustement_curve(self):
        g = self._cur_stature_area.get_subarea_by_ids("Back", "BodiceAdjust")

        # back
        self._points['Bbaback'] = byA_Point(x=0, y=0.1, name = "Bb") + self._points['Bback']
        equaLIa,equaLIb = pattern.get_equation_line(self._points['Lback'],self._points['Iback'])
        angle = math.atan(equaLIa)
        # cos(angle) = dx/0.25cm
        # sin(angle) = dy/0.25cm
        dx = 0.25*math.cos(angle)
        dy = 0.25*math.sin(angle)
        self._points['Ibaback'] = byA_Point(x=-dx, y=-dy, name = "Ib") + self._points['Iback']
        bh = pattern._points['Bbaback']._x-pattern._points['Ibaback']._x;
        delta = 0.02*bh
        g._data["_back_neckline_bodice_adjustement_curve"] = byA_CubicBezier(P1 = self._points['Bbaback'],
                              C1 = byA_Point(x=0.2*self._points['Bbaback']._x+0.8*self._points['Ibaback']._x,y=self._points['Bbaback']._y),
                              C2 = byA_Point(x=self._points['Ibaback']._x+delta,y=self._points['Ibaback']._y-delta/equaLIa), 
                              P2 = self._points['Ibaback'])        

     def compute_back_armhole_base_curve(self):
        g = self._cur_stature_area.get_subarea_by_ids("Back", "Base")

         # back
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lback'],pattern._points['Iback'])
        path, dist = self.compute_curve_from_to_through(self._points['Lback'], self._points['Mback'], self._points['E'], 0.5, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        g._data["_back_armhole_base_curve"] = path
        g._data["_back_armhole_base_curve_measurement"] = dist
        
     def compute_front_armhole_base_curve(self):
        g = self._cur_stature_area.get_subarea_by_ids("Front", "Base")

         # front
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lfront'],pattern._points['Ifront'])
        path, dist = self.compute_curve_from_to_through(self._points['Lfront'], self._points['Nfront'], self._points['E'], 0.5, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        g._data["_front_armhole_base_curve"] = path
        g._data["_front_armhole_base_curve_measurement"] = dist

     def compute_front_armhole_bodice_adjustement_curve(self):
        g = self._cur_stature_area.get_subarea_by_ids("Front", "BodiceAdjust")

        # front
        self._points['Nbafront'] = byA_Point(x=-0.75, y=0, name = "Nb") + self._points['Nfront']

        # Underarm side seam adjustement
        self._points['Ebafront'] = byA_Point(x=-1.75, y=1.5, name = "Eb") + self._points['E']

        # armhole curve redesign
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lfront'],pattern._points['Ifront'])
        path, dist = self.compute_curve_from_to_through(self._points['Lbafront'], self._points['Nbafront'], self._points['Ebafront'], 0.5, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        g._data["_front_armhole_bodice_adjustement_curve"] = path
        g._data["_front_armhole_bodice_adjustement_curve_measurement"] = dist

     def compute_back_armhole_bodice_adjustement_curve(self):
        g = self._cur_stature_area.get_subarea_by_ids("Back", "BodiceAdjust")

        # back
        self._points['Mbaback'] = byA_Point(x=-0.75, y=0, name = "Mb") + self._points['Mback']

        # Underarm side seam adjustement
        self._points['Ebaback'] = byA_Point(x=-1.75, y=1.5, name = "Eb") + self._points['E']

        # armhole curve redesign
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lback'],pattern._points['Iback'])
        path, dist = self.compute_curve_from_to_through(self._points['Lbaback'], self._points['Mbaback'], self._points['Ebaback'], 0.5, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        g._data["_back_armhole_bodice_adjustement_curve"] = path
        g._data["_back_armhole_bodice_adjustement_curve_measurement"] = dist

     def compute_front_waist_base_curve(self):
        g = self._cur_stature_area.get_subarea_by_ids("Front", "Base")

        P1 = byA_Point(x=self._points['Dfront']._x+2, y=self._points['Dfront']._y)
        P2 = byA_Point(x=self._points['Afront']._x-5, y=self._points['Afront']._y)

        g._data['_front_waist_base_curve'] = byA_CubicBezier(P1 = pattern._points['Dfront'], C1 = P1, C2 = P2, P2 = pattern._points['Afront'])
        g._data['_front_waist_base_curve_lenght'] = self.get_curve_distance(pattern._points['Dfront'], P1, P2, pattern._points['Afront'])

     def compute_front_waist_bodice_adjustement_curve(self):
        g = self._cur_stature_area.get_subarea_by_ids("Front", "BodiceAdjust")

        # Waist adjustement
        self._points['Dbafront'] = byA_Point(x=-1.5, y=0, name = "D2b") + self._points['Dfront']
        P1 = byA_Point(x=pattern._points['Dbafront']._x+2, y=pattern._points['Dbafront']._y)
        P2 = byA_Point(x=pattern._points['Afront']._x-5, y=pattern._points['Afront']._y)
        
        g._data['_front_waist_bodice_adjustement_curve'] = byA_CubicBezier(P1 = pattern._points['Dbafront'], C1 = P1, C2 = P2, P2 = pattern._points['Afront'])
        g._data['_front_waist_bodice_adjustement_curve_lenght'] = self.get_curve_distance(pattern._points['Dbafront'], P1, P2, pattern._points['Afront'])

     def compute_back_waist_bodice_adjustement_curve(self):
        # Waist adjustement
        self._points['Dbaback'] = byA_Point(x=0-1.5, y=0, name = "Db") + self._points['Dback']

     def compute_front_shoulderline_bodice_adjustement_line(self):
        # Shoulder line adjustement
        equaLIa,equaLIb = pattern.get_equation_line(self._points['Lfront'],self._points['Ifront'])
        angle = math.atan(equaLIa)
        dx = 0.5*math.cos(angle)
        dy = 0.5*math.sin(angle)
        self._points['Lbafront'] = byA_Point(x=-dx, y=-dy, name = "") + self._points['Lfront']

     def compute_back_shoulderline_bodice_adjustement_line(self):
        # Shoulder line adjustement
        equaLIa,equaLIb = pattern.get_equation_line(self._points['Lfront'],self._points['Ifront'])
        angle = math.atan(equaLIa)
        dx = 0.5*math.cos(angle)
        dy = 0.5*math.sin(angle)
        self._points['Lbaback'] = byA_Point(x=-dx, y=-dy, name = "Lb") + self._points['Lback']

     def draw_bodice_adjustement_curves_back(self):
        area = self._cur_stature_area.get_subarea_by_ids("Back", "BodiceAdjust")

        pattern.compute_back_neckline_bodice_adjustement_curve()
        pattern.compute_back_shoulderline_bodice_adjustement_line()
        pattern.compute_back_armhole_bodice_adjustement_curve()
        pattern.compute_back_waist_bodice_adjustement_curve()
        
        line1 = byA_Line(P1=self._points['A'], P2=self._points['Bbaback'])        
        line2 = byA_Line(P1=self._points['Ibaback'], P2=self._points['Lbaback'])  
        line3 = byA_Line(P1=self._points['Ebaback'], P2=self._points['Dbaback'])  
        line4 = byA_Line(P1=self._points['Dbaback'], P2=self._points['A'])  
        paths = byA_Path(line1,area._data["_back_neckline_bodice_adjustement_curve"],line2, area._data["_back_armhole_bodice_adjustement_curve"],line3,line4, closed=True)
        area.add_path(paths.toStr(), id = area.get_id() + "Curve", stroke_linejoin = 'round', class_='bodiceadjust '+str(self._strokes[curStatureIdx]))

        self.draw_line(area, self._points['G'], self._points['Mbaback'], curStatureIdx, 'thin')

        frontpointsarea = self._cur_stature_area.get_subarea_by_ids("Front", "Points")
        backpointsarea = self._cur_stature_area.get_subarea_by_ids("Back", "Points")
        for pointKey, pointValue in self._points.items():
            if "bafront" not in pointKey:
                self.draw_point(backpointsarea, pointValue)
            elif "baback" not in pointKey:
                self.draw_point(frontpointsarea, pointValue)
        
     def draw_bodice_adjustement_curves_front(self):
        area = self._cur_stature_area.get_subarea_by_ids("Front", "BodiceAdjust")

        pattern.compute_front_neckline_bodice_adjustement_curve()
        pattern.compute_front_shoulderline_bodice_adjustement_line()
        pattern.compute_front_armhole_bodice_adjustement_curve()
        pattern.compute_front_waist_bodice_adjustement_curve()
        
        line1 = byA_Line(P1=self._points['A'], P2=self._points['Cbafront'])        
        line2 = byA_Line(P1=self._points['Ibafront'], P2=self._points['Lbafront'])  
        line3 = byA_Line(P1=self._points['Ebafront'], P2=self._points['Dbafront'])  
        line4 = byA_Line(P1=self._points['Afront'], P2=self._points['A'])  
        paths = byA_Path(line1,area._data["_front_neckline_bodice_adjustement_curve"],line2, area._data["_front_armhole_bodice_adjustement_curve"],line3, area._data["_front_waist_bodice_adjustement_curve"], line4, closed=True)
        area.add_path(paths.toStr(), id = area.get_id() + "Curve", stroke_linejoin = 'round', class_='bodiceadjust '+str(self._strokes[curStatureIdx]))

        self.draw_line(area, self._points['A'], self._points['Dbafront'], curStatureIdx, 'thin')
        self.draw_line(area, self._points['G'], self._points['Nbafront'], curStatureIdx, 'thin')

        frontarea = self._cur_stature_area.get_subarea_by_ids("Front", "Points")
        backarea = self._cur_stature_area.get_subarea_by_ids("Back", "Points")
        for pointKey, pointValue in self._points.items():
            if "bafront" not in pointKey:
                self.draw_point(backarea, pointValue)
            elif "baback" not in pointKey:
                self.draw_point(frontarea, pointValue)

     def draw_abdomen_adjustement(self, group, curStatureIdx, thickness):
        equaLIa,equaLIb = pattern.get_equation_line(pattern._pointL2,pattern._pointI2)
        angle = math.atan(equaLIa)
        # cos(angle) = dx/2cm
        # sin(angle) = dy/2cm
        dx = 2*math.cos(angle)
        dy = 2*math.sin(angle)
        #self._pointAAA = byA_Point(x=self._pointL2._x-dx, y=self._pointL2._y-dy-0.5, name = "AAA")
        #self._pointI2AA = byA_Point(x=self._pointI2._x, y=self._pointI2._y-1.5, name = "I2AA")
        #self._pointCAA = byA_Point(x=self._points['C']_x, y=self._points['C']_y-1.5, name = "CAA")
        #self.draw_line(group, self._pointAAA, self._pointI2AA, curStatureIdx, thickness)
        #pathStr = 'M ' + str(self._pointI2AA._x*CMPX) + ',' + str(self._pointI2AA._y*CMPX)
        #bh = pattern._pointB._x-pattern._pointH._x;
        #delta = 0.1*bh
        #pathStr += ' C ' + str((self._pointI2AA._x+delta)*CMPX) + ',' + str((self._pointI2AA._y-delta/equaLIa)*CMPX)
        #pathStr += ' ' +   str((0.2*self._pointCAA._x+0.8*self._pointJ._x)*CMPX) + ',' + str(self._pointCAA._y*CMPX)
        #pathStr += ' ' +   str(self._pointCAA._x*CMPX) + ',' + str(self._pointCAA._y*CMPX) 
        #path = self._svg_file.path(d=(pathStr),
        #                              id = "curve"+str(self._pointI2AA._name)+str(self._pointCAA._name)+str(curStatureIdx), 
        #                              stroke_linejoin = 'round',
        #                              fill = 'none')
        #path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
        #group.add(path)
                   
     def draw_coat_enlargement_back(self, group, curStatureIdx, thickness):
        equaLIa,equaLIb = pattern.get_equation_line(pattern._pointL,pattern._pointI)
        angle = math.atan(equaLIa)
        dx = math.cos(angle)
        dy = math.sin(angle)
        self._pointLCE = byA_Point(x=self._pointL._x-2*dx, y=self._pointL._y-2*dy, name = "Lc")
        self._pointICE = byA_Point(x=self._pointI._x-dx, y=self._pointI._y-dy, name = "Ic")
        self._pointBCE = byA_Point(x=self._pointB._x, y=self._pointB._y+0.5, name = "Bc")
        self.draw_line(group, self._pointLCE, self._pointICE, curStatureIdx, thickness)
        pathStr = 'M ' + str(self._pointICE._x) + ',' + str(self._pointICE._y)
        bh = pattern._pointB._x-pattern._pointH._x
        delta = 0.02*bh
        P0 = byA_Point(x=self._pointICE._x+delta, y=self._pointICE._y-delta/equaLIa)
        P1 = byA_Point(x=0.1*self._pointBCE._x+0.9*self._pointICE._x, y=self._pointBCE._y)
        P2 = self._pointBCE
        self._backNecklinePath = np.array((self._pointICE, P0, P1, P2))
        pathStr += ' C ' + str(P0._x) + ',' + str(P0._y)
        pathStr += ' ' + str(P1._x) + ',' + str(P1._y)
        pathStr += ' ' +   str(P2._x) + ',' + str(P2._y)  
        area.add_path(paths.toStr(), id = area.get_id() + "Curve" +str(self._pointI._name)+str(self._pointB._name)+str(curStatureIdx), stroke_linejoin = 'round', class_='coatenlarg', stroke=str(self._strokes[curStatureIdx]))

        self._pointMCE = byA_Point(x=self._pointM._x-2.5, y=self._pointM._y, name = "ME")
        self._pointECE = byA_Point(x=self._pointE._x-4.75, y=self._pointE._y+4.5, name = "EE")
        self._pointACE = byA_Point(x=self._pointA._x, y=self._pointA._y+2, name = "AE")
        self._pointD2CE = byA_Point(x=self._pointD2._x-4.75, y=self._pointD2._y+2, name = "D2E")
        self.draw_line(group, self._pointECE, self._pointD2CE, curStatureIdx, 'base')
        self.draw_line(group, self._pointD2CE, self._pointACE, curStatureIdx, thickness)
        self.draw_line(group, self._pointBCE, self._pointACE, curStatureIdx, thickness)
        self.draw_line(group, self._pointMCE, self._pointM, curStatureIdx, 'base')
        
        path = self.compute_curve_from_to_through(self._pointLCE, self._pointMCE, self._pointECE, 0.4, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
            
     def draw_coat_enlargement_front(self, group, curStatureIdx, thickness):
        self._pointCCE = byA_Point(x=self._pointCAA._x, y=self._pointCAA._y+2, name = "Cc")
        longueurepauldos = self.get_distance(self._pointICE, self._pointLCE)
        equaLIa,equaLIb = pattern.get_equation_line(pattern._pointAAA,pattern._pointI2AA)
        angle = math.atan(equaLIa)
        dx = math.cos(angle)
        dy = math.sin(angle)
        self._pointI2CE = byA_Point(x=self._pointAAA._x+dx*longueurepauldos, y=self._pointAAA._y+dy*longueurepauldos, name = "I2c")
        self.draw_line(group, self._pointI2CE, self._pointAAA, curStatureIdx, thickness)
        pathStr = 'M ' + str(self._pointI2CE._x) + ',' + str(self._pointI2CE._y)
        bh = pattern._pointB._x-pattern._pointH._x;
        delta = 0.1*bh
        P0 = byA_Point(x=self._pointI2CE._x+delta, y=self._pointI2CE._y-delta/equaLIa)
        P1 = byA_Point(x=0.2*self._pointCCE._x+0.8*self._pointJ._x, y=self._pointCCE._y)
        P2 = byA_Point(x=self._pointCCE._x, y=self._pointCCE._y)
        self._frontNecklinePath = np.array((self._pointI2CE, P0, P1, P2))
        pathStr += ' C ' + str(P0._x) + ',' + str(P0._y)
        pathStr += ' ' + str(P1._x) + ',' + str(P1._y)
        pathStr += ' ' +   str(P2._x) + ',' + str(P2._y)  
        path = self._svg_file.path(d=(pathStr),
                                      id = "curve"+str(self._pointI2CE._name)+str(self._pointCCE._name)+str(curStatureIdx), 
                                      stroke = self._strokes[curStatureIdx], 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
        group.add(path)
        self._pointNCE = byA_Point(x=self._pointN._x-2.5, y=self._pointN._y, name = "NE")
        self._pointECE = byA_Point(x=self._pointE._x-4.75, y=self._pointE._y+4.5, name = "EE")
        self._pointACE = byA_Point(x=self._pointA._x, y=self._pointA._y+2, name = "AE")
        self._pointD2CE = byA_Point(x=self._pointD2._x-4.75, y=self._pointD2._y+2, name = "D2E")
        self.draw_line(group, self._pointECE, self._pointD2CE, curStatureIdx, 'base')
        self.draw_line(group, self._pointD2CE, self._pointACE, curStatureIdx, thickness)
        #self.draw_line(group, self._pointBCE, self._pointACE, curStatureIdx, thickness)
        self.draw_line(group, self._pointNCE, self._pointN, curStatureIdx, 'base')
        
        path = self.compute_curve_from_to_through(self._pointLCE, self._pointNCE, self._pointECE, 0.4, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)

     def draw_waist_line(self, group, curStatureIdx, thickness):
        self._pointW1 = byA_Point(x=self._pointACE._x, y=self._pointACE._y+self._waist_to_hips[curStatureIdx], name = "W1")
        self._pointW2 = byA_Point(x=self._pointACE._x-0.25*self._hips_measurement[curStatureIdx]-5, y=self._pointACE._y+self._waist_to_hips[curStatureIdx], name = "W2")
        self.draw_line(group, self._pointW1, self._pointW2, curStatureIdx, thickness)
        self.draw_line(group, self._pointW1, self._pointACE, curStatureIdx, thickness)
        self.draw_line(group, self._pointW2, self._pointD2CE, curStatureIdx, 'base')
        delta = self.get_distance(self._pointW2, self._pointD2CE)
        P1 = byA_Point(x=self._pointD2CE._x, y=self._pointD2CE._y-0.2*delta)
        P2 = byA_Point(x=self._pointD2CE._x, y=self._pointD2CE._y+0.2*delta)
        pathStr = 'M ' + str(self._pointECE._x) + ',' + str(self._pointECE._y)
        pathStr += ' C ' + str(P1._x) + ',' + str(P1._y)
        pathStr += ' ' +   str(P1._x) + ',' + str(P1._y)  
        pathStr += ' ' +   str(self._pointD2CE._x) + ',' + str(self._pointD2CE._y) 
        path = self._svg_file.path(d=(pathStr),
                                      id = "curve"+str(self._pointECE._name)+str(self._pointD2CE._name)+str(curStatureIdx), 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
        group.add(path)
        pathStr = 'M ' + str(self._pointD2CE._x) + ',' + str(self._pointD2CE._y)
        pathStr += ' C ' + str(P2._x) + ',' + str(P2._y)
        pathStr += ' ' +   str(P2._x) + ',' + str(P2._y)  
        pathStr += ' ' +   str(self._pointW2._x) + ',' + str(self._pointW2._y) 
        path = self._svg_file.path(d=(pathStr),
                                      id = "curve"+str(self._pointD2CE._name)+str(self._pointW2._name)+str(curStatureIdx), 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
        group.add(path)
        #self.compute_curve_from_to_through(self._pointECE, self._pointD2CE, self._pointW2, 0.4, 0, 0, curStatureIdx, self._strokes[curStatureIdx], self._svg_stroke_width_bold)

     def draw_croisure(self, group, curStatureIdx, thickness):
        delta = 0.02*self._hips_measurement[curStatureIdx]
        self._pointW1croisure = byA_Point(x=self._pointW1._x+delta, y=self._pointW1._y, name = "Wc")
        # P(t)= P0(1-t)^3+3P1t(1-t)^2+3P2t^2(1-t)+P3t^3 en x = self._pointW1croisure._x
        Ptx = float(self._pointW1._x-delta)
        deg3 = self._frontNecklinePath[3]._x - self._frontNecklinePath[0]._x + 3 * (self._frontNecklinePath[1]._x - self._frontNecklinePath[2]._x)        
        deg2 = 3*self._frontNecklinePath[0]._x - 6*self._frontNecklinePath[1]._x + 3*self._frontNecklinePath[2]._x
        deg1 = 3*self._frontNecklinePath[1]._x - 3*self._frontNecklinePath[0]._x
        deg0 = self._frontNecklinePath[0]._x-Ptx
        cardan = self.resolution(deg3,deg2,deg1,deg0)
        tReal = [x for x in cardan if x.imag==0]
        tReal = tReal[0].real
        Pty = self._frontNecklinePath[0]._y*(1-tReal)**3 + 3*self._frontNecklinePath[1]._y*tReal*(1-tReal)**2 + 3*self._frontNecklinePath[2]._y*tReal**2*(1-tReal) + self._frontNecklinePath[3]._y*tReal**3
        self._pointCcroisure = byA_Point(x=self._pointCCE._x+delta, y=Pty, name = "Cc")
        
        (P0,P11t,P21t,P31t),(P31t,P22t,P13t,P3) = self.get_sub_curves(self._frontNecklinePath[0], self._frontNecklinePath[1], self._frontNecklinePath[2], self._frontNecklinePath[3], tReal)
        
        pathStr = 'M ' + str(self._pointW1croisure._x) + ',' + str(self._pointW1croisure._y)
        pathStr += ' V ' + str(self._pointCcroisure._y)
        pathStr += ' C' +  str((2*self._frontNecklinePath[3]._x-P22t._x)) + "," + str(P22t._y)
        pathStr += ' ' +  str((2*self._frontNecklinePath[3]._x-P13t._x)) + "," + str(P13t._y)
        pathStr += ' ' +  str(self._frontNecklinePath[3]._x) + "," + str(self._frontNecklinePath[3]._y)  
        pathStr += ' V ' + str(self._pointW1._y)
        pathStr += ' Z'  
        path = self._svg_file.path(d=(pathStr),
                                      id = "curvecroisure"+str(curStatureIdx), 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
        group.add(path)
        
        # button
        self._pointButton = byA_Point(x=self._pointW1._x,y=self._pointECE._y, name="Button")

     def draw_tailored_collar(self, collarBandWidth, upperCollarWidth, group, curStatureIdx, thickness):
        self._pointButtonCroisure = byA_Point(x = self._pointW1._x, y = self._pointButton._y - 1, name="ButtonC")
        self.draw_point(group, self._pointButtonCroisure)
        self._pointCollarBandWidthCenterBack = byA_Point(x = self._pointBCE._x, y = self._pointBCE._y - collarBandWidth, name="Bcbw")
        self._pointCollarBandWidthCenterUpperBack = byA_Point(x = self._pointCollarBandWidthCenterBack._x, y = self._pointCollarBandWidthCenterBack._y + upperCollarWidth, name="Bcbw")
        self._pointCollarKBack = byA_Point(x = self._pointCollarBandWidthCenterBack._x, y = self._pointCollarBandWidthCenterBack._y - collarBandWidth, name="K")
        if group is self._areas["backArea"]:
            self.draw_line(group, self._pointCollarBandWidthCenterBack, self._pointBCE, curStatureIdx, 'base')
        equaShoulderFrontA,equaShoulderFrontB = pattern.get_equation_line(pattern._pointLCE,pattern._pointI2CE)
        angleFront = math.atan(equaShoulderFrontA)
        dx,dy = collarBandWidth*math.cos(-angleFront),collarBandWidth*math.sin(-angleFront)
        self._pointFrontCollarBandWidthShoulderLine = byA_Point(x = self._pointI2CE._x+dx, y = self._pointI2CE._y+dy, name="Icbwf")
        self._pointFrontCollarK2Back = byA_Point(x = self._pointI2CE._x+2*dx, y = self._pointI2CE._y+2*dy, name="K2f")
        if group is self._areas["frontArea"]:
            self.draw_line(group, self._pointFrontCollarBandWidthShoulderLine, self._pointI2CE, curStatureIdx, 'base')
            self.draw_line(group, self._pointFrontCollarBandWidthShoulderLine, self._pointButtonCroisure, curStatureIdx, thickness)
        equaShoulderBackA,equaShoulderBackB = self.get_equation_line(self._pointLCE, self._pointICE)
        angleBack = math.atan(equaShoulderBackA)
        angle = -2*angleFront-angleBack
        self._pointBackCollarBandWidthShoulderLine = byA_Point(x = self._pointICE._x+collarBandWidth*math.cos(angle), y = self._pointICE._y-collarBandWidth*math.sin(angle), name="Icbwb")
        self._pointBackCollarK2 = byA_Point(x = self._pointICE._x+2*collarBandWidth*math.cos(angle), y = self._pointICE._y-2*collarBandWidth*math.sin(angle), name="K2b")
        if group is self._areas["backArea"]:
            # P(t)= P0(1-t)^3+3P1t(1-t)^2+3P2t^2(1-t)+P3t^3 en x = Bc-Icbwb+Ic
            Ptx = self._pointBCE._x-self._pointBackCollarBandWidthShoulderLine._x+self._pointICE._x
            deg3 = self._backNecklinePath[3]._x - self._backNecklinePath[0]._x + 3 * (self._backNecklinePath[1]._x - self._backNecklinePath[2]._x)        
            deg2 = 3*self._backNecklinePath[0]._x - 6*self._backNecklinePath[1]._x + 3*self._backNecklinePath[2]._x
            deg1 = 3*self._backNecklinePath[1]._x - 3*self._backNecklinePath[0]._x
            deg0 = self._backNecklinePath[0]._x-Ptx
            cardan = self.resolution(deg3,deg2,deg1,deg0)
            tReal = [x for x in cardan if x.imag==0]
            tReal = tReal[0].real
            (P0,P11t,P21t,P31t),(P31t,P22t,P13t,P3) = self.get_sub_curves(self._backNecklinePath[0], self._backNecklinePath[1], self._backNecklinePath[2], self._backNecklinePath[3], tReal)
            
            pathStr = 'M ' + str(self._pointBackCollarBandWidthShoulderLine._x) + ',' + str(self._pointBackCollarBandWidthShoulderLine._y)
            pathStr += ' C' +  str((P11t._x+self._pointBackCollarBandWidthShoulderLine._x-self._pointICE._x)) + "," + str((P11t._y-collarBandWidth))
            pathStr += ' ' +  str((P21t._x+self._pointBackCollarBandWidthShoulderLine._x-self._pointICE._x)) + "," + str((P21t._y-collarBandWidth))
            pathStr += ' ' +  str((P31t._x+self._pointBackCollarBandWidthShoulderLine._x-self._pointICE._x)) + "," + str((P31t._y-collarBandWidth))
            path = self._svg_file.path(d=(pathStr),
                                          id = "curvecroisure"+str(curStatureIdx), 
                                          stroke_linejoin = 'round',
                                          fill = 'none')
            path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
            group.add(path)
            
            Ptx = Ptx-self._pointBackCollarBandWidthShoulderLine._x+self._pointICE._x
            deg3 = self._backNecklinePath[3]._x - self._backNecklinePath[0]._x + 3 * (self._backNecklinePath[1]._x - self._backNecklinePath[2]._x)        
            deg2 = 3*self._backNecklinePath[0]._x - 6*self._backNecklinePath[1]._x + 3*self._backNecklinePath[2]._x
            deg1 = 3*self._backNecklinePath[1]._x - 3*self._backNecklinePath[0]._x
            deg0 = self._backNecklinePath[0]._x-Ptx
            cardan = self.resolution(deg3,deg2,deg1,deg0)
            tReal = [x for x in cardan if x.imag==0]
            tReal = tReal[0].real
            (P0,P11t,P21t,P31t),(P31t,P22t,P13t,P3) = self.get_sub_curves(self._backNecklinePath[0], self._backNecklinePath[1], self._backNecklinePath[2], self._backNecklinePath[3], tReal)
            
            pathStr = 'M ' + str(self._pointBackCollarK2._x) + ',' + str(self._pointBackCollarK2._y)
            pathStr += ' C' +  str((P11t._x+self._pointBackCollarK2._x-self._pointICE._x)) + "," + str((P11t._y-2*collarBandWidth))
            pathStr += ' ' +  str((P21t._x+self._pointBackCollarK2._x-self._pointICE._x)) + "," + str((P21t._y-2*collarBandWidth))
            pathStr += ' ' +  str((P31t._x+self._pointBackCollarK2._x-self._pointICE._x)) + "," + str((P31t._y-2*collarBandWidth))
            path = self._svg_file.path(d=(pathStr),
                                          id = "curvecroisure"+str(curStatureIdx), 
                                          stroke_linejoin = 'round',
                                          fill = 'none')
            path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
            group.add(path)
            
     def compute_armhole_depth(self):
            sleevearea = self._cur_stature_area.get_subarea_by_ids("Sleeve", "Base")
            vectELxFront = -0.5 * (self._points["Efront"]._x - self._points["Lfront"]._x)             
            vectELyFront = -0.5 * (self._points["Efront"]._y - self._points["Lfront"]._y)            
            vectELxBack = -0.5 * (self._points["Eback"]._x - self._points["Lback"]._x)             
            vectELyBack = -0.5 * (self._points["Eback"]._y - self._points["Lback"]._y)            
            self._points['CenterShoulderTips'] = self._points["Eback"] + byA_Point(x=vectELxBack, y=vectELyBack) + byA_Point(x=-vectELxFront, y=vectELyFront)
            sleevearea._data["_armehole_depth"] = self.get_distance(self._points['CenterShoulderTips'], self._points["Efront"])

     def draw_sleeve(self, bracelet = 0):
        sleevebasearea = self._cur_stature_area.get_subarea_by_ids("Sleeve", "Base")
        sleeveelargarea = self._cur_stature_area.get_subarea_by_ids("Sleeve", "Enlarg")

        sleevebasesubareas = dict()
        sleeveelargsubareas = dict()
        subsSleeveIds = ["BackSleeve","FrontSleeve","CenterSleeve"]
        for dummy,x in enumerate(subsSleeveIds):
            sleevebasesubareas[x] = byA_PatternArea(id=sleevebasearea.get_id() + str(x))
            sleevebasearea.add(sleevebasesubareas[x])
            sleeveelargsubareas[x] = byA_PatternArea(id=sleeveelargarea.get_id() + str(x))
            sleeveelargarea.add(sleeveelargsubareas[x])

        if (pattern._basic_bodice_enlargement):
            m1 = self._cur_stature_area.get_subarea_by_ids("Front", "BodiceAdjust")._data.get("_front_armhole_bodice_adjustement_curve_measurement")
            m2 = self._cur_stature_area.get_subarea_by_ids("Back", "BodiceAdjust")._data.get("_back_armhole_bodice_adjustement_curve_measurement")
        else:
            m1 = self._cur_stature_area.get_subarea_by_ids("Front", "Base")._data.get("_front_armhole_base_curve_measurement")
            m2 = self._cur_stature_area.get_subarea_by_ids("Back", "Base")._data.get("_back_armhole_base_curve_measurement")
        armhole_measurement = m1+m2

        self._points['SleeveA'] = byA_Point(x=0, y=0, name="SA")
        self._points['SleeveB'] = byA_Point(x=0, y=4.0/5.0*sleevebasearea._data["_armehole_depth"], name="SB") + self._points["SleeveA"]
        ab = self.get_distance(self._points["SleeveA"], self._points["SleeveB"])
        self._points['SleeveC'] = byA_Point(x=-2.0/5.0*armhole_measurement, y=0, name="SC") + self._points["SleeveB"]
        self._points['SleeveD'] = byA_Point(x=2.0/5.0*armhole_measurement, y=0, name="SD") + self._points["SleeveB"]
        self.draw_line(sleevebasearea, self._points['SleeveC'], self._points['SleeveD'], curStatureIdx, 'base sleeve')
        self._points['SleeveE'] = byA_Point(x=-1.0/5.0*armhole_measurement, y=0, name="SE") + self._points["SleeveB"]
        self._points['SleeveF'] = byA_Point(x=1.0/5.0*armhole_measurement, y=0, name="SF") + self._points["SleeveB"]
        self._points['SleeveG'] = byA_Point(x=0, y=self._arm_lenght[curStatureIdx]-bracelet, name="SG") + self._points["SleeveA"]
        self.draw_line(sleevebasearea, self._points['SleeveA'], self._points['SleeveG'], curStatureIdx, 'base '+str(self._strokes[curStatureIdx]))
        self._points['SleeveC2'] = byA_Point(x=self._points["SleeveC"]._x, y=self._points["SleeveG"]._y, name="SC'")
        self._points['SleeveD2'] = byA_Point(x=self._points["SleeveD"]._x, y=self._points["SleeveG"]._y, name="SD'")
        self.draw_line(sleevebasearea, self._points['SleeveC'], self._points['SleeveC2'], curStatureIdx, 'base '+str(self._strokes[curStatureIdx]))
        self.draw_line(sleevebasearea, self._points['SleeveD'], self._points['SleeveD2'], curStatureIdx, 'base '+str(self._strokes[curStatureIdx]))
        self.draw_line(sleevebasearea, self._points['SleeveC2'], self._points['SleeveD2'], curStatureIdx, 'base '+str(self._strokes[curStatureIdx]))
        self._points['SleeveE2'] = byA_Point(x=0, y=-2.0/3.0*ab, name="SE'") + self._points["SleeveE"]
        self._points['SleeveF2'] = byA_Point(x=0, y=-1.0/2.0*ab, name="SF'") + self._points["SleeveF"]
        self._points['SleeveF2down'] = byA_Point(x=self._points["SleeveF2"]._x, y=self._points["SleeveD2"]._y, name="SF2d") 
        self._points['SleeveE2down'] = byA_Point(x=self._points["SleeveE2"]._x,y=self._points["SleeveD2"]._y, name='SE2d')
        #pattern.draw_line(pattern._areas["sleeveArea"], pattern._points['SE'], pattern._points['"SleeveE2"'], curStatureIdx, 'base')
        #pattern.draw_line(pattern._areas["sleeveArea"], pattern._points['SF'], pattern._points['SF2'], curStatureIdx, 'base')
        
        pointsarea = self._cur_stature_area.get_subarea_by_ids("Sleeve", "Points")
        for pointKey, pointValue in self._points.items():
            if "Sleeve" in pointKey:
                self.draw_point(pointsarea, pointValue)

        # Curve of the back sleeve (base and enlarg)
        
        equaSCE2a,equaSCE2b = self.get_equation_line(self._points["SleeveC"],self._points["SleeveE2"])
        angle = math.atan(-1.0/equaSCE2a)
        dx = 0.75*math.cos(angle)
        dy = 0.75*math.sin(angle)
        self._points['SleeveCE2Creux'] = byA_Point(x=1.0/3.0*(self._points["SleeveE2"]._x-self._points["SleeveC"]._x), y=1.0/3.0*(self._points["SleeveE2"]._y-self._points["SleeveC"]._y), name="SCE2Creux") + byA_Point(x=dx,y=dy) + self._points["SleeveC"]

        bezier1 = byA_CubicBezier(P1 = self._points['SleeveC'],
                              C1 = byA_Point(x=self._points["SleeveC"]._x+1.0,y=self._points["SleeveC"]._y), 
                              C2 = byA_Point(x=self._points["SleeveCE2Creux"]._x - 1.0*math.cos(math.atan(equaSCE2a)),y=self._points["SleeveCE2Creux"]._y - 1.0*math.sin(math.atan(equaSCE2a))),
                              P2 = self._points['SleeveCE2Creux'])   
        bezier2 = byA_CubicBezier(P1 = self._points['SleeveCE2Creux'],
                              C1 = byA_Point(x=self._points["SleeveCE2Creux"]._x + 1.0*math.cos(math.atan(equaSCE2a)),y=self._points["SleeveCE2Creux"]._y + 1.0*math.sin(math.atan(equaSCE2a))), 
                              C2 = byA_Point(x=self._points["SleeveE2"]._x - 1.0*math.cos(math.atan(equaSCE2a)),y=self._points["SleeveE2"]._y - 1.0*math.sin(math.atan(equaSCE2a))),
                              P2 = self._points['SleeveE2'])
        line1 = byA_Line(P1=self._points["SleeveE2"], P2=self._points['SleeveE2down'])
        line2 = byA_Line(P1=self._points['SleeveE2down'], P2=self._points["SleeveC2"])
        line3 = byA_Line(P1=self._points["SleeveC2"], P2=self._points["SleeveC"])
        curPath = byA_Path(bezier1, bezier2, line1, line2, line3, close=True)
        sleevebasesubareas["BackSleeve"].add_path(curPath.toStr(), id = "curve"+str(curStatureIdx), class_='base '+str(self._strokes[curStatureIdx]))
        self._points['SleeveC2rot'] = copy.deepcopy(self._points["SleeveC2"]);
        self._points['SleeveC2rot'].rotate(3, self._points["SleeveE2"])
        self._points['SleeveE2downRot'] = copy.deepcopy(self._points["SleeveE2down"]);
        self._points['SleeveE2downRot'].rotate(3, self._points["SleeveE2"])
        sleeveelargsubareas["BackSleeve"].add_path(curPath.toStr(), id = "curve"+str(curStatureIdx), class_='base '+str(self._strokes[curStatureIdx]))
        sleeveelargsubareas["BackSleeve"].rotate(3, [self._points["SleeveE2"]._x, self._points["SleeveE2"]._y])
        #sleeveelargsubareas["BackSleeve"].add_path(pathafter.d(), id = "curve"+str(curStatureIdx), class_='base '+str(self._strokes[curStatureIdx]))

        # Curve of the front sleeve (base and enlarg)

        equaSF2Aa,equaSF2Ab = self.get_equation_line(self._points["SleeveA"],self._points["SleeveF2"])
        angle = math.atan(-1.0/equaSF2Aa)
        dx = 1.0*math.cos(angle)
        dy = 1.0*math.sin(angle)
        self._points['SleeveAF2Creux'] = byA_Point(x=1.0/2.0*(self._points["SleeveF2"]._x-self._points["SleeveA"]._x), y=1.0/2.0*(self._points["SleeveF2"]._y-self._points["SleeveA"]._y), name="SAF2Creux") + byA_Point(x=dx,y=dy) + self._points["SleeveA"]

        equaSDF2a,equaSDF2b = self.get_equation_line(self._points["SleeveF2"],self._points["SleeveD"])
        angle = math.atan(-1.0/equaSDF2a)
        dx = -1.0*math.cos(angle)
        dy = -1.0*math.sin(angle)
        self._points['SleeveF2DCreux'] = byA_Point(x=1.0/2.0*(self._points["SleeveD"]._x-self._points["SleeveF2"]._x), y=1.0/2.0*(self._points["SleeveD"]._y-self._points["SleeveF2"]._y), name="SF2DCreux") + byA_Point(x=dx,y=dy) + self._points["SleeveF2"]

        P1 = byA_Point(x=self._points["SleeveAF2Creux"]._x + 1.0*math.cos(math.atan(equaSF2Aa)), y=self._points["SleeveAF2Creux"]._y + 1.0*math.sin(math.atan(equaSF2Aa)))
        P2 = byA_Point(x=self._points["SleeveF2DCreux"]._x - 1.0*math.cos(math.atan(equaSF2Aa)), y=self._points["SleeveF2DCreux"]._y - 1.0*math.sin(math.atan(equaSF2Aa)))
        equaSCreuxCreuxa,equaSCreuxCreuxb = self.get_equation_line(P1,P2)

        bezier1 = byA_CubicBezier(P1 = self._points['SleeveF2'],
                              C1 = byA_Point(x=self._points["SleeveF2"]._x + 1.0*math.cos(math.atan(equaSCreuxCreuxa)),y=self._points["SleeveF2"]._y + 1.0*math.sin(math.atan(equaSCreuxCreuxa))), 
                              C2 = byA_Point(x=self._points["SleeveF2DCreux"]._x - 1.0*math.cos(math.atan(equaSF2Aa)),y=self._points["SleeveF2DCreux"]._y - 1.0*math.sin(math.atan(equaSF2Aa))),
                              P2 = self._points['SleeveF2DCreux'])        
        bezier2 = byA_CubicBezier(P1 = self._points['SleeveF2DCreux'],
                              C1 = byA_Point(x=self._points["SleeveF2DCreux"]._x + 1.0*math.cos(math.atan(equaSF2Aa)),y=self._points["SleeveF2DCreux"]._y + 1.0*math.sin(math.atan(equaSF2Aa))), 
                              C2 = self._points["SleeveD"] + byA_Point(x=dx,y=0),
                              P2 = self._points['SleeveD'])       
        line1 = byA_Line(P1=self._points["SleeveD"], P2=self._points['SleeveD2'])
        line2 = byA_Line(P1=self._points['SleeveD2'], P2=byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2"]._y))
        line3 = byA_Line(P1=byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2"]._y), P2=self._points["SleeveF2"])
        curPath = byA_Path(bezier1, bezier2, line1, line2, line3, close=True)
        sleevebasesubareas["FrontSleeve"].add_path(curPath.toStr(), id = "curve"+str(curStatureIdx), class_='base '+str(self._strokes[curStatureIdx]))
        self._points['SleeveD2rot'] = copy.deepcopy(self._points["SleeveD2"]);
        self._points['SleeveD2rot'].rotate(-3, self._points["SleeveF2"])
        self._points['SleeveF2downRot'] = copy.deepcopy(self._points["SleeveF2down"]);
        self._points['SleeveF2downRot'].rotate(-3, self._points["SleeveF2"])
        line1 = byA_Line(P1=self._points["SleeveD"], P2=self._points['SleeveD2'])
        line2 = byA_Line(P1=self._points['SleeveD2'], P2=byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2"]._y))
        line3 = byA_Line(P1=byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2"]._y), P2=self._points["SleeveF2"])
        curPath = byA_Path(bezier1, bezier2, line1, line2, line3, close=True)
        sleeveelargsubareas["FrontSleeve"].add_path(curPath.toStr(), id = "curve"+str(curStatureIdx), class_='base '+str(self._strokes[curStatureIdx]))
        sleeveelargsubareas["FrontSleeve"].rotate(-3, [self._points["SleeveF2"]._x, self._points["SleeveF2"]._y])

        # Curve of the center sleeve (base and enlarg)

        dx = (self._points["SleeveA"]._x-((self._points["SleeveA"]._y-equaSCE2b)/equaSCE2a))
        frontUpCurve1 = byA_CubicBezier(P1 = self._points['SleeveE2'],
                              C1 = byA_Point(x=self._points["SleeveE2"]._x + 1.0*math.cos(math.atan(equaSCE2a)),y=self._points["SleeveE2"]._y + 1.0*math.sin(math.atan(equaSCE2a))), 
                              C2 = byA_Point(x=self._points["SleeveA"]._x-dx,y=self._points["SleeveA"]._y),
                              P2 = self._points['SleeveA'])        
        dx = 0.5*(self._points["SleeveAF2Creux"]._x-self._points["SleeveA"]._x)
        frontUpCurve2 = byA_CubicBezier(P1 = self._points['SleeveA'],
                              C1 = byA_Point(x=self._points["SleeveA"]._x+dx,y=self._points["SleeveA"]._y), 
                              C2 = byA_Point(x=self._points["SleeveAF2Creux"]._x - 1.0*math.cos(math.atan(equaSF2Aa)),y=self._points["SleeveAF2Creux"]._y - 1.0*math.sin(math.atan(equaSF2Aa))),
                              P2 = self._points['SleeveAF2Creux'])        
        frontUpCurve3 = byA_CubicBezier(P1 = self._points['SleeveAF2Creux'],
                              C1 = byA_Point(x=self._points["SleeveAF2Creux"]._x + 1.0*math.cos(math.atan(equaSF2Aa)),y=self._points["SleeveAF2Creux"]._y + 1.0*math.sin(math.atan(equaSF2Aa))), 
                              C2 = byA_Point(x=self._points["SleeveF2"]._x - 1.0*math.cos(math.atan(equaSCreuxCreuxa)),y=self._points["SleeveF2"]._y - 1.0*math.sin(math.atan(equaSCreuxCreuxa))),
                              P2 = self._points['SleeveF2'])        
        line1 = byA_Line(P1=self._points["SleeveF2"], P2=self._points["SleeveF2down"])
        line2 = byA_Line(P1=self._points["SleeveF2down"], P2=self._points['SleeveE2down'])
        line3 = byA_Line(P1=self._points['SleeveE2down'], P2=self._points["SleeveE2"])
        frontUpCurve = byA_Path(frontUpCurve1, frontUpCurve2, frontUpCurve3, line1, line2, line3, close=True)
        sleevebasesubareas["CenterSleeve"].add_path(frontUpCurve.toStr(), id = "curve"+str(curStatureIdx), class_='base '+str(self._strokes[curStatureIdx]))

        downPath = byA_Path()
        downLine = byA_Line(P1=self._points["SleeveC2rot"], P2=self._points['SleeveD2rot'])
        maxt=6
        for t in range(1,maxt+1):
            downPath.append(byA_Line(P1=byA_Point(c=downLine._svgline.point((t-1)/float(maxt))), P2=byA_Point(c=downLine._svgline.point(t/float(maxt)))))
        sleeveelargsubareas["CenterSleeve"].add_path(downPath.toStr(), id = sleeveelargsubareas["CenterSleeve"].get_id() + "Curve" + str(curStatureIdx), class_='elarg '+str(self._strokes[curStatureIdx]))

        line1bis = byA_Line(P1=self._points["SleeveF2"], P2=self._points["SleeveF2downRot"])
        line3bis = byA_Line(P1=self._points["SleeveE2"], P2=self._points["SleeveE2downRot"])
        tIntersect1 = line1bis._svgline.point(line1bis._svgline.intersect(downLine._svgline)[0][0])
        Ponline1 = byA_Point(x=tIntersect1.real, y=tIntersect1.imag)
        tIntersect3 = line3bis._svgline.point(line3bis._svgline.intersect(downLine._svgline)[0][0])
        Ponline3 = byA_Point(x=tIntersect3.real, y=tIntersect3.imag)
        self.draw_point(sleevebasesubareas["CenterSleeve"], Ponline1)
        self.draw_point(sleevebasesubareas["CenterSleeve"], Ponline3)
        line1 = byA_Line(P1=self._points["SleeveF2"], P2=Ponline1)
        line2 = byA_Line(P1=Ponline1, P2=Ponline3)
        line3 = byA_Line(P1=Ponline3, P2=self._points["SleeveE2"])
        centerpath = byA_Path(frontUpCurve1, frontUpCurve2, frontUpCurve3, line1, line2, line3, close=True)
        sleeveelargsubareas["CenterSleeve"].add_path(centerpath.toStr(), id = sleeveelargsubareas["CenterSleeve"].get_id() + "Curve" + str(curStatureIdx), class_='elarg '+str(self._strokes[curStatureIdx]))

        sleeveelargsubareas["BackSleeve"].replace_point(self._points["SleeveE2down"], Ponline3.rotate(-3, self._points["SleeveE2"]))
        sleeveelargsubareas["FrontSleeve"].replace_point(self._points["SleeveF2down"], Ponline1.rotate(3, self._points["SleeveF2"]))

        # Creative sleeve byAnhor

        dp = byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2"]._y) - self._points['SleeveA']
        dirpm = byA_Point(x=0.5*dp._x,y=-0.5*dp._y)
        dirmm = byA_Point(x=-0.5*dp._x,y=-0.5*dp._y)
        dirpp = byA_Point(x=0.5*dp._x,y=0.5*dp._y)
        dirmp = byA_Point(x=-0.5*dp._x,y=0.5*dp._y)
        bezier1 = byA_CubicBezier(P1 = self._points['SleeveA'],
                              C1 = self._points['SleeveA'] + dirpp,
                              C2 = byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2rot"]._y) + dirpm,
                              P2 = byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2rot"]._y))   
        bezier2 = byA_CubicBezier(P1 = byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2rot"]._y),
                              C1 = byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2rot"]._y) + dirmm,
                              C2 = self._points['SleeveA'] + dirmp,
                              P2 = self._points['SleeveA'])   
        sleeveelargsubareas["CenterSleeve"].add_path(byA_Path(bezier1, bezier2, closed=True).toStr(), id = sleeveelargsubareas["CenterSleeve"].get_id() + "byAnhor2_" + str(curStatureIdx), stroke_linejoin = 'round', class_='base '+str(self._strokes[curStatureIdx]))
        
        PSAtleft = self._points['SleeveA'] - byA_Point(x=2,y=0);
        PSAtright = self._points['SleeveA'] + byA_Point(x=2,y=0);
        PSBtleft = byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2rot"]._y) - byA_Point(x=2,y=0);
        PSBtright = byA_Point(x=self._points["SleeveF2"]._x,y=self._points["SleeveD2rot"]._y) + byA_Point(x=2,y=0);        
        bezier3 = byA_CubicBezier(P1 = PSAtleft,
                              C1 = PSAtleft + dirmp,
                              C2 = PSBtleft + dirmm,
                              P2 = PSBtleft)   
        (T1,T2) = bezier3._svgcubicbezier.intersect(frontUpCurve1._svgcubicbezier)[0]
        (sub1bezier3,sub2bezier3) = bezier3.split(T1)
        (sub1frontUpCurve1,sub2frontUpCurve1) = frontUpCurve1.split(T2)
        bezier4 = byA_CubicBezier(P1 = PSBtright,
                              C1 = PSBtright + dirpm,
                              C2 = PSAtright + dirpp,
                              P2 = PSAtright) 
        (T1,T2) = bezier4._svgcubicbezier.intersect(frontUpCurve2._svgcubicbezier)[0]
        (sub1bezier4,sub2bezier4) = bezier4.split(T1)
        (sub1frontUpCurve2,sub2frontUpCurve2) = frontUpCurve2.split(T2)
        
        line2 = byA_Line(P1 = PSBtleft, P2 = PSBtright)
        sleeveelargsubareas["CenterSleeve"].add_path(byA_Path(sub2bezier3, line2, sub1bezier4, sub1frontUpCurve2, sub2frontUpCurve1, closed=True).toStr(), id = sleeveelargsubareas["CenterSleeve"].get_id() + "byAnhor1_" + str(curStatureIdx), class_='base '+str(self._strokes[curStatureIdx]))
        
     def display(self):
        print "PATTERN"
        for attr in self.__dict__.keys():
            print attr, getattr(self,attr)

if __name__ == '__main__':
    
    pattern = byA_PatternGenerator(basic_bodice_enlargement='True')

    a4Size = np.array((21,29.7))
    pdfSize = np.trunc(0.95*a4Size)
    
    pattern.open_svg("pattern.svg", pdfSize)
    
    # Creation of the working area and the pdf area
    pattern.create_areas()
    
    for curStatureIdx,curStature in enumerate(pattern._stature):
        
        print "Stature", curStature
        
        pattern.fill_working_area(curStature, ("Front","Back","Sleeve"), ("Base","BodiceAdjust", "Enlarg") if pattern._basic_bodice_enlargement else ("Base","BodiceAdjust"))

        # Points
        pattern.place_base_points()

        # Base, lines
        pattern.draw_base_curves_front()
        pattern.draw_base_curves_back()
        pattern.save_svg()

        # Elargissements
        if (pattern._basic_bodice_enlargement):
            pattern.draw_bodice_adjustement_curves_front()
            pattern.draw_bodice_adjustement_curves_back()
            for oldkey in [k for k,v in pattern._points.items() if "bafront" in k]:
                pattern._points[oldkey.replace("bafront", "front")] = pattern._points.pop(oldkey)
            for oldkey in [k for k,v in pattern._points.items() if "baback" in k]:
                pattern._points[oldkey.replace("baback", "back")] = pattern._points.pop(oldkey)

        # Compute arlhole depth
        pattern.compute_armhole_depth()
        
        # Sleeve
        pattern.draw_sleeve(3.5)

        pattern.save_svg()

        # Translate front and back area to the same armpits point)
        frontarea = pattern._cur_stature_area.get_subarea_by_ids("Front")
        backarea = pattern._cur_stature_area.get_subarea_by_ids("Back")
        sleevarea = pattern._cur_stature_area.get_subarea_by_ids("Sleeve")
        print "before queries"
        pattern._svg_file.query(frontarea)
        print "..."
        pattern._svg_file.query(backarea)
        print "..."
        pattern._svg_file.query(sleevarea)
        print "after queries"
        frontarea.translate(frontarea.getX()*-PXCM,-pattern._points["Ifront"]._y)
        backarea.translate((backarea.getX()-2.0*frontarea.getW())*-PXCM,-pattern._points["Iback"]._y)
        sleevarea.translate((sleevarea.getX()-2.0*(frontarea.getW()+backarea.getW()))*-PXCM,-pattern._points["SleeveA"]._y)

        pattern.save_svg()

        #pattern.draw_abdomen_adjustement(pattern._areas["frontArea"], curStatureIdx, 'abdomen')
        #pattern.draw_coat_enlargement_back(pattern._areas["backArea"], curStatureIdx, 'coat')
        #pattern.draw_coat_enlargement_front(pattern._areas["frontArea"], curStatureIdx, 'coat')
        #for frontbackId,frontback in enumerate(("front","back")):
        #    pattern.draw_waist_line(pattern._areas[frontback+"Area"], curStatureIdx, 'coat') 

        #pattern.draw_croisure(pattern._areas["frontArea"], curStatureIdx, 'coat')
        #for frontbackId,frontback in enumerate(("front","back")):
        #    pattern.draw_tailored_collar(2.0, 3.5, pattern._areas[frontback+"Area"], curStatureIdx, 'coat')
        
        #for point in ([attr for attr in vars(pattern).items() if "_point" in attr[0]]):
        #    if "front" in getattr(pattern, point[0])._pattern :
        #        pattern.draw_point(pattern._areas["frontArea"], getattr(pattern, point[0]))
        #    if "back" in getattr(pattern, point[0])._pattern :
        #        pattern.draw_point(pattern._areas["backArea"], getattr(pattern, point[0]))

        #pattern._areas["frontAreaMirror"] = copy.deepcopy(pattern._areas["frontArea"])
        #pattern._areas["frontAreaMirror"]['id'] += "Mirror"
        #pattern._areas["frontAreaMirror"].scale(-1,1)
        #pattern._areas[curStatureAreaStr].add(pattern._areas["frontAreaMirror"])
    
        #pattern._areas["backAreaRotated"] = copy.deepcopy(pattern._areas["backArea"])
        #pattern._areas["backAreaRotated"]['id'] += "Rotated"
        #equaLIa,equaLIb = pattern.get_equation_line(pattern._pointLCE,pattern._pointICE)
        #equaL2I2a,equaL2I2b = pattern.get_equation_line(pattern._pointLCE,pattern._pointI2CE)
        #rotangle=-math.degrees(math.atan(equaLIa)) - math.degrees(math.atan(equaL2I2a))
        #pattern._areas["backAreaRotated"].scale(1,-1)
        #pattern._areas["backAreaRotated"].translate((pattern._pointICE._x-pattern._pointI2CE._x)*,(pattern._pointICE._y+pattern._pointI2CE._y))
        #pattern._areas["backAreaRotated"].rotate(rotangle, [pattern._pointICE._x, pattern._pointICE._y])
        #pattern._areas[curStatureAreaStr].add(pattern._areas["backAreaRotated"])
        
        for xx,x in enumerate(["Front", "Back", "Sleeve"]):
            allarea = pattern._cur_stature_area.get_subarea_by_ids(x)
            justbodiceadjustarea = pattern._cur_stature_area.get_subarea_by_ids(x, "BodiceAdjust")
            copyarea = copy.deepcopy(justbodiceadjustarea)
            copyarea._g['transform'] = allarea._g['transform']
            copyarea.set_id("Clean"+copyarea.get_id())
            copyarea.translate(0, 2*pdfSize[1])
            pattern._clean_area.add(copyarea)
        pattern.save_svg()

    pattern._svg_file.query(pattern._clean_area)
    padding=50
    RATIODPI = 2.54/96.0
    paddingline = byA_Line(P1=byA_Point(x=(pattern._clean_area.getX()-padding)*PXCM,y=(pattern._clean_area.getY()-padding)*PXCM), 
                           P2=byA_Point(x=(pattern._clean_area.getX()+pattern._clean_area.getW()+padding)*PXCM,y=(pattern._clean_area.getY()+pattern._clean_area.getH()+padding)*PXCM))        
    pattern._clean_area.add_path(byA_Path(paddingline, id="Padding"+str(padding), closed=False).toStr())
    pattern.save_svg()
    
    pattern._svg_file.resizepagetocontent()

    pdfSheets = byA_PDFGrid(PDFSize = pdfSize)
    pdfSheets.replicate(width=pattern._clean_area.getW()+2*padding, height=pattern._clean_area.getH()+2*padding)
    pdfArea = byA_PatternArea(id="PDFArea")
    pattern._clean_area.add(pdfArea)
    for oneSheet in pdfSheets._allPDFSheetPaths:
        pdfArea.add_path(oneSheet[0].toStr(), id=oneSheet[1], class_="onePdfSheet", transform=oneSheet[2])
    pdfArea.translate(0, 2*pdfSize[1])
    
    pattern.save_svg()

    #for q in ["x","y","width","height"]:
    #    query["pdfArea"+q]=float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
    #                      "--query-id=pdfArea",
    #                      "--query-"+q,
    #                      pattern._svg_file.filename]))
    #    print "pdfArea"+q, "=", query["pdfArea"+q]

    #tx = str(PXCM * (query["cleanAreaPaddingx"]-query["pdfAreax"]))
    #ty = str(PXCM * (query["cleanAreaPaddingy"]-query["pdfAreay"]))
    #pattern._areas["pdfArea"]['transform'] = "translate(" + tx + "," + ty + ")"
    #pattern.save_svg()

    #utilPdfAreas = list();
    #for x in range(0, int(min(nbPdf[0], math.ceil((RATIODPI*query["cleanAreaPaddingwidth"])/pdfSize[0])))):
    #    for y in range(0, int(min(nbPdf[1], math.ceil((RATIODPI*query["cleanAreaPaddingheight"])/pdfSize[1])))):
    #        xyPdfSheet = "sheet_" + str(x) + "_" + str(y)
    #        utilPdfAreas.append("png\\"+(pattern._svg_file.filename.replace(".svg","") + "_" + xyPdfSheet + ".png"))
    #        p=subprocess.call(["C:\\Program Files\\Inkscape\\inkscape.exe",
    #                          '--export-png=' + utilPdfAreas[-1],
    #                          '--export-id=' + xyPdfSheet,
    #                          '--export-dpi=300', 
    #                          '--export-background-opacity=1',
    #                          pattern._svg_file.filename])

    #makePdf(pattern._svg_file.filename.replace(".svg",".pdf"), utilPdfAreas, pdfSize[0], pdfSize[1])


    
