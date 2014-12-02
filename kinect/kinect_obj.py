from openni import *
import pygame 
import pickle
import json
import urllib
import httplib
import os
import numpy as np
from cv2 import cv

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Kinect(object):
    """Manage context and generator of the kinect"""
    def __init__(self, game):

        self.MAX_DEPTH_SIZE = 10000
        self.POSE_TO_USE = 'Psi'
        self.calibrated = False
        self.point_cloud = None
        self.current_user = 0

        self.context = Context()
        self.context.init()

        self.image_generator = ImageGenerator()
        self.image_generator.create(self.context)
        self.image_generator.set_resolution_preset(RES_VGA)

        self.depth_generator = DepthGenerator()
        self.depth_generator.create(self.context)
        self.depth_generator.set_resolution_preset(RES_VGA)
        self.depth_generator.alternative_view_point_cap.set_view_point(self.image_generator)
        self.depth_generator.fps = 30

        self.gesture_generator = GestureGenerator()
        self.gesture_generator.create(self.context)
        self.gesture_generator.add_gesture('Wave')

        self.user = UserGenerator()
        self.user.create(self.context)
        self.user.alternative_view_point_cap.set_view_point(self.image_generator)

        self.skel_cap = self.user.skeleton_cap
        self.pose_cap = self.user.pose_detection_cap
        
        self.hands_generator = HandsGenerator()
        self.hands_generator.create(self.context)

        self.gesture_generator.register_gesture_cb(self.gesture_detected, self.gesture_progress)
        self.hands_generator.register_hand_cb(self.create, self.update, self.destroy)
        self.user.register_user_cb(self.new_user, self.lost_user)
        self.pose_cap.register_pose_detected_cb(self.front_pose_detected)
        self.skel_cap.register_c_start_cb(self.calibration_start)
        self.skel_cap.register_c_complete_cb(self.calibration_complete)

        self.skel_cap.set_profile(SKEL_PROFILE_ALL)

        self.game = game

    def new_user(self, src, id):
        print "User detected! Looking for pose..."
        self.pose_cap.start_detection(self.POSE_TO_USE, id)

    def front_pose_detected(self, src, pose, id):
        print "Detected pose! Requesting calibration..."
        self.pose_cap.stop_detection(id)
        self.skel_cap.request_calibration(id, True)

    def calibration_start(self, src, id):
        print "Calibration started for user..."

    def calibration_complete(self, src, id, status):
        if status == CALIBRATION_STATUS_OK:
            print "User calibrated successfully! Starting to track."
            print '\a'
            self.skel_cap.start_tracking(id)
            self.calibrated = True
            self.current_user = id
        else:
            print "ERR User {} failed to calibrate. Restarting process." .format(id)
            self.new_user(self.user, id)

    def lost_user(self, src, id):
        print "--- User lost!"

    def gesture_detected(self, src, gesture, id, end_point):
        print "Detected gesture:", gesture
        self.hands_generator.start_tracking(end_point)
        self.game._running = False
    # gesture_detected

    def gesture_progress(self, src, gesture, point, progress): 
        pass
    # gesture_progress

    def create(self, src, id, pos, time):
        print 'Create ', id, pos
    # create

    def update(self, src, id, pos, time):
        print 'Update ', id, pos
    # update

    def destroy(self, src, id, time):
        print 'Destroy ', id
    # destroy

    def get_real_world_by_user_pixels(self, id):
        user_pixels = np.asarray(self.user.get_user_pixels(id)).reshape(480, 640)
        point_map = []
        depth_map = np.asarray(self.depth_generator.get_tuple_depth_map()).reshape(480, 640)

        for y in range(0, 480): #numpy arrays are backwards
            for x in range(0, 640): 
                if user_pixels[y][x] == 1:
                    z = depth_map[y][x]
                    if z != 0 and z < self.MAX_DEPTH_SIZE:
                        point = [int(x), int(y), float(z)]
                        point_map.append(point)

        point_map = self.depth_generator.to_real_world(point_map)
        return point_map
                
    def capture_rgb(self):
        rgb_frame = np.fromstring(self.image_generator.get_raw_image_map_bgr(), dtype=np.uint8).reshape(SCREEN_HEIGHT, SCREEN_WIDTH, 3)
        image = cv.fromarray(rgb_frame)
        cv.Flip(image, None, 1)
        cv.CvtColor(cv.fromarray(rgb_frame), image, cv.CV_BGR2RGB)
        self.game.frame = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')


