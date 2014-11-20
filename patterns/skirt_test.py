from __future__ import division
from math import pi
import sys
import measurement_api as measures

import cairo
if not cairo.HAS_PDF_SURFACE:
    raise SystemExit ('cairo was not compiled with PDF support')


#drafts 1/2 a full circle skirt

m = measures.create_point_measures()
width  = (m.get("hip") + m.get("ease"))/2
height = 24 + m.get("ease") + (5 * 72)

def draft_skirt(cr):
    cr.set_line_width (10)
    cr.set_source_rgb(1,0,0)
    cr.arc(72, 72, 72, 0, 2*pi)
    cr.fill()
    cr.move_to(0,0)
    cr.line_to(width, height)
    cr.stroke()


def render_pdf():
    surface = cairo.PDFSurface ("skirt_test.pdf", width, height)
    cr = cairo.Context(surface)

    cr.save()

    draft_skirt(cr)
    
    cr.restore()
    cr.show_page()
    surface.finish()


if __name__ == '__main__':

    render_pdf()

