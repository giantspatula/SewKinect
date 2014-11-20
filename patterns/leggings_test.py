from __future__ import division
from math import pi
import sys
import measurement_api as measures

import cairo
if not cairo.HAS_PDF_SURFACE:
    raise SystemExit ('cairo was not compiled with PDF support')


#drafts 1/2 a full circle skirt

m = measures.create_point_measures()
width  = m.get("hip")
height = 45*72 + 5*72


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


def draft_leggings(cr):
    cr.set_line_width (10)
    cr.set_source_rgb(1,0,0)

    #draw center line 
    cr.move_to(width/2, 0)
    cr.line_to(width/2, height)
    cr.stroke()

    #measure waist to floor 
    cr.set_source_rgb(0,0,0)
    A = Point(width/2, 72*2)
    B = Point(A.x, m.get("waist_to_floor"))

    #draw ankle line
    C = Point(B.x-m.get("ankle")/2, B.y) #left ankle point
    D = Point(B.x+m.get("ankle")/2, B.y) #right ankle point
    cr.move_to(C.x, C.y)
    cr.line_to(D.x, D.y)
    cr.stroke()

    #move up to knee
    E = Point(width/2, B.y-m.get("ankle_to_knee"))
    F = Point(E.x-m.get("knee")/2, E.y) #left knee point
    G = Point(E.x+m.get("knee")/2, E.y) #right knee point
    cr.move_to(C.x, C.y)
    cr.line_to(F.x, F.y)
    cr.stroke()
    cr.move_to(D.x, D.y)
    cr.line_to(G.x, G.y)
    cr.stroke()

    #move up to thigh 
    H = Point(width/2, E.y-m.get("knee_to_thigh"))
    I = Point(H.x-m.get("thigh")/2, H.y) #left thigh point
    J = Point(H.x+m.get("thigh")/2, H.y) #right thigh point
    cr.move_to(F.x, F.y)
    cr.line_to(I.x, I.y)
    cr.stroke()
    cr.move_to(G.x, G.y)
    cr.line_to(J.x, J.y)
    cr.stroke()

    #back thigh depth
    K = Point(I.x+m.get("back_rise_depth"), I.y)
    
    #front thigh depth
    L = Point(J.x-m.get("front_rise_depth"), J.y)

    #back rise height
    M = Point(K.x, K.y-m.get("back_rise"))

    #front rise height
    N = Point(L.x, L.y-m.get("front_rise"))

    #-- draw line -- replace with curve later --
    cr.move_to(N.x, N.y)
    cr.line_to(M.x, M.y)
    cr.stroke()

    #-- draw line -- replcae with curve later --
    O = Point(I.x+72, I.y) #back curve point
    P = Point(J.x-72, I.y) #front curve point
    cr.move_to(M.x, M.y)
    cr.line_to(O.x, O.y)
    cr.stroke()
    cr.move_to(N.x, N.y)
    cr.line_to(P.x, P.y)
    cr.stroke()


def render_pdf():
    surface = cairo.PDFSurface ("leggings_test.pdf", width, height)
    cr = cairo.Context(surface)

    cr.save()

    draft_leggings(cr)
    
    cr.restore()
    cr.show_page()
    surface.finish()


if __name__ == '__main__':

    render_pdf()

