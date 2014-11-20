#!/usr/bin/python

import pygame
from pygame.locals import *
from pygame.color import THECOLORS
from openni import *
import numpy
import cv
import sys

XML_FILE = 'config.xml'
MAX_DEPTH_SIZE = 10000

context = Context()
context.init_from_xml_file(XML_FILE)

depth_generator = DepthGenerator()
depth_generator.create(context)

image_generator = ImageGenerator()
image_generator.create(context)

context.start_generating_all()

pygame.init()

screen = pygame.display.set_mode((1280, 480))
depth_frame = pygame.Surface((640, 480))

grayscale_palette = tuple([(i, i, i) for i in range(256)])

pygame.display.set_caption('Kinect Simple Viewer')

running = True
histogram = None
depth_map = None
image_count = 0
total_time = 0

print "Image dimensions ({full_res[0]}, {full_res[1]})".format(full_res=depth_generator.metadata.full_res)

def calc_histogram():
	global histogram, depth_map
	max_depth = 0
	num_points = 0

	depth_map = numpy.asarray(depth_generator.get_tuple_depth_map())
	reduced_depth_map = depth_map[depth_map != 0]
	reduced_depth_map = reduced_depth_map[reduced_depth_map < MAX_DEPTH_SIZE]

	max_depth = min(reduced_depth_map.max(), MAX_DEPTH_SIZE)

	histogram = numpy.bincount(reduced_depth_map)
	num_points = len(reduced_depth_map)

	for i in xrange(1, max_depth): histogram[i] += histogram[i-1]

	if num_points > 0:
		histogram = 256 * (1.0-(histogram / float(num_points)))
# calc_histogram

def update_depth_image(surface):
	calc_histogram()

	depth_frame = numpy.arange(640*480, dtype=numpy.uint32)
	depth_frame = histogram[depth_map[depth_frame]]
	depth_frame = depth_frame.reshape(480, 640)

	frame_surface = pygame.transform.rotate(pygame.transform.flip(pygame.surfarray.make_surface(depth_frame), True, False), 90)
	frame_surface.set_palette(grayscale_palette)
	surface.blit(frame_surface, (0, 0))
# update_depth_image

def capture_rgb():
	rgb_frame = numpy.fromstring(image_generator.get_raw_image_map_bgr(), dtype=numpy.uint8).reshape(480, 640, 3)
	image = cv.fromarray(rgb_frame)
	cv.CvtColor(cv.fromarray(rgb_frame), image, cv.CV_BGR2RGB)
	pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

	return pyimage
# capture_rgb

while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN and event.key == K_ESCAPE: running = False
	# for

	screen.fill(THECOLORS['white'])
	context.wait_any_update_all()
	cv.WaitKey(10)

	start_time = pygame.time.get_ticks()

	update_depth_image(depth_frame)
	rgb_frame = capture_rgb()

	screen.blit(rgb_frame, (0, 0))
	screen.blit(depth_frame, (640, 0))

	image_count += 1
	total_time += pygame.time.get_ticks() - start_time

	pygame.display.flip()
# while

context.stop_generating_all()
sys.exit(0)