class Game(object):
    """Define screen, sprites and states of the game"""
    def __init__(self):
        self.timer = pygame.time.Clock()
        self.sprites = pygame.sprite.RenderUpdates()
        self._running = True
        self.display_surf = None
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((0,0,0))
        self.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.frame = None
        self.my_kinect = Kinect(self)
        self.scan = 0
        self.sound =  None
        pygame.mixer.pre_init(44100, -16, 2, 2048)

    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.display_surf.blit(self.background, (0,0))
        self._running = True
        self.my_kinect.context.start_generating_all()
        self.sound = pygame.mixer.Sound(os.path.join('sounds','OOT_Secret_Mono.wav'))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):        
        self.my_kinect.context.wait_any_update_all()
        if self.my_kinect.calibrated == True and self.scan < 30:
            point_cloud = self.my_kinect.get_real_world_by_user_pixels(self.my_kinect.current_user)
            self.scan += 1
            print "Point cloud #%d! %d points!" % (self.scan, len(point_cloud))
            if len(point_cloud) > 32000:
                self.my_kinect.calibrated = False
                s_point_cloud = pickle.dumps(point_cloud)
                skel_cap = self.my_kinect.skel_cap
                neck = np.asarray(self.my_kinect.skel_cap.get_joint_position(self.my_kinect.current_user, SKEL_NECK).point)
                torso = np.asarray(self.my_kinect.skel_cap.get_joint_position(self.my_kinect.current_user, SKEL_TORSO).point)
                left_shoulder = np.asarray(self.my_kinect.skel_cap.get_joint_position(self.my_kinect.current_user, SKEL_LEFT_SHOULDER).point)
                right_shoulder = np.asarray(self.my_kinect.skel_cap.get_joint_position(self.my_kinect.current_user, SKEL_RIGHT_SHOULDER).point)
                waist = np.asarray(self.my_kinect.skel_cap.get_joint_position(self.my_kinect.current_user, SKEL_TORSO).point)
                left_hip = np.asarray(self.my_kinect.skel_cap.get_joint_position(self.my_kinect.current_user, SKEL_LEFT_HIP).point)
                right_hip = np.asarray(self.my_kinect.skel_cap.get_joint_position(self.my_kinect.current_user, SKEL_RIGHT_HIP).point)
                knee = np.asarray(self.my_kinect.skel_cap.get_joint_position(self.my_kinect.current_user, SKEL_LEFT_KNEE).point)
                foot = np.asarray(self.my_kinect.skel_cap.get_joint_position(self.my_kinect.current_user, SKEL_RIGHT_FOOT).point)
                body_parts = {"neck": neck,
                "torso": torso,
                "left_shoulder": left_shoulder,
                "right_shoulder": right_shoulder,
                "waist": waist,
                "left_hip": left_hip,
                "right_hip": right_hip,
                "knee": knee,
                "foot": foot,
                }
                s_body_parts = pickle.dumps(body_parts)
                params = urllib.urlencode({"body_parts": base64.b64encode(s_body_parts), 
                    "point_cloud": base64.b64encode(s_point_cloud)})
                headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"}
                conn = httplib.HTTPConnection("localhost:5000")
                conn.request('POST', "/calculate", params, headers)
                response = conn.getresponse()
                print response.status, response.reason
                data = response.read()
                conn.close()
                sound.play()
        self.my_kinect.capture_rgb()

    def on_render(self):
        self.sprites.clear(self.display_surf, self.background)
        self.display_surf.blit(self.frame, (0,0))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        self.on_init()
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == '__main__':
    theApp = Game()
    theApp.on_execute()

