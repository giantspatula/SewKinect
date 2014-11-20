#! /usr/bin/python

from openni import *

def main():
	context = Context()
	context.init()

	depth_generator = DepthGenerator()
	depth_generator.create(context)
	depth_generator.set_resolution_preset(RES_VGA)
	depth_generator.fps = 30

	gesture_generator = GestureGenerator()
	gesture_generator.create(context)
	gesture_generator.add_gesture('Wave')

	hands_generator = HandsGenerator()
	hands_generator.create(context)
	# gesture

	# Register the callbacks
	gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
	hands_generator.register_hand_cb(create, update, destroy)

	# Start generating
	context.start_generating_all()

	print 'Make a Wave to close window...'

	while True:
	    context.wait_any_update_all()
	# while

# Declare the callbacks

def gesture_detected(src, gesture, id, end_point):
    print "Detected gesture:", gesture
    hands_generator.start_tracking(end_point)
    pygame.quit()
# gesture_detected

def gesture_progress(src, gesture, point, progress): pass
# gesture_progress

def create(src, id, pos, time):
    print 'Create ', id, pos
# create

def update(src, id, pos, time):
    print 'Update ', id, pos
# update

def destroy(src, id, time):
    print 'Destroy ', id
# destroy