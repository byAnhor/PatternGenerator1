# -*- coding: utf-8 -*-
"""
Created on Wed May 10 10:00:57 2017

@author: orhanda
"""
import numpy as np
import math
from matplotlib.pyplot import *
import copy
import svgwrite  
from svgwrite import cm, mm
from svgpathtools import svg2paths, Path, Line, QuadraticBezier, CubicBezier, Arc, parse_path
from pyx import *
import subprocess
from PyPDF2 import PdfFileWriter
from PIL import Image
from fpdf import FPDF

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

CMPX = 1.0
PXCM = 1.0/35.43307

class FrozenClass(object):
  """ When a class herits from this mother class, it cannot create new attributes that have not been 
      already declared in __init__ method   
  """
  __isFrozen = False
  def __setattr__(self, attr, value):
    if self.__isFrozen and not hasattr(self, attr):
      raise TypeError("%r is a frozen class, please declare attribute %r in __init__" % (self.__class__.__name__, attr))
    super(FrozenClass, self).__setattr__(attr, value)

  def _freeze(self, instance):
    if (self.__class__.__name__ == instance):
      self.__isFrozen = True

# résolution de l'équation du troisième degré par la méthode de Cardan 
 
class Point():
    def __init__(self,**kwargs):
        self._name = kwargs.get('name', "O")
        if 'c' not in kwargs:
            self._x = kwargs.get('x', 0)
            self._y = kwargs.get('y', 0)
        else:
            c = kwargs.get('c', 0+0j)
            self._x = c.real
            self._y = c.imag
        self._drawn = kwargs.get('drawn', False)
        #print "Point", self._name," (", getattr(self,'_x'), ",", getattr(self,'_y'), ")"
    def __add__(self, other):  # Equivalent of + operator
        return Point(x=self._x + other._x, y=self._y + other._y, name=self._name, drawn = self._drawn)
    def __sub__(self, other):  # Equivalent of - operator
        return Point(x=self._x - other._x, y=self._y - other._y, name=self._name, drawn = self._drawn)
    def __mul__(self, other):  # Equivalent of * operator
        return Point(x=self._x * other, y=self._y * other, name=self._name, drawn = self._drawn)
    def __rmul__(self, other):  # Equivalent of * operator
        return Point(x=self._x * other, y=self._y * other, name=self._name, drawn = self._drawn)
    def translate(self, dx, dy):  
        self._x += dx
        self._y += dy
    def rotate(self, degre, centerot = None):  # Equivalent of * operator
        if centerot is None:
            x = self._x * math.cos(math.radians(degre)) - self._y * math.sin(math.radians(degre))
            y = self._x * math.sin(math.radians(degre)) + self._y * math.cos(math.radians(degre))
            self._x = x
            self._y = y
        else:
            self.translate(-centerot._x,-centerot._y)
            self.rotate(degre)
            self.translate(centerot._x,centerot._y)
    def toRI(self):
        return complex(self._x,self._y)

class My_CubicBezier():
    def __init__(self,**kwargs):
        self._from = kwargs.get('P1')
        self._fromcontrol = kwargs.get('C1')
        self._tocontrol = kwargs.get('C2')
        self._to = kwargs.get('P2')
        assert isinstance(self._from, Point)
        assert isinstance(self._fromcontrol, Point)
        assert isinstance(self._tocontrol, Point)
        assert isinstance(self._to, Point)
        self._cubicbezier = CubicBezier(self._from.toRI(), self._fromcontrol.toRI(), self._tocontrol.toRI(), self._to.toRI())
    def toStr(self):
        return Path(self._cubicbezier).d()
    def reverse(self):
        return My_CubicBezier(P1=self._to, C1=self._tocontrol, C2=self._fromcontrol, P2=self._from)
    def split(self, t):
        P12 = self._from + t*(self._fromcontrol - self._from)
        P23 = self._fromcontrol + t*(self._tocontrol - self._fromcontrol)
        P34 = self._tocontrol + t*(self._to - self._tocontrol)
        P123 = P12 + t*(P23-P12)
        P234 = P23 + t*(P34-P23)
        P1234 = P123 + t*(P234-P123)
        return (My_CubicBezier(P1 = self._from, C1 = P12, C2 = P123, P2 = P1234),
                My_CubicBezier(P1 = P1234, C1 = P234, C2 = P34, P2 = self._to))
            
class My_Line():
    def __init__(self,**kwargs):
        self._from = kwargs.get('P1')
        self._to = kwargs.get('P2')
        assert isinstance(self._from, Point)
        assert isinstance(self._to, Point)
        self._line = Line(self._from.toRI(), self._to.toRI())
    def toStr(self):
        return Path(self._line).d()

class My_Path():
    def __init__(self, *segments, **kw):
        self._segments = Path()
        for p in segments:
            assert isinstance(p, My_Line) or isinstance(p, My_CubicBezier)  
            if isinstance(p, My_Line):
                self.insert(-1, p)   
            if isinstance(p, My_CubicBezier):
                self.insert(-1, p)   
        if 'closed' in kw:
            self._segments.closed = kw['closed']  # DEPRECATED
    def insert(self, index, value):
        assert isinstance(value, My_Line) or isinstance(value, My_CubicBezier)  
        if isinstance(value, My_Line):
            self._segments.insert(index, value._line)   
        if isinstance(value, My_CubicBezier):
            self._segments.insert(index, value._cubicbezier)   
    def append(self, value):
        assert isinstance(value, My_Line) or isinstance(value, My_CubicBezier)  
        if isinstance(value, My_Line):
            self._segments.append(value._line)   
        if isinstance(value, My_CubicBezier):
            self._segments.append(value._cubicbezier)   
    def d(self):
        return self._segments.d()

