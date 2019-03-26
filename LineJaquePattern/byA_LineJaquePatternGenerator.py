"""
Created on Fri Mar 22 11:04:19 2019

@author: byAnhor
"""
import numpy as np
import svgwrite 
import csv
from byA_SVGUtils.byA_FrozenClass import byA_FrozenClass
from byA_HipLine import byA_HipLine
from byA_WaistLine import byA_WaistLine
from byA_BustLine import byA_BustLine
from byA_FrontAndBack.byA_FB_Middle import byA_MiddleFront, byA_MiddleBack
from byA_FrontAndBack.byA_FB_BustLineMark import byA_FrontBustLineMark, byA_BackBustLineMark
from byA_FrontAndBack.byA_FB_HipLineMark import byA_FrontHipLineMark, byA_BackHipLineMark
from byA_FrontAndBack.byA_FB_BodiceLenghtLine import byA_FrontBodiceLenghtLine, byA_BackBodiceLenghtLine
from byA_FrontAndBack.byA_FB_DartBustLine import byA_FrontDartBustLine, byA_BackDartBustLine
from byA_FrontAndBack.byA_FB_DartWaistLine import byA_FrontDartWaistLine, byA_BackDartWaistLine
from byA_FrontAndBack.byA_FB_SideLine import byA_FrontSideLine, byA_BackSideLine
from byA_FrontAndBack.byA_FB_SideCurve import byA_FrontSideCurve, byA_BackSideCurve
from byA_FrontAndBack.byA_FB_Dart import byA_FrontDart, byA_BackDart

PXCM = 1.0/35.43307

