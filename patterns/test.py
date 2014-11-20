import cairo
from PIL import Image

width = 800
height = 600

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
cr = cairo.Context(surface)

# optional conversion from screen to cartesian coordinates:
cr.translate(0, height)
cr.scale(1, -1)

# something very similar to Japanese flag:
cr.set_source_rgb(1,1,1)
cr.rectangle(0, 0, width, height)
cr.fill()
cr.arc(width/2, height/2, 150, 0, 6.28)
cr.set_source_rgb(1,0,0)
cr.fill()

im = Image.frombuffer("RGBA",
                       (width, height),
                       surface.get_data(),
                       "raw",
                       "BGRA",
                       0,1) # don't ask me what these are!
im.show()
# im.save('filename', 'png')