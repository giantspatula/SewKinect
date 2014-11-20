from openni import *

class Kinect(object):
    """Manage context and generator of the kinect"""
    def __init__(self, game):

        self.context = openni.Context()
        self.context.init()
        self.depth_generator = openni.DepthGenerator()
        self.depth_generator.create(self.context)
        self.depth_generator.set_resolution_preset(openni.RES_VGA)
        self.depth_generator.fps = 30

        self.image_generator = openni.ImageGenerator()
        self.image_generator.create(self.context)
        self.image_generator.set_resolution_preset(openni.RES_VGA)
        
        self.gesture_generator = openni.GestureGenerator()
        self.gesture_generator.create(self.context)
        self.gesture_generator.add_gesture('Wave')
        
        self.hands_generator = openni.HandsGenerator()
        self.hands_generator.create(self.context)

        self.gesture_generator.register_gesture_cb(self.gesture_detected, self.gesture_progress)
        self.hands_generator.register_hand_cb(self.create, self.update, self.destroy)

        self.game = game 

   def gesture_detected(src, gesture, id, end_point):
    print "Detected gesture:", gesture
    hands_generator.start_tracking(end_point)
    pygame.quit()
    # gesture_detected

    def gesture_progress(src, gesture, point, progress): 
        pass
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
                

    def capture_rgb(self):
        rgb_frame = np.fromstring(self.image_generator.get_raw_image_map_bgr(), dtype=np.uint8).reshape(SCREEN_HEIGHT, SCREEN_WIDTH, 3)
        image = cv.fromarray(rgb_frame)
        cv.Flip(image, None, 1)
        cv.CvtColor(cv.fromarray(rgb_frame), image, cv.CV_BGR2RGB)
        self.game.frame = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