class byA_LineJaquePatternGenerator(byA_FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_FrozenClass.__init__(self)
        self._liststatures = kwargs.get('liststatures', '')
        self._currentStature = None
        self._sheetSize = kwargs.get('sheetSize', a0Size)
        self._filename = kwargs.get('filename', 'pattern.svg')
        self._dicoConstruction = dict()
        self._dicoMesures = kwargs.get('dicoMesures', a0Size)        
        w = str(self._sheetSize[0]).replace("cm","")
        h = str(self._sheetSize[1]).replace("cm","")
        self._svgDrawing = svgwrite.Drawing(self._filename, [str(int(w))+'cm',str(int(h))+'cm'], profile='full')
        self._svgDrawing.viewbox(width=str(int(w)), height=str(int(h)))
        self._Stature = dict()
        self._FrontPattern = dict()
        self._BackPattern = dict()
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
        self._FrontDartBustLine = dict()
        self._BackDartBustLine = dict()
        self._FrontDartWaistLine = dict()
        self._BackDartWaistLine = dict()
        self._FrontSideLine = dict()
        self._BackSideLine = dict()
        self._FrontSideCurve = dict()
        self._BackSideCurve = dict()
        self._FrontDart = dict()
        self._BackDart = dict()

        svgStyle = svgwrite.container.Style()
        svgStyle['id'] = "LineJaquePatternStyles"
        
        svgStyle.append(' text.nomenclature {font-family: cursive;}')
        svgStyle.append(' text.nomenclature {font-size:' + str(200*PXCM) + ';}')
        svgStyle.append(' text.nomenclature {fill:#e6e6e6;}')
        svgStyle.append(' text.nomenclature {stroke-width:' + str(6*PXCM) + ';}')
        svgStyle.append(' text.nomenclature {opacity:0.5}')
        
        svgStyle.append(' path.middleline {stroke:black;}')
        svgStyle.append(' path.middleline {stroke-width:' + str(15*PXCM) + ';}')
        svgStyle.append(' path.middleline {opacity:1.0; }')
        
        svgStyle.append(' path.horizline {stroke:black;}')
        svgStyle.append(' path.horizline {stroke-width:' + str(6*PXCM) + ';}')
        svgStyle.append(' path.horizline {stroke-dasharray:' + str(6) +','+ str(3) + '}')
        svgStyle.append(' path.horizline {opacity:1.0; }')

        svgStyle.append(' circle.constructionPoint {stroke:none;}')
        #svgStyle.append(' circle.constructionPoint {fill:xxx;}')
        svgStyle.append(' circle.constructionPoint {opacity:0.5;}')
        
        svgStyle.append(' path.constructionLine {stroke:black;}')
        svgStyle.append(' path.constructionLine {stroke-width:' + str(6*PXCM) + ';}')
        svgStyle.append(' path.constructionLine {stroke-dasharray:' + str(2) +','+ str(2) + '}')
        svgStyle.append(' path.constructionLine {opacity:1.0; }')

        svgStyle.append(' path.constructionCurve {stroke:black;}')
        svgStyle.append(' path.constructionCurve {stroke-width:' + str(6*PXCM) + ';}')
        svgStyle.append(' path.constructionCurve {stroke-dasharray:' + str(2) +','+ str(2) + '}')
        svgStyle.append(' path.constructionCurve {opacity:1.0; }')

        svgStyle.append(' circle.finalPoint {stroke:none;}')
        #svgStyle.append(' circle.finalPoint {fill:xxx;}')
        svgStyle.append(' circle.finalPoint {opacity:0.5;}')

        svgStyle.append(' path.finalLine {fill:none;}')
        #svgStyle.append(' path.finalLine {stroke:xxx;}')
        svgStyle.append(' path.finalLine {stroke-width:' + str(25*PXCM) + ';}')
        svgStyle.append(' path.finalLine {opacity:1.0; }')

        svgStyle.append(' path.finalCurve {fill:none;}')
        #svgStyle.append(' path.finalCurve {stroke:xxx;}')
        svgStyle.append(' path.finalCurve {stroke-width:' + str(25*PXCM) + ';}')
        svgStyle.append(' path.finalCurve {opacity:1.0; }')

        #svgStyle.append(' .pointCaption {fill: black; font-family: Verdana; font-size:' + str(5*PXCM) + ';}')
        #svgStyle.append(' .pointCircle {fill: green;}')
        #svgStyle.append(' line.base {stroke-width:' + str(1*PXCM) + '; opacity:0.1}')
        #svgStyle.append(' path.base {stroke-width:' + str(1*PXCM) + '; opacity:0.1; stroke_linejoin:round}')
        #svgStyle.append(' line.bodiceadjust {stroke-width:' + str(1*PXCM) + '; stroke_linejoin:round}')
        #svgStyle.append(' path.bodiceadjust {stroke-width:' + str(1*PXCM) + '; stroke_linejoin:round}')
        #svgStyle.append(' line.elarg {stroke-width:' + str(1*PXCM) + '; stroke_linejoin:round}')
        #svgStyle.append(' path.elarg {stroke-width:' + str(1*PXCM) + '; stroke_linejoin:round}')
        #svgStyle.append(' line.abdomen {stroke-width:' + str(4.5*PXCM) + '; opacity:0.1; stroke-dasharray:' + str(0.15) +','+ str(0.05) + '}')
        #svgStyle.append(' path.abdomen {stroke-width:' + str(4.5*PXCM) + '; opacity:0.1; stroke-dasharray:' + str(0.15) +','+ str(0.05) + '}')
        #svgStyle.append(' line.coat {stroke-width:' + str(6*PXCM) + ';}')
        #svgStyle.append(' path.coat {stroke-width:' + str(6*PXCM) + ';}')
        #for sizeFigure, sizeTxt in enumerate(('thin', 'normal', 'bold')):
        #    svgStyle.append(' line.' + sizeTxt + "{stroke-width : " + str((sizeFigure+1)*PXCM) + "; stroke-dasharray:" + str(0.05) +','+ str(0.05) + '}')
        #    svgStyle.append(' path.' + sizeTxt + "{stroke-width : " + str((sizeFigure+1)*PXCM) + "; stroke-dasharray:" + str(0.05) +','+ str(0.05) + '}')
        for s in self._liststatures:
            svgStyle.append(' circle.stature' + str(s) + " {stroke : " + self._dicoMesures['Couleur'+str(s)] + ";}")
            svgStyle.append(' path.stature' + str(s) + " {stroke : " + self._dicoMesures['Couleur'+str(s)] + ";}")
        self._svgDrawing.add(svgStyle)

        self._freeze("byA_LineJaquePatternGenerator")

     def set_currentStature(self, stature):
        self._currentStature = stature

        self._Stature[self._currentStature] = svgwrite.container.Group(id="groupStature"+self._currentStature)
        self._FrontPattern[self._currentStature] = svgwrite.container.Group(id="groupFront"+self._currentStature)
        self._BackPattern[self._currentStature] = svgwrite.container.Group(id="groupBack"+self._currentStature)

        self._svgDrawing.add(self._Stature[self._currentStature])
        self._Stature[self._currentStature].add(self._FrontPattern[self._currentStature])
        self._Stature[self._currentStature].add(self._BackPattern[self._currentStature])
        
        self._svgDrawing.save()
         
     def trace_MiddleFront(self):
        self._MiddleFront[self._currentStature] = byA_MiddleFront(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupMiddleFront = svgwrite.container.Group(id="groupMiddleFront"+self._currentStature)
        self._FrontPattern[self._currentStature].add(groupMiddleFront)
        self._MiddleFront[self._currentStature].addToGroup(self._svgDrawing, groupMiddleFront, id="middleFront", class_='middleline')
        self._svgDrawing.save()
        
     def trace_MiddleBack(self):
        self._MiddleBack[self._currentStature] = byA_MiddleBack(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupMiddleBack = svgwrite.container.Group(id="groupMiddleBack"+self._currentStature, debug=False)
        self._BackPattern[self._currentStature].add(groupMiddleBack)
        self._MiddleBack[self._currentStature].addToGroup(self._svgDrawing, groupMiddleBack, id="middleBack", class_='middleline')
        self._svgDrawing.save()

     def trace_HipLine(self):
        self._HipLine[self._currentStature] = byA_HipLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        for side in ('Front', 'Back'):
            group = svgwrite.container.Group(id="groupHipLine"+side+self._currentStature, debug=False)
            self.__getattribute__('_'+side+'Pattern')[self._currentStature].add(group)
            self._HipLine[self._currentStature].addToGroup(self._svgDrawing, group, id="HipLine"+side, class_='horizline')
        self._svgDrawing.save()

     def trace_WaistLine(self):
        self._WaistLine[self._currentStature] = byA_WaistLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        for side in ('Front', 'Back'):
            group = svgwrite.container.Group(id="groupWaistLine"+side+self._currentStature, debug=False)
            self.__getattribute__('_'+side+'Pattern')[self._currentStature].add(group)
            self._WaistLine[self._currentStature].addToGroup(self._svgDrawing, group, id="WaistLine"+side, class_='horizline')
        self._svgDrawing.save()

     def trace_BustLine(self):
        self._BustLine[self._currentStature] = byA_BustLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        for side in ('Front', 'Back'):
            group = svgwrite.container.Group(id="groupBustLine"+side+self._currentStature, debug=False)
            self.__getattribute__('_'+side+'Pattern')[self._currentStature].add(group)
            self._BustLine[self._currentStature].addToGroup(self._svgDrawing, group, id="BustLine"+side, class_='horizline')
        self._svgDrawing.save()
        
     def mark_FrontBustLine(self):
        self._FrontBustLineMark[self._currentStature] = byA_FrontBustLineMark(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBustLine = None
        for elem in self._FrontPattern[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupBustLine")):
                groupBustLine = elem
        assert(groupBustLine is not None)
        self._FrontBustLineMark[self._currentStature].addToGroup(self._svgDrawing, groupBustLine, id="frontBustMark")
        self._svgDrawing.save()

     def mark_BackBustLine(self):
        self._BackBustLineMark[self._currentStature] = byA_BackBustLineMark(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBustLine = None
        for elem in self._BackPattern[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupBustLine")):
                groupBustLine = elem
        assert(groupBustLine is not None)
        self._BackBustLineMark[self._currentStature].addToGroup(self._svgDrawing, groupBustLine, id="backBustMark")
        self._svgDrawing.save()

     def mark_FrontHipLine(self):
        self._FrontHipLineMark[self._currentStature] = byA_FrontHipLineMark(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupHipLine = None
        for elem in self._FrontPattern[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupHipLine")):
                groupHipLine = elem
        assert(groupHipLine is not None)
        self._FrontHipLineMark[self._currentStature].addToGroup(self._svgDrawing, groupHipLine, id="frontHipMark")
        self._svgDrawing.save()

     def mark_BackHipLine(self):
        self._BackHipLineMark[self._currentStature] = byA_BackHipLineMark(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupHipLine = None
        for elem in self._BackPattern[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupHipLine")):
                groupHipLine = elem
        assert(groupHipLine is not None)
        self._BackHipLineMark[self._currentStature].addToGroup(self._svgDrawing, groupHipLine, id="backHipMark")
        self._svgDrawing.save()

     def trace_FrontBodiceLenght(self):
        self._FrontBodiceLenghtLine[self._currentStature] = byA_FrontBodiceLenghtLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupFrontBodiceLenghtLine = svgwrite.container.Group(id="groupFrontBodiceLenghtLine"+self._currentStature, debug=False)
        self._FrontPattern[self._currentStature].add(groupFrontBodiceLenghtLine)
        self._FrontBodiceLenghtLine[self._currentStature].addToGroup(self._svgDrawing, groupFrontBodiceLenghtLine, id="frontBodiceLenghtLine")
        self._svgDrawing.save()

     def trace_BackBodiceLenght(self):
        self._BackBodiceLenghtLine[self._currentStature] = byA_BackBodiceLenghtLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBackBodiceLenghtLine = svgwrite.container.Group(id="groupBackBodiceLenghtLine"+self._currentStature, debug=False)
        self._BackPattern[self._currentStature].add(groupBackBodiceLenghtLine)
        self._BackBodiceLenghtLine[self._currentStature].addToGroup(self._svgDrawing, groupBackBodiceLenghtLine, id="backBodiceLenghtLine")
        self._svgDrawing.save()
        
     def mark_FrontDartBustLine(self):
        self._FrontDartBustLine[self._currentStature] = byA_FrontDartBustLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBustLine = None
        for elem in self._FrontPattern[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupBustLine")):
                groupBustLine = elem
        assert(groupBustLine is not None)
        self._FrontDartBustLine[self._currentStature].addToGroup(self._svgDrawing, groupBustLine, id="frontDartBustMark")
        self._svgDrawing.save()
         
     def mark_BackDartBustLine(self):
        self._BackDartBustLine[self._currentStature] = byA_BackDartBustLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBustLine = None
        for elem in self._BackPattern[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupBustLine")):
                groupBustLine = elem
        assert(groupBustLine is not None)
        self._BackDartBustLine[self._currentStature].addToGroup(self._svgDrawing, groupBustLine, id="backDartBustMark")
        self._svgDrawing.save()

     def mark_FrontDartWaistLine(self):
        self._FrontDartWaistLine[self._currentStature] = byA_FrontDartWaistLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupWaistLine = None
        for elem in self._FrontPattern[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupWaistLine")):
                groupWaistLine = elem
        assert(groupWaistLine is not None)
        self._FrontDartWaistLine[self._currentStature].addToGroup(self._svgDrawing, groupWaistLine, id="frontDartWaistMark")
        self._svgDrawing.save()

     def mark_BackDartWaistLine(self):
        self._BackDartWaistLine[self._currentStature] = byA_BackDartWaistLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupWaistLine = None
        for elem in self._BackPattern[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupWaistLine")):
                groupWaistLine = elem
        assert(groupWaistLine is not None)
        self._BackDartWaistLine[self._currentStature].addToGroup(self._svgDrawing, groupWaistLine, id="backDartWaistMark")
        self._svgDrawing.save()

     def mark_FrontSideLine(self):
        self._FrontSideLine[self._currentStature] = byA_FrontSideLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupFrontSide = svgwrite.container.Group(id="groupFrontSide"+self._currentStature, debug=False)
        self._FrontPattern[self._currentStature].add(groupFrontSide)
        self._FrontSideLine[self._currentStature].addToGroup(self._svgDrawing, groupFrontSide, id="frontSideLine")
        self._svgDrawing.save()

     def mark_BackSideLine(self):
        self._BackSideLine[self._currentStature] = byA_BackSideLine(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBackSide = svgwrite.container.Group(id="groupBackSide"+self._currentStature, debug=False)
        self._BackPattern[self._currentStature].add(groupBackSide)
        self._BackSideLine[self._currentStature].addToGroup(self._svgDrawing, groupBackSide, id="backSideLine")
        self._svgDrawing.save()

     def trace_FrontSideCurve(self):
        self._FrontSideCurve[self._currentStature] = byA_FrontSideCurve(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupFrontSide = None
        for elem in self._FrontPattern[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupFrontSide")):
                groupFrontSide = elem
        assert(groupFrontSide is not None)
        self._FrontSideCurve[self._currentStature].addToGroup(self._svgDrawing, groupFrontSide, id="frontSideLine")
        self._svgDrawing.save()

     def trace_BackSideCurve(self):
        self._BackSideCurve[self._currentStature] = byA_BackSideCurve(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBackSide = None
        for elem in self._BackPattern[self._currentStature].elements:
            if (isinstance(elem, svgwrite.container.Group) and elem.get_id().startswith("groupBackSide")):
                groupBackSide = elem
        assert(groupBackSide is not None)
        self._BackSideCurve[self._currentStature].addToGroup(self._svgDrawing, groupBackSide, id="backSideLine")
        self._svgDrawing.save()

     def trace_FrontDart(self):
        self._FrontDart[self._currentStature] = byA_FrontDart(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupFrontDart = svgwrite.container.Group(id="groupFrontDart"+self._currentStature, debug=False)
        self._FrontPattern[self._currentStature].add(groupFrontDart)
        self._FrontDart[self._currentStature].addToGroup(self._svgDrawing, groupFrontDart, id="frontSideLine")
        self._svgDrawing.save()

     def trace_BackDart(self):
        self._BackDart[self._currentStature] = byA_BackDart(parent=self, stature=self._currentStature, sheetSize=self._sheetSize, filename=self._filename)
        groupBackDart = svgwrite.container.Group(id="groupBackDart"+self._currentStature, debug=False)
        self._BackPattern[self._currentStature].add(groupBackDart)
        self._BackDart[self._currentStature].addToGroup(self._svgDrawing, groupBackDart, id="backSideLine")
        self._svgDrawing.save()

     def trace_AllStatures(self):
        for stature in self._liststatures[:1]: 
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
            pattern.mark_FrontDartBustLine()
            pattern.mark_BackDartBustLine()
            pattern.mark_FrontDartWaistLine()
            pattern.mark_BackDartWaistLine()
            pattern.mark_FrontSideLine()
            pattern.mark_BackSideLine()
            pattern.trace_FrontSideCurve()
            pattern.trace_BackSideCurve()
            pattern.trace_BackDart()
            pattern.trace_FrontDart()

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
                    if (curRow[0] != "Couleur"):
                        dicoMesures[curRow[0].replace(" ","")+str(stature)] = float(curRow[idx+1])
                    else:
                        dicoMesures[curRow[0].replace(" ","")+str(stature)] = str(curRow[idx+1])
                        
    pattern = byA_LineJaquePatternGenerator(dicoMesures=dicoMesures, liststatures=listStatures, sheetSize=a0Size, filename = "test_LineJaquePatternGenerator.svg")
    pattern.trace_AllStatures()
    pattern.save()
    


