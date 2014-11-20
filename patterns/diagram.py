#! /usr/bin/env python
import cairo
from math import pi
import sys

class Diagram(object):
    def __init__(self, filename, width, height, alpha, separate=True):
        iwidth = width
        if separate:
            iwidth = int(width * 4.0 / 3 + 0.99)
        iheight = height
        #self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, iwidth, iheight)
        self.surface = cairo.SVGSurface(filename + '.svg', iwidth, iheight)
        cr = self.cr = cairo.Context(self.surface)

        cr.scale(width, height)
        cr.set_line_width(0.01)

        cr.save()
        cr.transform(cairo.Matrix(0.6, 0, 1.0/3, 0.5, 0.02, 0.45))
        cr.push_group()
        cr.rectangle(0, 0, 1, 1); cr.clip()
        self.draw_dest(self.cr)
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width( max(cr.device_to_user_distance(2, 2)) )
        cr.rectangle(0, 0, 1, 1)
        cr.stroke()
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha[0])
        cr.restore()

        cr.save()
        cr.transform(cairo.Matrix(0.6, 0, 1.0/3, 0.5, 0.04, 0.25))
        cr.push_group()
        cr.rectangle(0, 0, 1, 1); cr.clip()
        self.draw_mask(self.cr)
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha[1])
        cr.restore()

        cr.save()
        cr.transform(cairo.Matrix(0.6, 0, 1.0/3, 0.5, 0.06, 0.05))
        cr.push_group()
        cr.rectangle(0, 0, 1, 1); cr.clip()
        self.draw_src(self.cr)
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha[2])
        cr.restore()

        if separate:
            cr.save()
            cr.translate(1, 0)
            cr.scale(1.0 / 3, 1.0 / 3)
            cr.push_group()
            cr.rectangle(0, 0, 1, 1); cr.clip()
            self.draw_src(self.cr)
            cr.pop_group_to_source()
            cr.paint()
            cr.restore()

            cr.save()
            cr.translate(1, 1.0 / 3)
            cr.scale(1.0 / 3, 1.0 / 3)
            cr.push_group()
            cr.rectangle(0, 0, 1, 1); cr.clip()
            self.draw_mask(self.cr)
            cr.pop_group_to_source()
            cr.paint()
            cr.restore()

            cr.save()
            cr.translate(1, 2.0 / 3)
            cr.scale(1.0 / 3, 1.0 / 3)
            cr.push_group()
            cr.rectangle(0, 0, 1, 1); cr.clip()
            self.draw_dest(self.cr)
            cr.pop_group_to_source()
            cr.paint()
            cr.restore()

            cr.set_line_width( max(cr.device_to_user_distance(2, 2)) )
            cr.rectangle(1, 0, 1.0/3, 1)
            cr.clip_preserve()
            cr.stroke()
            cr.rectangle(1, 1.0/3, 1.0/3, 1.0/3)
            cr.stroke()

        self.surface.write_to_png(filename + '.png')
        cr.show_page()
        self.surface.finish()

    def draw_dest(self, cr):
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, 1, 1)
        cr.fill()

    def draw_mask(self, cr, mask=None):
        cr.set_source_rgb(1, 0.9, 0.6)
        if mask:
            cr.mask(mask)
        else:
            cr.rectangle(0, 0, 1, 1)
            cr.fill()

    def draw_src(self, cr):
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0, 1, 1)
        cr.fill()

class Stroke(Diagram):
    def draw_mask(self, cr):
        cr.push_group()
        cr.rectangle(0, 0, 1, 1)
        cr.rectangle(0.20, 0.20, 0.6, 0.6)
        cr.rectangle(0.30, 0.30, 0.4, 0.4)
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.fill()
        cr.set_fill_rule(cairo.FILL_RULE_WINDING)

        Diagram.draw_mask(self, cr, cr.pop_group())

        cr.rectangle(0.25, 0.25, 0.5, 0.5)
        cr.set_source_rgb(0, 0.6, 0)
        cr.set_line_width( max(cr.device_to_user_distance(1, 1)) )
        cr.stroke()


    def draw_dest(self, cr):
        Diagram.draw_dest(self, cr)

        cr.set_line_width(0.1)              #stroke
        cr.set_source_rgb(0, 0, 0)          #stroke
        cr.rectangle(0.25, 0.25, 0.5, 0.5)  #stroke
        cr.stroke()                         #stroke

