from __future__ import division
from math import pi
import sys

import cairo
if not cairo.HAS_PDF_SURFACE:
    raise SystemExit ('cairo was not compiled with PDF support')


#drafts 1/2 a full circle skirt

waist_in_inches = 28
length_in_inches = 24

waist = waist_in_inches*72
length = length_in_inches*72

waist_radius = waist/(2*pi)

width = waist_radius + length
height = width


# width_in_inches, height_in_inches = 2, 2
# width_in_points, height_in_points = width_in_inches * 72, height_in_inches * 72
# width, height = width_in_points, height_in_points


def draw():
    surface = cairo.PDFSurface ("test.pdf", width, height)
    cr = cairo.Context(surface)

    cr.save()

    cr.set_source_rgb(1,1,1)
    cr.rectangle(0, 0, width, height)
    cr.fill()
    cr.arc(width/2, height/2, width/2, pi, 2*pi)
    cr.set_source_rgb(1,0,0)
    cr.fill()
    cr.arc(width/2, height/2, waist_radius, pi, 2*pi)
    cr.set_source_rgb(1,1,1)
    cr.fill()
    cr.restore()
    cr.show_page()
    surface.finish()


if __name__ == '__main__':
    draw()