class Pattern_Generator(FrozenClass):

     def __init__(self,**kwargs):
        """Constructor
        """
        # According to Become a pattern drafter (Claire Wargnier)
        self._stature = self.inclusive_range(110,6,2)#11)
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
        self._armehole_depth = None
        self._armhole_front_measurement = None
        self._armhole_back_measurement = None
        self._front_armhole_base_curve = None
        self._back_armhole_base_curve = None
        self._front_neckline_base_curve = None        
        self._back_neckline_base_curve = None  
        self._front_waist_base_curve = None
        self._front_waist_base_curve_lenght = None 
        self._front_armhole_bodice_adjustement_curve = None
        self._back_armhole_bodice_adjustement_curve = None
        self._front_neckline_bodice_adjustement_curve = None        
        self._back_neckline_bodice_adjustement_curve = None  
        self._front_waist_bodice_adjustement_curve = None 
        self._front_waist_bodice_adjustement_curve_lenght = None 
        self.display()
        self._svg_file = None
        self._areas = dict()
        self._strokes = ['black', 'red', 'blue', 'green', 'cyan', 'orange', 'pink', 'purple', 'darkblue', 'olive', 'magenta']
        self._basic_bodice_enlargement = kwargs.get('basic_bodice_enlargement', False)
        self._points = dict()
        self._freeze("Pattern_Generator")

     def inclusive_range(self, start, step, nb):
        res = [start]
        for elem in range(0,nb-1):
            res = np.append(res, [res[-1]+step])
        return res

     def open_svg(self, path, size):
        width = int(size[0])
        height = int(size[1])
        print "width = ", width, " x height = ", height
        self._svg_file = svgwrite.Drawing(path, profile='full', size = (str(width)+'cm', str(height)+'cm'))
        self._svg_file.viewbox(width=str(width), height=str(height))
        
        svgStyle = svgwrite.container.Style()
        svgStyle['id'] = "patternStyles"
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
        for s in self._strokes:
            svgStyle.append(' line.' + str(s) + "{stroke : " + str(s) + ";}")
            svgStyle.append(' path.' + str(s) + "{stroke : " + str(s) + ";}")
        svgStyle.append(' path.onePdfSheet {stroke:orange; stroke-width:0.02;}')            
        self._svg_file.add(svgStyle)
        
     def save_svg(self):
        self._svg_file.save()
        
     def get_equation_line(self, src, dst):
        assert isinstance(src, Point)
        assert isinstance(dst, Point)
        assert not src._x == dst._x
        # y = ax+b
        # src._y = a*src._x + b
        # dst._y = a*dst._x + b
        a = (src._y-dst._y)/(src._x - dst._x)
        return [a, src._y-a*src._x]
        
     def get_distance(self, src, dst):
        assert isinstance(src, Point)
        assert isinstance(dst, Point)
        return math.sqrt((src._y-dst._y)**2+(src._x-dst._x)**2)
        
     def combinaison_lineaire(self, A,B,u,v):
        assert isinstance(A, Point)
        assert isinstance(B, Point)
        return Point(x = A._x*u+B._x*v, y = A._y*u+B._y*v)
    
     def interpolation_lineaire(self, A,B,t):
        return combinaison_lineaire(A,B,t,1-t)

     def point_bezier_3(self, points_control,t):
        x=(1-t)**2
        y=t*t
        A = self.combinaison_lineaire(points_control[0],points_control[1],(1-t)*x,3*t*x)
        B = self.combinaison_lineaire(points_control[2],points_control[3],3*y*(1-t),y*t)
        return Point(x = A._x+B._x, y = A._y+B._y)
    
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
        assert isinstance(P0, Point)
        assert isinstance(P1, Point)
        assert isinstance(P2, Point)
        assert isinstance(P3, Point)
        P11t = Point(x=(1-t)*P0._x+t*P1._x,y=(1-t)*P0._y+t*P1._y, name="") 
        P12t = Point(x=(1-t)*P1._x+t*P2._x,y=(1-t)*P1._y+t*P2._y, name="") 
        P13t = Point(x=(1-t)*P2._x+t*P3._x,y=(1-t)*P2._y+t*P3._y, name="")
        P21t = Point(x=(1-t)*P11t._x+t*P12t._x,y=(1-t)*P11t._y+t*P12t._y, name="")
        P22t = Point(x=(1-t)*P12t._x+t*P13t._x,y=(1-t)*P12t._y+t*P13t._y, name="")
        P31t = Point(x=(1-t)*P21t._x+t*P22t._x,y=(1-t)*P21t._y+t*P22t._y, name="")
        return (P0, P11t, P21t, P31t),(P31t, P22t, P13t, P3)            
        
     def get_curve_distance(self, src, P1, P2, dst):
        assert isinstance(src, Point)
        assert isinstance(dst, Point)
        assert isinstance(P1, Point)
        assert isinstance(P2, Point)
        l = self.get_distance(src,dst)
        points = self.courbe_bezier_3([src,P1,P2,dst],l*10)
        res = 0
        for point in range(0, len(points)-1):
            res += self.get_distance(points[point], points[point+1])
        return res
        

     def draw_line(self, group, src, dst, svgId, thickness, drawExtrem=True):
        assert isinstance(src, Point)
        assert isinstance(dst, Point)
        line = self._svg_file.line(start = (src._x*PXCM*cm, src._y*PXCM*cm), 
                                   end = (dst._x*PXCM*cm, dst._y*PXCM*cm), 
                                   id = str(src._name)+str(dst._name)+str(svgId)) 
        line['class'] = str(self._strokes[svgId]) + " " + str(thickness)
        group.add(line)
        if drawExtrem:
            if not src._drawn: 
                self.draw_point(group, src)
            if not dst._drawn: 
                self.draw_point(group, dst)
                
     def compute_curve_from_to_through(self, pFrom, pThrough, pTo, t, pFromCoeffA, pFromCoeffB, svgId, svgStroke):
        assert isinstance(pFrom, Point)
        assert isinstance(pTo, Point)
        assert isinstance(pThrough, Point)

        P2y = pTo._y
        P1y = (pThrough._y - pFrom._y*(1-t)**3 - 3*P2y*t**2*(1-t) - pTo._y*t**3) / (3*t*(1-t)**2)
        P1x = (pFrom._x * (1+pFromCoeffA**2) + pFromCoeffA*pFromCoeffB - pFromCoeffA*P1y)
        P2x = (pThrough._x - pFrom._x*(1-t)**3 - 3*P1x*t*(1-t)**2 - pTo._x*t**3) / (3*t**2*(1-t))
        bezier = My_CubicBezier(P1 = pFrom, C1 = Point(x=P1x,y=P1y), C2 = Point(x=P2x,y=P2y), P2 = pTo)
        dist = pattern.get_curve_distance(pFrom, Point(x=P1x, y=P1y), Point(x=P2x, y=P2y), pTo)
        return bezier, dist

     def draw_point(self, group, src, svgColor='red'):
        assert isinstance(src, Point)
        subgroup = group.add(self._svg_file.g(id=group.get_id()+"spot"+src._name))
        subgroup.add(self._svg_file.circle(center=(src._x*PXCM*cm, src._y*PXCM*cm), r=str(0.03*PXCM)+'cm', fill='red'))
        subgroup.add(self._svg_file.text(src._name, insert=((src._x+0.1)*PXCM*cm, (src._y-0.1)*PXCM*cm), fill='black'))
        src._drawn = True

     def compute_front_neckline_base_curve(self):
        # front
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lback'],pattern._points['Iback'])
        bh = pattern._points['Bback']._x-pattern._points['Hback']._x;
        delta = 0.1*bh
        self._front_neckline_base_curve = My_CubicBezier(P1 = self._points['Cfront'],
                              C1 = Point(x=0.2*self._points['Cfront']._x+0.8*self._points['Jfront']._x,y=self._points['Jfront']._y),
                              C2 = Point(x=self._points['Ifront']._x+delta,y=self._points['Ifront']._y-delta/equaLIa), 
                              P2 = self._points['Ifront'])        

     def compute_back_neckline_base_curve(self):
         # back
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lback'],pattern._points['Iback'])
        bh = pattern._points['Bback']._x-pattern._points['Hback']._x;
        delta = 0.02*bh
        self._back_neckline_base_curve = My_CubicBezier(P1 = self._points['Bback'],
                              C1 = Point(x=0.1*self._points['Bback']._x+0.9*self._points['Hback']._x,y=self._points['Hback']._y),
                              C2 = Point(x=self._points['Iback']._x+delta,y=self._points['Iback']._y-delta/equaLIa), 
                              P2 = self._points['Iback'])        

     def compute_front_neckline_bodice_adjustement_curve(self):
        # front
        self._points['Cbafront'] = Point(x=0, y=0.75, name = "C'") + self._points['Cfront']
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lfront'],pattern._points['Ifront'])
        angle = math.atan(equaLIa)
        # cos(angle) = dx/0.25cm
        # sin(angle) = dy/0.25cm
        dx = 0.25*math.cos(angle)
        dy = 0.25*math.sin(angle)
        self._points['Ibafront'] = Point(x=-dx, y=-dy, name = "") + self._points['Ifront']
        bh = pattern._points['Cbafront']._x-pattern._points['Ibafront']._x;
        delta = 0.1*bh
        self._front_neckline_bodice_adjustement_curve = My_CubicBezier(P1 = self._points['Cbafront'],
                              C1 = Point(x=0.2*self._points['Cbafront']._x+0.8*self._points['Ibafront']._x,y=self._points['Cbafront']._y),
                              C2 = Point(x=self._points['Ibafront']._x+delta,y=self._points['Ibafront']._y-delta/equaLIa), 
                              P2 = self._points['Ibafront'])        
        
     def compute_back_neckline_bodice_adjustement_curve(self):
        # back
        self._points['Bbaback'] = Point(x=0, y=0.1, name = "Bb") + self._points['Bback']
        equaLIa,equaLIb = pattern.get_equation_line(self._points['Lback'],self._points['Iback'])
        angle = math.atan(equaLIa)
        # cos(angle) = dx/0.25cm
        # sin(angle) = dy/0.25cm
        dx = 0.25*math.cos(angle)
        dy = 0.25*math.sin(angle)
        self._points['Ibaback'] = Point(x=-dx, y=-dy, name = "Ib") + self._points['Iback']
        bh = pattern._points['Bbaback']._x-pattern._points['Ibaback']._x;
        delta = 0.02*bh
        self._back_neckline_bodice_adjustement_curve = My_CubicBezier(P1 = self._points['Bbaback'],
                              C1 = Point(x=0.2*self._points['Bbaback']._x+0.8*self._points['Ibaback']._x,y=self._points['Bbaback']._y),
                              C2 = Point(x=self._points['Ibaback']._x+delta,y=self._points['Ibaback']._y-delta/equaLIa), 
                              P2 = self._points['Ibaback'])        

     def compute_back_armhole_base_curve(self):
         # back
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lback'],pattern._points['Iback'])
        path, dist = self.compute_curve_from_to_through(self._points['Lback'], self._points['Mback'], self._points['E'], 0.5, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        self._back_armhole_base_curve = path
        self._armhole_back_measurement = dist
        
     def compute_front_armhole_base_curve(self):
         # front
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lfront'],pattern._points['Ifront'])
        path, dist = self.compute_curve_from_to_through(self._points['Lfront'], self._points['Nfront'], self._points['E'], 0.5, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        self._front_armhole_base_curve = path
        self._armhole_front_measurement = dist

     def compute_front_armhole_bodice_adjustement_curve(self):
        # front
        self._points['Nbafront'] = Point(x=-0.75, y=0, name = "Nb") + self._points['Nfront']

        # Underarm side seam adjustement
        self._points['Ebafront'] = Point(x=-1.75, y=1.5, name = "Eb") + self._points['E']

        # armhole curve redesign
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lfront'],pattern._points['Ifront'])
        path, dist = self.compute_curve_from_to_through(self._points['Lbafront'], self._points['Nbafront'], self._points['Ebafront'], 0.5, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        self._front_armhole_bodice_adjustement_curve = path
        self._armhole_front_measurement = dist


     def compute_back_armhole_bodice_adjustement_curve(self):
        # back
        self._points['Mbaback'] = Point(x=-0.75, y=0, name = "Mb") + self._points['Mback']

        # Underarm side seam adjustement
        self._points['Ebaback'] = Point(x=-1.75, y=1.5, name = "Eb") + self._points['E']

        # armhole curve redesign
        equaLIa,equaLIb = pattern.get_equation_line(pattern._points['Lback'],pattern._points['Iback'])
        path, dist = self.compute_curve_from_to_through(self._points['Lbaback'], self._points['Mbaback'], self._points['Ebaback'], 0.5, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        self._back_armhole_bodice_adjustement_curve = path
        self._armhole_back_measurement = dist

     def compute_front_waist_base_curve(self):
        P1 = Point(x=pattern._points['Dfront']._x+2, y=pattern._points['Dfront']._y)
        P2 = Point(x=pattern._points['Afront']._x-5, y=pattern._points['Afront']._y)
        self._front_waist_base_curve = My_CubicBezier(P1 = pattern._points['Dfront'], C1 = P1, C2 = P2, P2 = pattern._points['Afront'])
        self._front_waist_base_curve_lenght = self.get_curve_distance(pattern._points['Dfront'], P1, P2, pattern._points['Afront'])

     def compute_front_waist_bodice_adjustement_curve(self):
        # Waist adjustement
        self._points['Dbafront'] = Point(x=-1.5, y=0, name = "D2b") + self._points['Dfront']
        P1 = Point(x=pattern._points['Dbafront']._x+2, y=pattern._points['Dbafront']._y)
        P2 = Point(x=pattern._points['Afront']._x-5, y=pattern._points['Afront']._y)
        self._front_waist_bodice_adjustement_curve = My_CubicBezier(P1 = pattern._points['Dbafront'], C1 = P1, C2 = P2, P2 = pattern._points['Afront'])
        self._front_waist_bodice_adjustement_curve_lenght = self.get_curve_distance(pattern._points['Dbafront'], P1, P2, pattern._points['Afront'])

     def compute_back_waist_bodice_adjustement_curve(self):
        # Waist adjustement
        self._points['Dbaback'] = Point(x=0-1.5, y=0, name = "Db") + self._points['Dback']

     def compute_front_shoulderline_bodice_adjustement_line(self):
        # Shoulder line adjustement
        equaLIa,equaLIb = pattern.get_equation_line(self._points['Lfront'],self._points['Ifront'])
        angle = math.atan(equaLIa)
        dx = 0.5*math.cos(angle)
        dy = 0.5*math.sin(angle)
        self._points['Lbafront'] = Point(x=-dx, y=-dy, name = "") + self._points['Lfront']

     def compute_back_shoulderline_bodice_adjustement_line(self):
        # Shoulder line adjustement
        equaLIa,equaLIb = pattern.get_equation_line(self._points['Lfront'],self._points['Ifront'])
        angle = math.atan(equaLIa)
        dx = 0.5*math.cos(angle)
        dy = 0.5*math.sin(angle)
        self._points['Lbaback'] = Point(x=-dx, y=-dy, name = "Lb") + self._points['Lback']

     def draw_bodice_adjustement_line_and_curves_back(self):
        g = self._areas["BackAreaBodiceEnlargement"]
        pattern.compute_back_neckline_bodice_adjustement_curve()
        pattern.compute_back_shoulderline_bodice_adjustement_line()
        pattern.compute_back_armhole_bodice_adjustement_curve()
        pattern.compute_back_waist_bodice_adjustement_curve()
        line1 = My_Line(P1=self._points['A'], P2=self._points['Bbaback'])        
        line2 = My_Line(P1=self._points['Ibaback'], P2=self._points['Lbaback'])  
        line3 = My_Line(P1=self._points['Ebaback'], P2=self._points['Dbaback'])  
        line4 = My_Line(P1=self._points['Dbaback'], P2=self._points['A'])  
        paths = My_Path(line1,self._back_neckline_bodice_adjustement_curve,line2, self._back_armhole_bodice_adjustement_curve,line3,line4, closed=True)
        path = self._svg_file.path(d=(paths.d()),
                                      id = g.get_id() + "Curve", 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + 'base'
        g.add(path)
        self.draw_line(g, self._points['G'], self._points['Mbaback'], curStatureIdx, 'thin')

        for pointKey, pointValue in self._points.items():
            if "baback" in pointKey:
                self.draw_point(pattern._areas["BackAreaBodiceEnlargementPoints"], pointValue)
        
     def draw_bodice_adjustement_line_and_curves_front(self):
        g = self._areas["FrontAreaBodiceEnlargement"]
        pattern.compute_front_neckline_bodice_adjustement_curve()
        pattern.compute_front_shoulderline_bodice_adjustement_line()
        pattern.compute_front_armhole_bodice_adjustement_curve()
        pattern.compute_front_waist_bodice_adjustement_curve()
        line1 = My_Line(P1=self._points['A'], P2=self._points['Cbafront'])        
        line2 = My_Line(P1=self._points['Ibafront'], P2=self._points['Lbafront'])  
        line3 = My_Line(P1=self._points['Ebafront'], P2=self._points['Dbafront'])  
        line4 = My_Line(P1=self._points['Afront'], P2=self._points['A'])  
        paths = My_Path(line1,self._front_neckline_bodice_adjustement_curve,line2, self._front_armhole_bodice_adjustement_curve,line3, self._front_waist_bodice_adjustement_curve, line4, closed=True)
        path = self._svg_file.path(d=(paths.d()),
                                      id = g.get_id() + "Curve", 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + 'base'
        g.add(path)
        self.draw_line(g, self._points['A'], self._points['Dbafront'], curStatureIdx, 'thin')
        self.draw_line(g, self._points['G'], self._points['Nbafront'], curStatureIdx, 'thin')

        for pointKey, pointValue in self._points.items():
            if "bafront" in pointKey:
                self.draw_point(pattern._areas["FrontAreaBodiceEnlargementPoints"], pointValue)

     def draw_abdomen_adjustement(self, group, curStatureIdx, thickness):
        equaLIa,equaLIb = pattern.get_equation_line(pattern._pointL2,pattern._pointI2)
        angle = math.atan(equaLIa)
        # cos(angle) = dx/2cm
        # sin(angle) = dy/2cm
        dx = 2*math.cos(angle)
        dy = 2*math.sin(angle)
        #self._pointAAA = Point(x=self._pointL2._x-dx, y=self._pointL2._y-dy-0.5, name = "AAA")
        #self._pointI2AA = Point(x=self._pointI2._x, y=self._pointI2._y-1.5, name = "I2AA")
        #self._pointCAA = Point(x=self._points['C']_x, y=self._points['C']_y-1.5, name = "CAA")
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
        self._pointLCE = Point(x=self._pointL._x-2*dx, y=self._pointL._y-2*dy, name = "Lc")
        self._pointICE = Point(x=self._pointI._x-dx, y=self._pointI._y-dy, name = "Ic")
        self._pointBCE = Point(x=self._pointB._x, y=self._pointB._y+0.5, name = "Bc")
        self.draw_line(group, self._pointLCE, self._pointICE, curStatureIdx, thickness)
        pathStr = 'M ' + str(self._pointICE._x*CMPX) + ',' + str(self._pointICE._y*CMPX)
        bh = pattern._pointB._x-pattern._pointH._x
        delta = 0.02*bh
        P0 = Point(x=self._pointICE._x+delta, y=self._pointICE._y-delta/equaLIa)
        P1 = Point(x=0.1*self._pointBCE._x+0.9*self._pointICE._x, y=self._pointBCE._y)
        P2 = self._pointBCE
        self._backNecklinePath = np.array((self._pointICE, P0, P1, P2))
        pathStr += ' C ' + str(P0._x*CMPX) + ',' + str(P0._y*CMPX)
        pathStr += ' ' + str(P1._x*CMPX) + ',' + str(P1._y*CMPX)
        pathStr += ' ' +   str(P2._x*CMPX) + ',' + str(P2._y*CMPX)  
        path = self._svg_file.path(d=(pathStr),
                                      id = "curve"+str(self._pointI._name)+str(self._pointB._name)+str(curStatureIdx), 
                                      stroke = self._strokes[curStatureIdx], 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
        group.add(path)
        self._pointMCE = Point(x=self._pointM._x-2.5, y=self._pointM._y, name = "ME")
        self._pointECE = Point(x=self._pointE._x-4.75, y=self._pointE._y+4.5, name = "EE")
        self._pointACE = Point(x=self._pointA._x, y=self._pointA._y+2, name = "AE")
        self._pointD2CE = Point(x=self._pointD2._x-4.75, y=self._pointD2._y+2, name = "D2E")
        self.draw_line(group, self._pointECE, self._pointD2CE, curStatureIdx, 'base')
        self.draw_line(group, self._pointD2CE, self._pointACE, curStatureIdx, thickness)
        self.draw_line(group, self._pointBCE, self._pointACE, curStatureIdx, thickness)
        self.draw_line(group, self._pointMCE, self._pointM, curStatureIdx, 'base')
        
        path = self.compute_curve_from_to_through(self._pointLCE, self._pointMCE, self._pointECE, 0.4, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
            
     def draw_coat_enlargement_front(self, group, curStatureIdx, thickness):
        self._pointCCE = Point(x=self._pointCAA._x, y=self._pointCAA._y+2, name = "Cc")
        longueurepauldos = self.get_distance(self._pointICE, self._pointLCE)
        equaLIa,equaLIb = pattern.get_equation_line(pattern._pointAAA,pattern._pointI2AA)
        angle = math.atan(equaLIa)
        dx = math.cos(angle)
        dy = math.sin(angle)
        self._pointI2CE = Point(x=self._pointAAA._x+dx*longueurepauldos, y=self._pointAAA._y+dy*longueurepauldos, name = "I2c")
        self.draw_line(group, self._pointI2CE, self._pointAAA, curStatureIdx, thickness)
        pathStr = 'M ' + str(self._pointI2CE._x*CMPX) + ',' + str(self._pointI2CE._y*CMPX)
        bh = pattern._pointB._x-pattern._pointH._x;
        delta = 0.1*bh
        P0 = Point(x=self._pointI2CE._x+delta, y=self._pointI2CE._y-delta/equaLIa)
        P1 = Point(x=0.2*self._pointCCE._x+0.8*self._pointJ._x, y=self._pointCCE._y)
        P2 = Point(x=self._pointCCE._x, y=self._pointCCE._y)
        self._frontNecklinePath = np.array((self._pointI2CE, P0, P1, P2))
        pathStr += ' C ' + str(P0._x*CMPX) + ',' + str(P0._y*CMPX)
        pathStr += ' ' + str(P1._x*CMPX) + ',' + str(P1._y*CMPX)
        pathStr += ' ' +   str(P2._x*CMPX) + ',' + str(P2._y*CMPX)  
        path = self._svg_file.path(d=(pathStr),
                                      id = "curve"+str(self._pointI2CE._name)+str(self._pointCCE._name)+str(curStatureIdx), 
                                      stroke = self._strokes[curStatureIdx], 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
        group.add(path)
        self._pointNCE = Point(x=self._pointN._x-2.5, y=self._pointN._y, name = "NE")
        self._pointECE = Point(x=self._pointE._x-4.75, y=self._pointE._y+4.5, name = "EE")
        self._pointACE = Point(x=self._pointA._x, y=self._pointA._y+2, name = "AE")
        self._pointD2CE = Point(x=self._pointD2._x-4.75, y=self._pointD2._y+2, name = "D2E")
        self.draw_line(group, self._pointECE, self._pointD2CE, curStatureIdx, 'base')
        self.draw_line(group, self._pointD2CE, self._pointACE, curStatureIdx, thickness)
        #self.draw_line(group, self._pointBCE, self._pointACE, curStatureIdx, thickness)
        self.draw_line(group, self._pointNCE, self._pointN, curStatureIdx, 'base')
        
        path = self.compute_curve_from_to_through(self._pointLCE, self._pointNCE, self._pointECE, 0.4, equaLIa, equaLIb, curStatureIdx, self._strokes[curStatureIdx])
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)

     def draw_waist_line(self, group, curStatureIdx, thickness):
        self._pointW1 = Point(x=self._pointACE._x, y=self._pointACE._y+self._waist_to_hips[curStatureIdx], name = "W1")
        self._pointW2 = Point(x=self._pointACE._x-0.25*self._hips_measurement[curStatureIdx]-5, y=self._pointACE._y+self._waist_to_hips[curStatureIdx], name = "W2")
        self.draw_line(group, self._pointW1, self._pointW2, curStatureIdx, thickness)
        self.draw_line(group, self._pointW1, self._pointACE, curStatureIdx, thickness)
        self.draw_line(group, self._pointW2, self._pointD2CE, curStatureIdx, 'base')
        delta = self.get_distance(self._pointW2, self._pointD2CE)
        P1 = Point(x=self._pointD2CE._x, y=self._pointD2CE._y-0.2*delta)
        P2 = Point(x=self._pointD2CE._x, y=self._pointD2CE._y+0.2*delta)
        pathStr = 'M ' + str(self._pointECE._x*CMPX) + ',' + str(self._pointECE._y*CMPX)
        pathStr += ' C ' + str(P1._x*CMPX) + ',' + str(P1._y*CMPX)
        pathStr += ' ' +   str(P1._x*CMPX) + ',' + str(P1._y*CMPX)  
        pathStr += ' ' +   str(self._pointD2CE._x*CMPX) + ',' + str(self._pointD2CE._y*CMPX) 
        path = self._svg_file.path(d=(pathStr),
                                      id = "curve"+str(self._pointECE._name)+str(self._pointD2CE._name)+str(curStatureIdx), 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
        group.add(path)
        pathStr = 'M ' + str(self._pointD2CE._x*CMPX) + ',' + str(self._pointD2CE._y*CMPX)
        pathStr += ' C ' + str(P2._x*CMPX) + ',' + str(P2._y*CMPX)
        pathStr += ' ' +   str(P2._x*CMPX) + ',' + str(P2._y*CMPX)  
        pathStr += ' ' +   str(self._pointW2._x*CMPX) + ',' + str(self._pointW2._y*CMPX) 
        path = self._svg_file.path(d=(pathStr),
                                      id = "curve"+str(self._pointD2CE._name)+str(self._pointW2._name)+str(curStatureIdx), 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
        group.add(path)
        #self.compute_curve_from_to_through(self._pointECE, self._pointD2CE, self._pointW2, 0.4, 0, 0, curStatureIdx, self._strokes[curStatureIdx], self._svg_stroke_width_bold)

     def draw_croisure(self, group, curStatureIdx, thickness):
        delta = 0.02*self._hips_measurement[curStatureIdx]
        self._pointW1croisure = Point(x=self._pointW1._x+delta, y=self._pointW1._y, name = "Wc")
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
        self._pointCcroisure = Point(x=self._pointCCE._x+delta, y=Pty, name = "Cc")
        
        (P0,P11t,P21t,P31t),(P31t,P22t,P13t,P3) = self.get_sub_curves(self._frontNecklinePath[0], self._frontNecklinePath[1], self._frontNecklinePath[2], self._frontNecklinePath[3], tReal)
        
        pathStr = 'M ' + str(self._pointW1croisure._x*CMPX) + ',' + str(self._pointW1croisure._y*CMPX)
        pathStr += ' V ' + str(self._pointCcroisure._y*CMPX)
        pathStr += ' C' +  str((2*self._frontNecklinePath[3]._x-P22t._x)*CMPX) + "," + str(P22t._y*CMPX)
        pathStr += ' ' +  str((2*self._frontNecklinePath[3]._x-P13t._x)*CMPX) + "," + str(P13t._y*CMPX)
        pathStr += ' ' +  str(self._frontNecklinePath[3]._x*CMPX) + "," + str(self._frontNecklinePath[3]._y*CMPX)  
        pathStr += ' V ' + str(self._pointW1._y*CMPX)
        pathStr += ' Z'  
        path = self._svg_file.path(d=(pathStr),
                                      id = "curvecroisure"+str(curStatureIdx), 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
        group.add(path)
        
        # button
        self._pointButton = Point(x=self._pointW1._x,y=self._pointECE._y, name="Button")

     def draw_tailored_collar(self, collarBandWidth, upperCollarWidth, group, curStatureIdx, thickness):
        self._pointButtonCroisure = Point(x = self._pointW1._x, y = self._pointButton._y - 1, name="ButtonC")
        self.draw_point(group, self._pointButtonCroisure)
        self._pointCollarBandWidthCenterBack = Point(x = self._pointBCE._x, y = self._pointBCE._y - collarBandWidth, name="Bcbw")
        self._pointCollarBandWidthCenterUpperBack = Point(x = self._pointCollarBandWidthCenterBack._x, y = self._pointCollarBandWidthCenterBack._y + upperCollarWidth, name="Bcbw")
        self._pointCollarKBack = Point(x = self._pointCollarBandWidthCenterBack._x, y = self._pointCollarBandWidthCenterBack._y - collarBandWidth, name="K")
        if group is self._areas["backArea"]:
            self.draw_line(group, self._pointCollarBandWidthCenterBack, self._pointBCE, curStatureIdx, 'base')
        equaShoulderFrontA,equaShoulderFrontB = pattern.get_equation_line(pattern._pointLCE,pattern._pointI2CE)
        angleFront = math.atan(equaShoulderFrontA)
        dx,dy = collarBandWidth*math.cos(-angleFront),collarBandWidth*math.sin(-angleFront)
        self._pointFrontCollarBandWidthShoulderLine = Point(x = self._pointI2CE._x+dx, y = self._pointI2CE._y+dy, name="Icbwf")
        self._pointFrontCollarK2Back = Point(x = self._pointI2CE._x+2*dx, y = self._pointI2CE._y+2*dy, name="K2f")
        if group is self._areas["frontArea"]:
            self.draw_line(group, self._pointFrontCollarBandWidthShoulderLine, self._pointI2CE, curStatureIdx, 'base')
            self.draw_line(group, self._pointFrontCollarBandWidthShoulderLine, self._pointButtonCroisure, curStatureIdx, thickness)
        equaShoulderBackA,equaShoulderBackB = self.get_equation_line(self._pointLCE, self._pointICE)
        angleBack = math.atan(equaShoulderBackA)
        angle = -2*angleFront-angleBack
        self._pointBackCollarBandWidthShoulderLine = Point(x = self._pointICE._x+collarBandWidth*math.cos(angle), y = self._pointICE._y-collarBandWidth*math.sin(angle), name="Icbwb")
        self._pointBackCollarK2 = Point(x = self._pointICE._x+2*collarBandWidth*math.cos(angle), y = self._pointICE._y-2*collarBandWidth*math.sin(angle), name="K2b")
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
            
            pathStr = 'M ' + str(self._pointBackCollarBandWidthShoulderLine._x*CMPX) + ',' + str(self._pointBackCollarBandWidthShoulderLine._y*CMPX)
            pathStr += ' C' +  str((P11t._x+self._pointBackCollarBandWidthShoulderLine._x-self._pointICE._x)*CMPX) + "," + str((P11t._y-collarBandWidth)*CMPX)
            pathStr += ' ' +  str((P21t._x+self._pointBackCollarBandWidthShoulderLine._x-self._pointICE._x)*CMPX) + "," + str((P21t._y-collarBandWidth)*CMPX)
            pathStr += ' ' +  str((P31t._x+self._pointBackCollarBandWidthShoulderLine._x-self._pointICE._x)*CMPX) + "," + str((P31t._y-collarBandWidth)*CMPX)
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
            
            pathStr = 'M ' + str(self._pointBackCollarK2._x*CMPX) + ',' + str(self._pointBackCollarK2._y*CMPX)
            pathStr += ' C' +  str((P11t._x+self._pointBackCollarK2._x-self._pointICE._x)*CMPX) + "," + str((P11t._y-2*collarBandWidth)*CMPX)
            pathStr += ' ' +  str((P21t._x+self._pointBackCollarK2._x-self._pointICE._x)*CMPX) + "," + str((P21t._y-2*collarBandWidth)*CMPX)
            pathStr += ' ' +  str((P31t._x+self._pointBackCollarK2._x-self._pointICE._x)*CMPX) + "," + str((P31t._y-2*collarBandWidth)*CMPX)
            path = self._svg_file.path(d=(pathStr),
                                          id = "curvecroisure"+str(curStatureIdx), 
                                          stroke_linejoin = 'round',
                                          fill = 'none')
            path['class'] = str(self._strokes[curStatureIdx]) + " " + str(thickness)
            group.add(path)
            
     def compute_armhole_depth(self):
            # Translate front and back area to the same armpits point
            self._areas["FrontArea"].scale(-1,1)
            self._areas["FrontArea"].translate((pattern._points["Efront"]._x)*-CMPX,(pattern._points["Efront"]._y)*-CMPX)
            self._areas["BackArea"].translate((pattern._points["Eback"]._x)*-CMPX,(pattern._points["Eback"]._y)*-CMPX)
            vectELxFront = -0.5 * (pattern._points["Efront"]._x - pattern._points["Lfront"]._x)             
            vectELyFront = -0.5 * (pattern._points["Efront"]._y - pattern._points["Lfront"]._y)            
            vectELxBack = -0.5 * (pattern._points["Eback"]._x - pattern._points["Lback"]._x)             
            vectELyBack = -0.5 * (pattern._points["Eback"]._y - pattern._points["Lback"]._y)            
            self._points['CenterShoulderTips'] = pattern._points["Eback"] + Point(x=vectELxBack, y=vectELyBack) + Point(x=-vectELxFront, y=vectELyFront)
            self._armehole_depth = pattern.get_distance(self._points['CenterShoulderTips'], self._points["Efront"])

     def draw_sleeve(self, bracelet = 0):
        subsSleeve = dict()
        subsSleeveIds = ["AllSpots","BackSleeve","FrontSleeve","CenterSleeve"]
        for dummy,x in enumerate(subsSleeveIds):
            subsSleeve[x] = pattern._svg_file.g(id=self._areas["sleeveArea"].get_id() + str(x))
            self._areas["sleeveArea"].add(subsSleeve[x])

        armhole_measurement = self._armhole_back_measurement + self._armhole_front_measurement 

        self._points['SA'] = Point(x=0, y=0, name="SA")
        self._points['SB'] = Point(x=0, y=4.0/5.0*self._armehole_depth, name="SB") + self._points["SA"]
        ab = self.get_distance(self._points["SA"], self._points["SB"])
        self._points['SC'] = Point(x=-2.0/5.0*armhole_measurement, y=0, name="SC") + self._points["SB"]
        self._points['SD'] = Point(x=2.0/5.0*armhole_measurement, y=0, name="SD") + self._points["SB"]
        self.draw_line(self._areas["sleeveArea"], self._points['SC'], self._points['SD'], curStatureIdx, 'base')
        self._points['SE'] = Point(x=-1.0/5.0*armhole_measurement, y=0, name="SE") + self._points["SB"]
        self._points['SF'] = Point(x=1.0/5.0*armhole_measurement, y=0, name="SF") + self._points["SB"]
        self._points['SG'] = Point(x=0, y=self._arm_lenght[curStatureIdx]-bracelet, name="SG") + self._points["SA"]
        self.draw_line(self._areas["sleeveArea"], self._points['SA'], self._points['SG'], curStatureIdx, 'base')
        self._points['SC2'] = Point(x=self._points["SC"]._x, y=self._points["SG"]._y, name="SC'")
        self._points['SD2'] = Point(x=self._points["SD"]._x, y=self._points["SG"]._y, name="SD'")
        self.draw_line(self._areas["sleeveArea"], self._points['SC'], self._points['SC2'], curStatureIdx, 'base')
        self.draw_line(self._areas["sleeveArea"], self._points['SD'], self._points['SD2'], curStatureIdx, 'base')
        self.draw_line(self._areas["sleeveArea"], self._points['SC2'], self._points['SD2'], curStatureIdx, 'base')
        self._points['SE2'] = Point(x=0, y=-2.0/3.0*ab, name="SE'") + self._points["SE"]
        self._points['SF2'] = Point(x=0, y=-1.0/2.0*ab, name="SF'") + self._points["SF"]
        self._points['SF2down'] = Point(x=self._points["SF2"]._x, y=self._points["SD2"]._y, name="SF2d") 
        self._points['SE2down'] = Point(x=self._points["SE2"]._x,y=self._points["SD2"]._y, name='SE2d')
        #pattern.draw_line(pattern._areas["sleeveArea"], pattern._points['SE'], pattern._points['SE2'], curStatureIdx, 'base')
        #pattern.draw_line(pattern._areas["sleeveArea"], pattern._points['SF'], pattern._points['SF2'], curStatureIdx, 'base')
        
        equaSCE2a,equaSCE2b = self.get_equation_line(self._points["SC"],self._points["SE2"])
        angle = math.atan(-1.0/equaSCE2a)
        dx = 0.75*math.cos(angle)
        dy = 0.75*math.sin(angle)
        self._points['SCE2Creux'] = Point(x=1.0/3.0*(self._points["SE2"]._x-self._points["SC"]._x), y=1.0/3.0*(self._points["SE2"]._y-self._points["SC"]._y), name="SCE2Creux") + Point(x=dx,y=dy) + self._points["SC"]

        equaSF2Aa,equaSF2Ab = self.get_equation_line(self._points["SA"],self._points["SF2"])
        angle = math.atan(-1.0/equaSF2Aa)
        dx = 1.0*math.cos(angle)
        dy = 1.0*math.sin(angle)
        self._points['SAF2Creux'] = Point(x=1.0/2.0*(self._points["SF2"]._x-self._points["SA"]._x), y=1.0/2.0*(self._points["SF2"]._y-self._points["SA"]._y), name="SAF2Creux") + Point(x=dx,y=dy) + self._points["SA"]

        equaSDF2a,equaSDF2b = self.get_equation_line(self._points["SF2"],self._points["SD"])
        angle = math.atan(-1.0/equaSDF2a)
        dx = -1.0*math.cos(angle)
        dy = -1.0*math.sin(angle)
        self._points['SF2DCreux'] = Point(x=1.0/2.0*(self._points["SD"]._x-self._points["SF2"]._x), y=1.0/2.0*(self._points["SD"]._y-self._points["SF2"]._y), name="SF2DCreux") + Point(x=dx,y=dy) + self._points["SF2"]

        P1 = Point(x=self._points["SAF2Creux"]._x + 1.0*math.cos(math.atan(equaSF2Aa)), y=self._points["SAF2Creux"]._y + 1.0*math.sin(math.atan(equaSF2Aa)))
        P2 = Point(x=self._points["SF2DCreux"]._x - 1.0*math.cos(math.atan(equaSF2Aa)), y=self._points["SF2DCreux"]._y - 1.0*math.sin(math.atan(equaSF2Aa)))
        equaSCreuxCreuxa,equaSCreuxCreuxb = self.get_equation_line(P1,P2)

        bezier1 = My_CubicBezier(P1 = self._points['SC'],
                              C1 = Point(x=self._points["SC"]._x+1.0,y=self._points["SC"]._y), 
                              C2 = Point(x=self._points["SCE2Creux"]._x - 1.0*math.cos(math.atan(equaSCE2a)),y=self._points["SCE2Creux"]._y - 1.0*math.sin(math.atan(equaSCE2a))),
                              P2 = self._points['SCE2Creux'])   
        bezier2 = My_CubicBezier(P1 = self._points['SCE2Creux'],
                              C1 = Point(x=self._points["SCE2Creux"]._x + 1.0*math.cos(math.atan(equaSCE2a)),y=self._points["SCE2Creux"]._y + 1.0*math.sin(math.atan(equaSCE2a))), 
                              C2 = Point(x=self._points["SE2"]._x - 1.0*math.cos(math.atan(equaSCE2a)),y=self._points["SE2"]._y - 1.0*math.sin(math.atan(equaSCE2a))),
                              P2 = self._points['SE2'])
        curPath = My_Path(bezier1, bezier2)
        curPath.append(My_Line(P1=self._points["SE2"], P2=self._points['SE2down']))
        curPath.append(My_Line(P1=self._points['SE2down'], P2=self._points["SC2"]))
        curPath.append(My_Line(P1=self._points["SC2"], P2=self._points["SC"]))
        path = self._svg_file.path(d=(curPath.d()),
                                  id = "curve"+str(curStatureIdx), 
                                  stroke_linejoin = 'round',
                                  fill = 'none')
                                     
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str('sleeve')
        subsSleeve["BackSleeve"].add(path)
        subsSleeve["BackSleeve"].rotate(3, [self._points["SE2"]._x*CMPX, self._points["SE2"]._y*CMPX])
        self._points['SC2rot'] = copy.deepcopy(self._points["SC2"]);
        self._points['SC2rot'].rotate(3, self._points["SE2"])
        
        dx = (self._points["SA"]._x-((self._points["SA"]._y-equaSCE2b)/equaSCE2a))
        frontUpCurve1 = My_CubicBezier(P1 = self._points['SE2'],
                              C1 = Point(x=self._points["SE2"]._x + 1.0*math.cos(math.atan(equaSCE2a)),y=self._points["SE2"]._y + 1.0*math.sin(math.atan(equaSCE2a))), 
                              C2 = Point(x=self._points["SA"]._x-dx,y=self._points["SA"]._y),
                              P2 = self._points['SA'])        
        dx = 0.5*(self._points["SAF2Creux"]._x-self._points["SA"]._x)
        frontUpCurve2 = My_CubicBezier(P1 = self._points['SA'],
                              C1 = Point(x=self._points["SA"]._x+dx,y=self._points["SA"]._y), 
                              C2 = Point(x=self._points["SAF2Creux"]._x - 1.0*math.cos(math.atan(equaSF2Aa)),y=self._points["SAF2Creux"]._y - 1.0*math.sin(math.atan(equaSF2Aa))),
                              P2 = self._points['SAF2Creux'])        
        frontUpCurve3 = My_CubicBezier(P1 = self._points['SAF2Creux'],
                              C1 = Point(x=self._points["SAF2Creux"]._x + 1.0*math.cos(math.atan(equaSF2Aa)),y=self._points["SAF2Creux"]._y + 1.0*math.sin(math.atan(equaSF2Aa))), 
                              C2 = Point(x=self._points["SF2"]._x - 1.0*math.cos(math.atan(equaSCreuxCreuxa)),y=self._points["SF2"]._y - 1.0*math.sin(math.atan(equaSCreuxCreuxa))),
                              P2 = self._points['SF2'])        
        frontUpCurve = My_Path(frontUpCurve1, frontUpCurve2, frontUpCurve3)
        frontUpCurve.append(My_Line(P1=self._points["SF2"], P2=self._points["SF2down"]))
        frontUpCurve.append(My_Line(P1=self._points["SF2down"], P2=self._points['SE2down']))
        frontUpCurve.append(My_Line(P1=self._points['SE2down'], P2=self._points["SE2"]))
        path = self._svg_file.path(d=(frontUpCurve.d()),
                                      id = "curve"+str(curStatureIdx), 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str('sleeve')
        subsSleeve["CenterSleeve"].add(path)

        bezier1 = My_CubicBezier(P1 = self._points['SF2'],
                              C1 = Point(x=self._points["SF2"]._x + 1.0*math.cos(math.atan(equaSCreuxCreuxa)),y=self._points["SF2"]._y + 1.0*math.sin(math.atan(equaSCreuxCreuxa))), 
                              C2 = Point(x=self._points["SF2DCreux"]._x - 1.0*math.cos(math.atan(equaSF2Aa)),y=self._points["SF2DCreux"]._y - 1.0*math.sin(math.atan(equaSF2Aa))),
                              P2 = self._points['SF2DCreux'])        
        bezier2 = My_CubicBezier(P1 = self._points['SF2DCreux'],
                              C1 = Point(x=self._points["SF2DCreux"]._x + 1.0*math.cos(math.atan(equaSF2Aa)),y=self._points["SF2DCreux"]._y + 1.0*math.sin(math.atan(equaSF2Aa))), 
                              C2 = self._points["SD"] + Point(x=-dx,y=0),
                              P2 = self._points['SD'])       
        curPath = My_Path(bezier1, bezier2)
        curPath.append(My_Line(P1=self._points["SD"], P2=self._points['SD2']))
        curPath.append(My_Line(P1=self._points['SD2'], P2=Point(x=self._points["SF2"]._x,y=self._points["SD2"]._y)))
        curPath.append(My_Line(P1=Point(x=self._points["SF2"]._x,y=self._points["SD2"]._y), P2=self._points["SF2"]))
        path = self._svg_file.path(d=(curPath.d()),
                                   id = "curve"+str(curStatureIdx), 
                                   stroke_linejoin = 'round',
                                   fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str('sleeve')
        subsSleeve["FrontSleeve"].add(path)
        subsSleeve["FrontSleeve"].rotate(-3, [self._points["SF2"]._x*CMPX, self._points["SF2"]._y*CMPX])
        self._points['SD2rot'] = copy.deepcopy(self._points["SD2"]);
        self._points['SD2rot'].rotate(-3, self._points["SF2"])
        
        downPath = My_Path()
        downLine = My_Line(P1=self._points["SC2rot"], P2=self._points['SD2rot'])
        maxt=6
        for t in range(1,maxt+1):
            downPath.append(My_Line(P1=Point(c=downLine._line.point((t-1)/float(maxt))), P2=Point(c=downLine._line.point(t/float(maxt)))))
        path = self._svg_file.path(d=downPath.d(),
                                   id = "curve"+str(curStatureIdx), 
                                   stroke_linejoin = 'round',
                                   fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str('sleeve')
        subsSleeve["CenterSleeve"].add(path)

        dp = Point(x=self._points["SF2"]._x,y=self._points["SD2"]._y) - self._points['SA']
        dirpm = Point(x=0.5*dp._x,y=-0.5*dp._y)
        dirmm = Point(x=-0.5*dp._x,y=-0.5*dp._y)
        dirpp = Point(x=0.5*dp._x,y=0.5*dp._y)
        dirmp = Point(x=-0.5*dp._x,y=0.5*dp._y)
        bezier1 = My_CubicBezier(P1 = self._points['SA'],
                              C1 = self._points['SA'] + dirpp,
                              C2 = Point(x=self._points["SF2"]._x,y=self._points["SD2rot"]._y) + dirpm,
                              P2 = Point(x=self._points["SF2"]._x,y=self._points["SD2rot"]._y))   
        bezier2 = My_CubicBezier(P1 = Point(x=self._points["SF2"]._x,y=self._points["SD2rot"]._y),
                              C1 = Point(x=self._points["SF2"]._x,y=self._points["SD2rot"]._y) + dirmm,
                              C2 = self._points['SA'] + dirmp,
                              P2 = self._points['SA'])   
        #path = self._svg_file.path(d=(My_Path(bezier1._cubicbezier, bezier1._cubicbezier.rotated(180, self._points['SA'].toRI()).translated(dp.toRI())).d()),
        path = self._svg_file.path(d=(My_Path(bezier1, bezier2, closed=True).d()),
                                      id = "curve"+str(curStatureIdx), 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str('sleeve')
        subsSleeve["CenterSleeve"].add(path)
        
        
        PSAtleft = self._points['SA'] - Point(x=2,y=0);
        PSAtright = self._points['SA'] + Point(x=2,y=0);
        PSBtleft = Point(x=self._points["SF2"]._x,y=self._points["SD2rot"]._y) - Point(x=2,y=0);
        PSBtright = Point(x=self._points["SF2"]._x,y=self._points["SD2rot"]._y) + Point(x=2,y=0);        
        bezier3 = My_CubicBezier(P1 = PSAtleft,
                              C1 = PSAtleft + dirmp,
                              C2 = PSBtleft + dirmm,
                              P2 = PSBtleft)   
        (T1,T2) = bezier3._cubicbezier.intersect(frontUpCurve1._cubicbezier)[0]
        (sub1bezier3,sub2bezier3) = bezier3.split(T1)
        (sub1frontUpCurve1,sub2frontUpCurve1) = frontUpCurve1.split(T2)
        bezier4 = My_CubicBezier(P1 = PSBtright,
                              C1 = PSBtright + dirpm,
                              C2 = PSAtright + dirpp,
                              P2 = PSAtright) 
        (T1,T2) = bezier4._cubicbezier.intersect(frontUpCurve2._cubicbezier)[0]
        (sub1bezier4,sub2bezier4) = bezier4.split(T1)
        (sub1frontUpCurve2,sub2frontUpCurve2) = frontUpCurve2.split(T2)
        
        line2 = My_Line(P1 = PSBtleft, P2 = PSBtright)
        #path = self._svg_file.path(d=(My_Path(sub2bezier3._cubicbezier, line2._line, sub1bezier4._cubicbezier, sub1frontUpCurve2._cubicbezier, sub2frontUpCurve1._cubicbezier, closed=False).d()),
        path = self._svg_file.path(d=(My_Path(sub2bezier3, line2, sub1bezier4, sub1frontUpCurve2, sub2frontUpCurve1, closed=True).d()),
                                      id = "curve"+str(curStatureIdx), 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + str('sleeve')
        subsSleeve["CenterSleeve"].add(path)
        
     def place_base_points(self):
        # Base, points
        self._points['A'] = Point(x=0, y=0, name="A")
        self._points['Bback'] = Point(x=0, y=-pattern._back_waist_lenght[curStatureIdx], name = "B") + pattern._points['A'] 
        self._points['Cfront'] = Point(x=0, y=-(pattern._front_waist_lenght[curStatureIdx]-1.25), name = "C") + pattern._points['A'] 
        self._points['Dback'] = Point(x=-0.25*pattern._bust_measurement[curStatureIdx], y=0, name = "D") + pattern._points['A'] 
        self._points['E'] = Point(x=0, y=-0.25*(pattern._back_waist_lenght[curStatureIdx]+pattern._front_waist_lenght[curStatureIdx]), name = "E") + pattern._points['Dback'] 
        self._points['F'] = Point(x=pattern._points['A']._x, y=pattern._points['E']._y, name="F")
        self._points['G'] = Point(x=0.5*(pattern._points['F']._x+pattern._points['Cfront']._x), y=0.5*(pattern._points['F']._y+pattern._points['Cfront']._y), name = "G")
        self._points['Hback'] = Point(x=-(0.8+pattern._neckline_measurement[curStatureIdx]/6), y=0, name = "H") + pattern._points['Bback']
        self._points['Iback'] = Point(x=0, y=-(0.25*(pattern._points['Bback']._x-pattern._points['Hback']._x)), name = "I") + pattern._points['Hback']
        self._points['Jfront'] = Point(x=pattern._points['Hback']._x, y=pattern._points['Cfront']._y, name = "J")
        self._points['Kback'] = Point(x=pattern._points['Hback']._x, y=pattern._points['Jfront']._y+(pattern._points['Iback']._y-pattern._points['Jfront']._y)/3.0, name = "K")
        #IL**2 = IL**2 + KL**2
        kl = math.sqrt(pattern._shoulder_lenght[curStatureIdx]**2-(pattern._points['Iback']._y-pattern._points['Kback']._y)**2)
        self._points['Lback'] = Point(x=-kl, y=0, name = "L") + pattern._points['Kback']
        self._points['Mback'] = Point(x=-0.5*pattern._crossback_measurement[curStatureIdx], y=0, name = "M") + pattern._points['G']
        self._points['Nfront'] = Point(x=-0.5*pattern._crossfront_measurement[curStatureIdx], y=0, name = "N") + pattern._points['G']
        self._points['Ifront'] = Point(x=0, y=0.5, name = "I'") + pattern._points['Iback']
        self._points['Lfront'] = Point(x=0, y=0.5, name = "L'") + pattern._points['Lback']
        self._points['Dfront'] = Point(x=0.75, y=0, name = "D'") + pattern._points['Dback']
        self._points['Afront'] = Point(x=0, y=pattern._front_waist_lenght[curStatureIdx], name = "A'") + pattern._points['Cfront']
        self._points['Oback'] = Point(x=0.5*(pattern._points['A']._x+pattern._points['Dback']._x), y=0.5*(pattern._points['A']._y+pattern._points['Dback']._y), name = "O")
        self._points['Odart'] = Point(x=pattern._points['Oback']._x, y=pattern._points['F']._y, name = "O2")
        
        for pointKey, pointValue in self._points.items():
            if "back" not in pointKey:
                self.draw_point(pattern._areas["FrontAreaBasePoints"], pointValue)
            if "front" not in pointKey:
                self.draw_point(pattern._areas["BackAreaBasePoints"], pointValue)

     def draw_base_line_and_curves_front(self):
        g = self._areas["FrontAreaBase"]
        pattern.compute_front_neckline_base_curve()
        pattern.compute_front_armhole_base_curve()
        pattern.compute_front_waist_base_curve()
        line1 = My_Line(P1=self._points['A'], P2=self._points['Cfront'])        
        line2 = My_Line(P1=self._points['Ifront'], P2=self._points['Lfront'])  
        line3 = My_Line(P1=self._points['E'], P2=self._points['Dfront'])  
        line4 = My_Line(P1=self._points['Afront'], P2=self._points['A'])  
        paths = My_Path(line1,self._front_neckline_base_curve,line2, self._front_armhole_base_curve,line3, self._front_waist_base_curve, line4, closed=True)
        path = self._svg_file.path(d=(paths.d()),
                                      id = g.get_id() + "Curve", 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + 'base'
        g.add(path)
        self.draw_line(g, self._points['Cfront'], self._points['Jfront'], curStatureIdx, 'thin')
        self.draw_line(g, self._points['Jfront'], self._points['Ifront'], curStatureIdx, 'thin')
        self.draw_line(g, self._points['E'], self._points['F'], curStatureIdx, 'thin')
        self.draw_line(g, self._points['A'], self._points['Dfront'], curStatureIdx, 'thin')
        self.draw_line(g, self._points['G'], self._points['Nfront'], curStatureIdx, 'thin')

     def draw_base_line_and_curves_back(self):
        g = self._areas["BackAreaBase"]
        pattern.compute_back_neckline_base_curve()
        pattern.compute_back_armhole_base_curve()
        line1 = My_Line(P1=self._points['A'], P2=self._points['Bback'])        
        line2 = My_Line(P1=self._points['Iback'], P2=self._points['Lback'])  
        line3 = My_Line(P1=self._points['E'], P2=self._points['Dback'])  
        line4 = My_Line(P1=self._points['Dback'], P2=self._points['A'])  
        paths = My_Path(line1,self._back_neckline_base_curve,line2, self._back_armhole_base_curve,line3, line4, closed=True)
        path = self._svg_file.path(d=(paths.d()),
                                      id = g.get_id() + "Curve", 
                                      stroke_linejoin = 'round',
                                      fill = 'none')
        path['class'] = str(self._strokes[curStatureIdx]) + " " + 'base'
        g.add(path)
        self.draw_line(g, self._points['Bback'], self._points['Hback'], curStatureIdx, 'thin')
        self.draw_line(g, self._points['Hback'], self._points['Iback'], curStatureIdx, 'thin')
        self.draw_line(g, self._points['Kback'], self._points['Lback'], curStatureIdx, 'thin')
        self.draw_line(g, self._points['E'], self._points['F'], curStatureIdx, 'thin')
        self.draw_line(g, self._points['G'], self._points['Mback'], curStatureIdx, 'thin')
        self.draw_line(g, self._points['Oback'], self._points['Odart'], curStatureIdx, 'thin')

        # Base, dart
        ad2lenght = self.get_distance(pattern._points['Dback'], pattern._points['A'])
        pince = 0.5*self._waist_measurement[curStatureIdx] - self._front_waist_base_curve_lenght - ad2lenght
        pattern._points['Pback'] = Point(x=-0.5*pince, y=0, name = "P") + pattern._points['Oback']
        pattern._points['Qback'] = Point(x=+0.5*pince, y=0, name = "Q") + pattern._points['Oback']
        pattern.draw_line(g, pattern._points['Odart'], pattern._points['Pback'], curStatureIdx, 'thin')
        pattern.draw_line(g, pattern._points['Odart'], pattern._points['Qback'], curStatureIdx, 'thin')

     def display(self):
        print "PATTERN"
        for attr in self.__dict__.keys():
            print attr, getattr(self,attr)

if __name__ == '__main__':
    
    pattern = Pattern_Generator(basic_bodice_enlargement='True')

    a4Size = np.array((21,29.7))
    pdfSize = np.trunc(0.95*a4Size)
    
    pattern.open_svg("pattern.svg", pdfSize)
    
    # Creation of the working area and the pdf area
    for id in ("pdfArea", "workingArea", "cleanAreaPadding"):
        pattern._areas[id] = pattern._svg_file.g(id=id, font_family="serif", font_size=str(8*PXCM)+'px')
        pattern._svg_file.add(pattern._areas[id])
    pattern._areas["cleanArea"] = pattern._svg_file.g(id="cleanArea", font_family="serif", font_size=str(8*PXCM)+'px')
    pattern._areas["cleanAreaPadding"].add(pattern._areas["cleanArea"])
    
    for curStatureIdx,curStature in enumerate(pattern._stature):
        curStatureAreaStr = "stature"+str(curStatureIdx)+"Area"
        pattern._areas[curStatureAreaStr] = pattern._svg_file.g(id="stature"+str(curStature), font_family="serif", font_size=str(8*PXCM)+'px', fill='black')
        pattern._areas["workingArea"].add(pattern._areas[curStatureAreaStr])
        for frontbackId,frontback in enumerate(("Front","Back")):
            pattern._areas[frontback+"Area"] = pattern._svg_file.g(id="stature"+str(curStature)+frontback, font_family="serif", font_size=str(8*PXCM)+'px', fill='black')
            pattern._areas[curStatureAreaStr].add(pattern._areas[frontback+"Area"])
            pattern._areas[frontback+"Area"+"Base"] = pattern._svg_file.g(id="stature"+str(curStature)+frontback+"Base", font_family="serif", font_size=str(8*PXCM)+'px', fill='black')
            pattern._areas[frontback+"Area"].add(pattern._areas[frontback+"Area"+"Base"])
            pattern._areas[frontback+"Area"+"BasePoints"] = pattern._svg_file.g(id="stature"+str(curStature)+frontback+"BasePoints", font_family="serif", font_size=str(8*PXCM)+'px', fill='black')
            pattern._areas[frontback+"Area"+"Base"].add(pattern._areas[frontback+"Area"+"BasePoints"])
            if (pattern._basic_bodice_enlargement):
                pattern._areas[frontback+"Area"+"BodiceEnlargement"] = pattern._svg_file.g(id="stature"+str(curStature)+frontback+"BodiceEnlargement", font_family="serif", font_size=str(8*PXCM)+'px', fill='black')
                pattern._areas[frontback+"Area"].add(pattern._areas[frontback+"Area"+"BodiceEnlargement"])
                pattern._areas[frontback+"Area"+"BodiceEnlargementPoints"] = pattern._svg_file.g(id="stature"+str(curStature)+frontback+"BodiceEnlargementPoints", font_family="serif", font_size=str(8*PXCM)+'px', fill='black')
                pattern._areas[frontback+"Area"+"BodiceEnlargement"].add(pattern._areas[frontback+"Area"+"BodiceEnlargementPoints"])
        pattern._areas["sleeveArea"] = pattern._svg_file.g(id="stature"+str(curStature)+"sleeve", font_family="serif", font_size=str(8*PXCM)+'px', fill='black')
        pattern._areas[curStatureAreaStr].add(pattern._areas["sleeveArea"])

        pattern._points.clear()
        
        # Points
        pattern.place_base_points()

        # Base, lines
        pattern.draw_base_line_and_curves_front()
        pattern.draw_base_line_and_curves_back()

        # Elargissements
        if (pattern._basic_bodice_enlargement):
            pattern.draw_bodice_adjustement_line_and_curves_front()
            pattern.draw_bodice_adjustement_line_and_curves_back()
            for oldkey in [k for k,v in pattern._points.items() if "bafront" in k]:
                pattern._points[oldkey.replace("bafront", "front")] = pattern._points.pop(oldkey)
            for oldkey in [k for k,v in pattern._points.items() if "baback" in k]:
                pattern._points[oldkey.replace("baback", "back")] = pattern._points.pop(oldkey)


        # print '\n'.join(str(p) for p in [(k,v) for k,v in sorted(pattern._points.items())])

        # Compute arlhole depth
        pattern.compute_armhole_depth()
        
        # Sleeve
        pattern.draw_sleeve(3.5)

        #c 1.3017396,0 2.269681,0.9999937 3.0771504,1.8935775 0.7892876,0.873463 1.3437468,2.774535 1.5377142,3.1794101 0.3109992,0.6491595 0.7845752,2.3514852 1.5977144,3.2394116 0.7948182,0.86792036 1.7326761,1.87302864 3.01715,1.83357617

        #pattern.draw_point(pattern._areas["sleeveArea"], pattern._points['SCE2Creux'])
        #pattern.draw_point(pattern._areas["sleeveArea"], pattern._points['SAF2Creux'])
        #pattern.draw_point(pattern._areas["sleeveArea"], pattern._points['SF2DCreux'])
        #pattern.draw_line(pattern._areas["sleeveArea"], pattern._points['SC'], pattern._points['SE2'], curStatureIdx, 'base')
        #pattern.draw_line(pattern._areas["sleeveArea"], pattern._points['SA'], pattern._points['SE2'], curStatureIdx, 'base')
        #pattern.draw_line(pattern._areas["sleeveArea"], pattern._points['SA'], pattern._points['SF2'], curStatureIdx, 'base')
        #pattern.draw_line(pattern._areas["sleeveArea"], pattern._points['SD'], pattern._points['SF2'], curStatureIdx, 'base')

        pattern._areas["BackArea"].translate(3*CMPX,0*CMPX)
        pattern._areas["sleeveArea"].translate((-35+pattern._points['SB']._x-0)*-CMPX,(pattern._points['SB']._y-0)*-CMPX)

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
        #pattern._areas["backAreaRotated"].translate((pattern._pointICE._x-pattern._pointI2CE._x)*-CMPX,(pattern._pointICE._y+pattern._pointI2CE._y)*-CMPX)
        #pattern._areas["backAreaRotated"].rotate(rotangle, [pattern._pointICE._x*CMPX, pattern._pointICE._y*CMPX])
        #pattern._areas[curStatureAreaStr].add(pattern._areas["backAreaRotated"])
        
        #pattern._areas["backArea"].scale(-1,1)
        #pattern._areas["backArea"].translate(2*(pattern._pointECE._x)*-CMPX,0)

        for xx,x in enumerate(["FrontAreaBodiceEnlargement", "BackAreaBodiceEnlargement"]):
            toto = copy.deepcopy(pattern._areas[x])
            toto.translate(50*xx,100)
            pattern._areas["cleanArea"].add(toto)
            toto = copy.deepcopy(pattern._areas[x])
            toto.translate(50*xx,100)
            toto.scale(-1,1)
            pattern._areas["cleanArea"].add(toto)
        pattern.save_svg()

    query = dict()
    for q in ["x","y","width","height"]:
        query["cleanArea"+q]=float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id=cleanArea",
                          "--query-"+q,
                          pattern._svg_file.filename]))
        print "cleanArea"+q, "=", query["cleanArea"+q]
    padding=50
    RATIODPI = 2.54/96.0
    paddingline = My_Line(P1=Point(x=(query["cleanAreax"]-padding)*PXCM,y=(query["cleanAreay"]-padding)*PXCM), 
                          P2=Point(x=(query["cleanAreax"]+query["cleanAreawidth"]+padding)*PXCM,y=(query["cleanAreay"]+query["cleanAreaheight"]+padding)*PXCM))        
    paddinglinepath = My_Path(paddingline, closed=False)
    path = pattern._svg_file.path(d=(paddinglinepath.d()),
                                  id="cleanAreaPaddingDiagonal",
                                  fill = 'none')
    pattern._areas["cleanAreaPadding"].add(path)
    pattern.save_svg()
    for q in ["x","y","width","height"]:
        query["cleanAreaPadding"+q]=float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id=cleanAreaPadding",
                          "--query-"+q,
                          pattern._svg_file.filename]))
        print "cleanAreaPadding"+q, "=", query["cleanAreaPadding"+q]
        
    # Fill the pdf area side (viewBox) with nbPdf sheets
    s1 = 'M0,0v'+str(0.5*pdfSize[1])+'v'+str(0.5*pdfSize[1])
    s1 += 'h'+str(0.5*pdfSize[0])+'h'+str(0.5*pdfSize[0])
    s1 += 'v'+str(-0.5*pdfSize[1])+'v'+str(-0.5*pdfSize[1])
    s1 += 'h'+str(-0.5*pdfSize[0])+'z'
    for x in (1,1.1):
      s1 += 'M0,'+str(x)+'l'+str(x)+',-'+str(x)
      s1 += 'M0,'+str(pdfSize[1]-x)+'l'+str(x)+','+str(x)
      s1 += 'M'+str(pdfSize[0]-x)+',0l'+str(x)+','+str(x)
      s1 += 'M'+str(pdfSize[0]-x)+','+str(pdfSize[1])+'l'+str(x)+',-'+str(x)

    onePdfSheetPath = parse_path(s1)        
    onePdfSheet = pattern._svg_file.path(d=(onePdfSheetPath.d()), id = "sheet", stroke = "grey", stroke_linejoin = 'round', fill = 'none')
    onePdfSheet['class'] = 'onePdfSheet'
    #markerPath = parse_path('M0,0v20h20v-20z')
    #marker = pattern._svg_file.marker(insert=(10,10), size=(20,20))
    #marker.add(pattern._svg_file.path(d=(markerPath.d()), fill = 'pink'))
    #pattern._svg_file.defs.add(marker)
    #onePdfSheet.set_markers(marker)
    
    for x in range(0,int(math.ceil(PXCM*query["cleanAreaPaddingwidth"]/pdfSize[0]))):
        for y in range(0,int(math.ceil(PXCM*query["cleanAreaPaddingheight"]/pdfSize[1]))):
            xyPdfSheet = copy.deepcopy(onePdfSheet)
            xyPdfSheet['id'] = "sheet_" + str(x) + "_" + str(y) 
            xyPdfSheet.translate(x*CMPX*pdfSize[0], y*CMPX*pdfSize[1])
            pattern._areas["pdfArea"].add(xyPdfSheet)

    pattern.save_svg()

    for q in ["x","y","width","height"]:
        query["pdfArea"+q]=float(subprocess.check_output(["C:\\Program Files\\Inkscape\\inkscape.exe",
                          "--query-id=pdfArea",
                          "--query-"+q,
                          pattern._svg_file.filename]))
        print "pdfArea"+q, "=", query["pdfArea"+q]

    tx = str(PXCM * (query["cleanAreaPaddingx"]-query["pdfAreax"]))
    ty = str(PXCM * (query["cleanAreaPaddingy"]-query["pdfAreay"]))
    pattern._areas["pdfArea"]['transform'] = "translate(" + tx + "," + ty + ")"
    pattern.save_svg()

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


    
