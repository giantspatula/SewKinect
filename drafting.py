from __future__ import division
from math import pi, sqrt
import math
import sys
import cairo
if not cairo.HAS_PDF_SURFACE:
    raise SystemExit ('cairo was not compiled with PDF support')


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(%r, %r)" % (self.x, self.y)

class Drafting():

    def __init__(self, measurements):
        self.inch_measurements = measurements
        self.m = {}
        self.width = 0
        self.height = 0
        self.default_measurements = { 
    "waist": 28,
    "hip": 40,
    "thigh": 22.25,
    "waistToHip": 8.34,
    "waistToKnee": 22.875,
    "waistToFloor": 40.35,
    "knee": 18,
    "ankle": 14,
    "girth": 29.375,
    "ease": 1.5
    }
        self.fill_in_holes()
        self.create_point_measures()


    def fill_in_holes(self):
        for measure in self.default_measurements:
            if measure not in self.inch_measurements or self.inch_measurements.get(measure) is None:
                self.inch_measurements[measure] = self.default_measurements.get(measure)
        self.inch_measurements["knee"] = self.inch_measurements["thigh"]*.82
        self.inch_measurements["ankle"] = self.inch_measurements["thigh"]*.62
        self.inch_measurements["kneeToFloor"] = self.inch_measurements.get("waistToFloor") - self.inch_measurements.get("waistToKnee")
        self.inch_measurements["thighToKnee"] = (self.inch_measurements.get("waistToKnee") - self.inch_measurements.get("waistToHip"))
        rise_depth = self.inch_measurements["thigh"] - (self.inch_measurements["waist"]/2)
        self.inch_measurements["front_rise_depth"] = rise_depth*(1/3)
        self.inch_measurements["back_rise_depth"] = (rise_depth)*(2/3)
        # self.inch_measurements["back_rise"] = self.inch_measurements["waistToKnee"] - self.inch_measurements["thighToKnee"]
        # self.inch_measurements["front_rise"] = self.inch_measurements["waistToKnee"] - self.inch_measurements["thighToKnee"]
        self.inch_measurements["back_rise"] = self.inch_measurements["girth"]*.56
        self.inch_measurements["front_rise"] = self.inch_measurements["girth"]*.44

    def create_point_measures(self):
        for measurement in self.inch_measurements:
            self.m[measurement] = 72*self.inch_measurements.get(measurement)

    def draft_circle_skirt(self, filename):
        self.m["ease"] = 1.5*72
        self.width  = 2*(self.m.get("waistToKnee")+8*72)
        self.height = (self.m.get("waistToKnee")+8*72)
        self.render_pdf(filename, self.circle_skirt)

    def draft_skirt(self, filename):
        self.m["ease"] = .59*72
        self.width  = (self.m.get("hip") + self.m.get("ease"))/2+(2*72)
        self.height =  self.m.get("waistToKnee") + (5 * 72)
        self.render_pdf(filename, self.skirt)

    def draft_leggings(self, filename):
        self.m["ease"] = .83
        self.width  = self.m.get("hip")
        self.height = self.m.get("waistToFloor") + (self.m.get('back_rise'))
        self.render_pdf(filename, self.leggings)

    def skirt(self, cr):
        cr.set_source_rgb(0,0,0)

        dart_width = (abs(self.m.get("hip")-self.m.get("waist"))/4 + self.m.get("ease"))/6
        if 12*dart_width > self.m.get("waist")-self.m.get("ease"):
            dart_width = 29

        A = Point(72, 72*2.5) #leftmost waist point
        B = Point(A.x+(self.m.get("hip")/2)+self.m.get("ease"), A.y) #rightmost waist point
        C = Point(A.x, A.y+self.m.get("waistToKnee")) #lower left corner
        cr.move_to(A.x, A.y)
        cr.line_to(C.x, C.y)
        cr.stroke()

        cr.move_to(C.x, C.y)
        cr.line_to(B.x, C.y)
        cr.stroke()

        cr.move_to(B.x, C.y)
        cr.line_to(B.x, B.y)
        cr.stroke()

        #front/back/hip point
        D = Point(A.x+(self.m.get("hip")/4)+self.m.get("ease"), A.y+self.m.get("waistToHip"))
        #draws side seam
        cr.move_to(D.x, D.y)
        cr.line_to(D.x, C.y)
        cr.stroke()

        # "POINT 9" - 1/4 waist measurement + 1.67"
        E = Point(A.x+(self.m.get("waist")/4)+1.67*72, A.y)
        # "POINT 10"
        F = Point(E.x, A.y-self.m.get('ease'))

        #DISTANCE between A and F 
        dist = math.hypot(F.x - A.x, F.y - A.y)
        third_AF = dist/3

        # "POINT 11"
        dx = (F.x-A.x)
        dy = (F.y-A.y)
        G = Point(dx/3+A.x, dy/3+A.y)
        G1 = Point(G.x-dart_width, G.y)
        G2 = Point(G.x+dart_width, G.y)

        # "POINT 12"
        H = Point(dx/3+G.x, dy/3+G.y)
        H1 = Point(H.x-dart_width, H.y)
        H2 = Point(H.x+dart_width, H.y)

        # "POINT 13"
        ratio = 432/dist #dart length
        I = Point(G.x-dy*ratio, G.y+dx*ratio) 

        # "POINT 14"
        ratio = 360/dist #dart length
        J = Point(H.x-dy*ratio, H.y+dx*ratio)

        cr.move_to(A.x, A.y)
        cr.line_to(G1.x, G1.y)
        cr.stroke()

        cr.move_to(G1.x, G1.y)
        cr.line_to(I.x, I.y)
        cr.stroke()

        cr.move_to(I.x, I.y)
        cr.line_to(G2.x, G2.y)
        cr.stroke()

        cr.move_to(G2.x, G2.y)
        cr.line_to(H1.x, H1.y)
        cr.stroke()

        cr.move_to(H1.x, H1.y)
        cr.line_to(J.x, J.y)
        cr.stroke()

        cr.move_to(J.x, J.y)
        cr.line_to(H2.x, H2.y)
        cr.stroke()

        cr.move_to(H2.x, H2.y)
        cr.line_to(F.x, F.y)
        cr.stroke()
    
        cr.curve_to(F.x, F.y, F.x+2*self.m.get("ease"), F.y, D.x, D.y)
        cr.stroke()

        # "POINT 16"
        K = Point(B.x-(self.m.get("waist")/4)-60, B.y-35)
        dist = math.hypot(B.x - K.x, B.y - K.y)
        third_BK = dist/3

        dy = K.y - B.y
        dx = B.x - K.x

        # "POINT 17"
        L = Point(K.x+dx/3, K.y-dy/3)
        L1 = Point(L.x-dart_width, L.y)
        L2 = Point(L.x+dart_width, L.y)

        # "POINT 18"
        ratio = 280/dist
        M = Point(L.x+dy*ratio, L.y+dx*ratio)

        cr.move_to(K.x, K.y)
        cr.line_to(L1.x, L1.y)
        cr.stroke()

        cr.move_to(L1.x, L1.y)
        cr.line_to(M.x, M.y)
        cr.stroke()

        cr.move_to(M.x, M.y)
        cr.line_to(L2.x, L2.y)
        cr.stroke()

        cr.move_to(L2.x, L2.y)
        cr.line_to(B.x, B.y)
        cr.stroke()

        cr.curve_to(K.x, K.y, K.x-2*self.m.get("ease"), K.y-2*self.m.get("ease"), D.x, D.y)
        cr.stroke()

    def leggings(self, cr):
        #measure waist to floor 
        cr.set_source_rgb(0,0,0)
        A = Point(self.width/2, 0)
        B = Point(A.x, self.m.get("waistToFloor")+self.m.get('waistToHip')+2.75*72)

        #draw ankle line
        C = Point(B.x-self.m.get("ankle")/2, B.y) #left ankle point
        D = Point(B.x+self.m.get("ankle")/2, B.y) #right ankle point
        cr.move_to(C.x, C.y)
        cr.line_to(D.x, D.y)
        cr.stroke()

        #move up to knee
        E = Point(self.width/2, B.y-self.m.get("kneeToFloor"))
        F = Point(E.x-self.m.get("knee")/2, E.y) #left knee point
        G = Point(E.x+self.m.get("knee")/2, E.y) #right knee point
        cr.move_to(C.x, C.y)
        cr.line_to(F.x, F.y)
        cr.stroke()
        cr.move_to(D.x, D.y)
        cr.line_to(G.x, G.y)
        cr.stroke()

        #move up to thigh 
        H = Point(self.width/2, E.y-self.m.get("thighToKnee"))
        I = Point(H.x-self.m.get("thigh")/2, H.y) #left thigh point
        J = Point(H.x+self.m.get("thigh")/2, H.y) #right thigh point
        cr.move_to(F.x, F.y)
        cr.line_to(I.x, I.y)
        cr.stroke()
        cr.move_to(G.x, G.y)
        cr.line_to(J.x, J.y)
        cr.stroke()

        #back thigh depth
        K = Point(I.x+self.m.get("back_rise_depth"), I.y)
        
        #front thigh depth
        L = Point(J.x-self.m.get("front_rise_depth"), J.y)

        #back rise height
        M = Point(K.x, K.y-self.m.get("back_rise"))

        #front rise height
        N = Point(L.x, L.y-self.m.get("front_rise"))

        #-- draw waist line --#
        MN = Point(M.x +(N.x - M.x)/2, M.y+(N.y -M.y)/2)
        cr.curve_to(M.x, M.y, MN.x-29, MN.y+29, N.x, N.y)
        cr.stroke()

        #-- draw crotch curves  --#
        O = Point(M.x, I.y) #back curve point
        P = Point(N.x, I.y) #front curve point

        cr.curve_to(I.x, I.y, O.x, O.y, M.x, M.y)
        cr.stroke()

        cr.curve_to(J.x, J.y, P.x, P.y, N.x, N.y)
        cr.stroke()

    def circle_skirt(self, cr):
        r = self.m.get("waist")/(2*pi)
        outer_r = r + self.m.get("waistToKnee")

        cr.set_source_rgb(0,0,0)
        cr.arc(self.width/2, 0, r, 0, 2*pi)
        cr.stroke()

        cr.arc(self.width/2, 0, outer_r, 0, 2*pi)
        cr.stroke()

    def render_pdf(self, filename, drafting_function):
        surface = cairo.PDFSurface (filename, self.width, self.height)
        cr = cairo.Context(surface)

        cr.save()

        print type(cr)

        drafting_function(cr)
    
        cr.restore()
        cr.show_page()
        surface.finish()

if __name__ == '__main__':
    draft = Drafting({})
    draft.draft_circle_skirt("static/patterns/test.pdf")



    