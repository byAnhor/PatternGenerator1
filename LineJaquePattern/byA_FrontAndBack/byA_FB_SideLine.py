"""
Created on Fri Mar 22 11:04:19 2019

@author: byAnhor
"""
import numpy as np
from byA_SVGUtils.byA_Point import byA_Point
from byA_SVGUtils.byA_Line import byA_Line
from byA_PatternStep import byA_PatternStep

PXCM = 1.0/35.43307
HORIZONTAL_MARGIN_MM = 50
VERTICAL_MARGIN_MM = 50
a0Size = np.array((841,1189))

class byA_FB_SideLine(byA_PatternStep):

     def __init__(self,**kwargs):
        """Constructor
        """
        byA_PatternStep.__init__(self,**kwargs)
        self._freeze(self.__class__.__name__+"_Parent")

     def addToGroup(self, frontorback, drawing, svggroup, **extra):
        """add a line to a SVG group
        """        
        super(byA_FB_SideLine, self).addToGroup(drawing, svggroup, **extra)

class byA_FrontSideLine(byA_FB_SideLine):

     def __init__(self,**kwargs):
        """Constructor
        """
        self.__class__.__bases__[0].__init__(self,**kwargs)
        
        aMark = self._parent._dicoConstruction['FrontBustLineMark_mark']
        waistMark = self._parent._dicoConstruction['FrontDartWaistLine_dart1']
        hipMark = self._parent._dicoConstruction['FrontHipLineMark_mark']

        self._bustToWaist = byA_Line(P1=aMark, P2=waistMark)
        self._waistToHip = byA_Line(P1=waistMark, P2=hipMark)
        waistToHipLenght = self._waistToHip.lenght()
        waistToHipX = abs(self._waistToHip._to._x - self._waistToHip._from._x)
        waistToHipY = abs(self._waistToHip._to._y - self._waistToHip._from._y)
        
        # 8 cm as specifed in the book give strange curves for high stature so try to 
        # modulate it 
        val8cm = 80 * waistToHipX / 48.75; # 48.75 is the waistToHipX for size 38
        
        self._8cm = byA_Point(x=waistMark._x-(waistToHipX*val8cm/waistToHipLenght),y=waistMark._y+(waistToHipY*val8cm/waistToHipLenght))
        self._1cm = byA_Point(x=self._8cm._x-10,y=self._8cm._y)

        self._constructionPoint.append(('_8cm',self._8cm, 'd8'))
        self._constructionPoint.append(('_1cm',self._1cm, 'v1'))
        self._finalLine.append(('_bustToWaist',self._bustToWaist, ''))
        self._constructionLine.append(('_waistToHip',self._waistToHip, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze(self.__class__.__name__)

     def addToGroup(self, drawing, svggroup, **extra):
         super(self.__class__, self).addToGroup("Front", drawing, svggroup, **extra)

class byA_BackSideLine(byA_FB_SideLine):

     def __init__(self,**kwargs):
        """Constructor
        """
        self.__class__.__bases__[0].__init__(self,**kwargs)
        
        bMark = self._parent._dicoConstruction['BackBustLineMark_mark']
        waistMark = self._parent._dicoConstruction['BackDartWaistLine_dart1']
        hipMark = self._parent._dicoConstruction['BackHipLineMark_mark']

        self._bustToWaist = byA_Line(P1=bMark, P2=waistMark)
        self._waistToHip = byA_Line(P1=waistMark, P2=hipMark)
        waistToHipLenght = self._waistToHip.lenght()
        waistToHipX = abs(self._waistToHip._to._x - self._waistToHip._from._x)
        waistToHipY = abs(self._waistToHip._to._y - self._waistToHip._from._y)

        # 8 cm as specifed in the book give strange curves for high stature so try to 
        # modulate it 
        val8cm = 80 * waistToHipX / 48.75; # 48.75 is the waistToHipX for size 38

        self._8cm = byA_Point(x=waistMark._x+(waistToHipX*val8cm/waistToHipLenght),y=waistMark._y+(waistToHipY*val8cm/waistToHipLenght))
        self._1cm = byA_Point(x=self._8cm._x+10,y=self._8cm._y)

        self._constructionPoint.append(('_8cm',self._8cm, 'd8'))
        self._constructionPoint.append(('_1cm',self._1cm, 'v1'))
        self._finalLine.append(('_bustToWaist',self._bustToWaist, ''))
        self._constructionLine.append(('_waistToHip',self._waistToHip, ''))

        self.fillDicoPoints(self.__class__.__name__.replace("byA_",""), self._parent)
        self._freeze(self.__class__.__name__)

     def addToGroup(self, drawing, svggroup, **extra):
         super(self.__class__, self).addToGroup("Back", drawing, svggroup, **extra)

if __name__ == '__main__':
    None
    