class Fill(Diagram):
    def draw_mask(self, cr):
        cr.push_group()
        cr.rectangle(0, 0, 1, 1)
        cr.rectangle(0.25, 0.25, 0.5, 0.5)
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.fill()
        cr.set_fill_rule(cairo.FILL_RULE_WINDING)

        Diagram.draw_mask(self, cr, cr.pop_group())

        cr.rectangle(0.25, 0.25, 0.5, 0.5)
        cr.set_source_rgb(0, 0.6, 0)
        cr.set_line_width( max(cr.device_to_user_distance(1, 1)) )
        cr.stroke()

    def draw_dest(self, cr):
        Diagram.draw_dest(self, cr)

        cr.set_source_rgb(0, 0, 0)         #fill
        cr.rectangle(0.25, 0.25, 0.5, 0.5) #fill
        cr.fill()                          #fill

class ShowText(Diagram):
    def draw_mask(self, cr):
        cr.select_font_face("Georgia",
                cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(1.2)
        x_bearing, y_bearing, width, height = cr.text_extents("a")[:4]

        cr.push_group()
        cr.rectangle(0, 0, 1, 1)
        cr.move_to(0.5 - width / 2 - x_bearing, 0.5 - height / 2 - y_bearing)
        cr.text_path("a")
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.fill()
        cr.set_fill_rule(cairo.FILL_RULE_WINDING)
        Diagram.draw_mask(self, cr, cr.pop_group())

        cr.move_to(0.5 - width / 2 - x_bearing, 0.5 - height / 2 - y_bearing)
        cr.set_source_rgb(0, 0.6, 0)
        cr.set_line_width( max(cr.device_to_user_distance(1, 1)) )
        cr.text_path("a")
        cr.stroke()


    def draw_dest(self, cr):
        Diagram.draw_dest(self, cr)

        cr.set_source_rgb(0.0, 0.0, 0.0)                                      #text
        cr.select_font_face("Georgia",                                        #text
                cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)              #text
        cr.set_font_size(1.2)                                                 #text
        x_bearing, y_bearing, width, height = cr.text_extents("a")[:4]        #text
        cr.move_to(0.5 - width / 2 - x_bearing, 0.5 - height / 2 - y_bearing) #text
        cr.show_text("a")                                                     #text

class Paint(Diagram):
    def draw_mask(self, cr):
        pass

    def draw_dest(self, cr):
        Diagram.draw_dest(self, cr)
        cr.set_source_rgb(0.0, 0.0, 0.0) #paint
        cr.paint_with_alpha(0.5)         #paint

    def draw_src(self, cr):
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.rectangle(0, 0, 1, 1)
        cr.fill()

class Mask(Diagram):
    def __init__(self, *args):

        self.linear = cairo.LinearGradient(0, 0, 1, 1)                    #mask
        self.linear.add_color_stop_rgb(0, 0, 0.3, 0.8)                    #mask
        self.linear.add_color_stop_rgb(1, 0, 0.8, 0.3)                    #mask
                                                                          #mask
        self.radial = cairo.RadialGradient(0.5, 0.5, 0.25, 0.5, 0.5, 0.75)#mask
        self.radial.add_color_stop_rgba(0, 0, 0, 0, 1)                    #mask
        self.radial.add_color_stop_rgba(0.5, 0, 0, 0, 0)                  #mask
                                                                          #mask
        self.radialinv = cairo.RadialGradient(0.5, 0.5, 0.25, 0.5, 0.5, 0.75)
        self.radialinv.add_color_stop_rgba(0, 0, 0, 0, 0)
        self.radialinv.add_color_stop_rgba(0.5, 0, 0, 0, 1)
        super(Mask, self).__init__(*args)

    def draw_mask(self, cr):
        cr.save()
        cr.rectangle(0, 0, 1, 1)
        cr.clip()
        Diagram.draw_mask(self, cr, self.radialinv)
        cr.restore()

    def draw_dest(self, cr):
        Diagram.draw_dest(self, cr)
        cr.save()
        cr.rectangle(0, 0, 1, 1)
        cr.clip()
        cr.set_source(self.linear)                                        #mask
        cr.mask(self.radial)                                              #mask
        cr.restore()

    def draw_src(self, cr):
        cr.set_source(self.linear)
        cr.rectangle(0, 0, 1, 1)
        cr.fill()

if __name__ == '__main__':
    size = 120
    Diagram('destination', size, size, [1, 0.15, 0.15])
    Diagram('the-mask', size, size, [0.15, 1, 0.15])
    Diagram('source', size, size, [0.15, 0.15, 1])
    Stroke('stroke', size, size, [1, 0.8, 0.4])
    Fill('fill', size, size, [1, 0.8, 0.4])
    ShowText('showtext', size, size, [1, 0.8, 0.4])
    Paint('paint', size, size, [1, 0.8, 0.4])
    Mask('mask', size, size, [1, 0.8, 0.4])