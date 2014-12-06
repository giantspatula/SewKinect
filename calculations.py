
from openni import *
import numpy as np
import json
from numpy.linalg import eig, inv
from scipy.special import hyp2f1
from math import sqrt, atan2, cos, asin, tan
from math import pi as M_PI

class CalculationObject():

	def __init__(self, point_cloud, body_parts):
		self.angles = {}
		self.torso = {}
		self.body_parts = body_parts
		self.point_cloud = point_cloud
		self.crossections = {}
		self.default = {"size":16,
"waist":698.5,
"hip":977.9,
"thigh":571.5,
"waistToHip":211.836,
"waistToKnee":581.025,
"waistToFloor":1022.35,
"girth":746.125
}
		self.measures = {"size":"kinect",
"waist":0,
"hip":0,
"thigh":0,
"waistToHip":0,
"waistToKnee":0,
"waistToFloor":0
}

###### ------------------- Utility Methods ------------------- ######

	def to_real_world(self, point):
		""" converts a point[x, y, z] to a real world point as described at 
		http://www.gurucycling.com/wp-content/uploads/2013/09/Kinect-for-Positional-Data-Acquisition.pdf"""
		x = point[0]
		y = point[1]
		z = point[2]

		z_meters = z/1000.0
		x_meters = 6 - 2*(x - 639/2.0)*tan(57/2.0)*(z_meters/640.0)
		y_meters = 4.5 - 2*(479 - y - 479/2.0)*tan(43/2.0)*(z_meters/480)

		point[0] = 1000*x_meters
		point[1] = 1000*y_meters

		return point

	def save_JSON(self):
		"""saves self.measures in .JSON format to a file"""
		with open('kinect.JSON', 'w') as outfile:
  				json.dump(self.measures, outfile)

  	def convert_measures_to_inches(self):
  		""" conversts the caclulationObject measures dictionary to inches"""
  		for key in self.measures:
  			if key is not "size":
  				self.measures[key] = self.measures[key]*0.0393701
  		self.measures["girth"] = self.measures["hip"]*.75

###### ------------------- Angular Skeleton ------------------- ######

	def calc_joint_angles(self):
		""" takes a skeleton capture and returns a dictionary of joint poistions by angular representation """

		neck = self.body_parts["neck"]
		torso = self.body_parts["torso"]
		left_shoulder = self.body_parts["left_shoulder"]
		right_shoulder = self.body_parts["right_shoulder"]

	#  - u should be the first principal component, aligned with the longer 
	#		dimension of the torso, and should be pointing down.
	#  - v is the second principal component, aligned with the line
	# 		that connectes the shoulders, and pointing in the left-right shoulder direction.
	#  - w should be the cross product of the first two principal
	# 		 components.

		# u = unit_vector(neck - torso)
		# v = unit_vector(right shoulder - left shoulder) 
		# w = unit_vector(cross product of u, v)

		#should be pointing down 
		u = np.array([neck[0]-torso[0], neck[1]-torso[1], 
						neck[2]-torso[2]])
		u = self.unit_vector(u)
		#I may have reversed this, need to check. Should point left--->right
		v = np.array([right_shoulder[0]-left_shoulder[0], 
						right_shoulder[1]-left_shoulder[1], 
						right_shoulder[2]-left_shoulder[2]])
		v = self.unit_vector(v)
		w = np.cross(u, v)
		w = self.unit_vector(w)

		#adding these to class dictionary because I need them later
		self.torso["u"] = u
		self.torso["v"] = v
		self.torso["w"] = w

		# #euler angles given by rotation of {u, v, w}
		# this is technically to calculate whether a user is facing forward
		# or backwards. As of 11/24, I do not need this since I am only
		# taking information from the front.
		# length_u = self.vector_length(u)
		# length_v = self.vector_length(v)

		# if w[0] != 1 and w[0] != -1:
		# 	pitch = -asin(w[0])
		# 	x = cos(pitch)
		# 	yaw = atan2(w[1]/x, w[2]/x)
		# 	roll = atan2(v[0]/x, u[0]/x)
		# else:
		# 	roll = 0
		# 	if w[0] == -1:
		# 		pitch = M_PI/2.0
		# 		yaw = atan2(u[1], u[2])

		# 	else:
		# 		pitch = -M_PI/2.0
		# 		yaw = atan2(-u[1], -u[2])
		
		# # #convert to degrees and add to instances' dictionary	
		# self.angles["TORSO_YAW"] = yaw *(180/M_PI) 
		# self.angles["TORSO_PITCH"] = pitch*(180/M_PI)
		# self.angles["TORSO_ROLL"] = roll*(180/M_PI) 


###### ------------------- Body Measure Calculations ------------------- ######

	def calc_lengths(self):
		waist = self.body_parts["waist"]
		hip = self.body_parts["left_hip"]
		knee = self.body_parts["knee"]
		foot = self.body_parts["foot"]

		waistToHip = np.array([waist[0]-hip[0], waist[1]-hip[1], 
						waist[2]-hip[2]])
		waistToKnee = np.array([waist[0]-knee[0], waist[1]-knee[1], 
						waist[2]-knee[2]])
		waistToFloor = np.array([waist[0]-foot[0], waist[1]-foot[1], 
						waist[2]-foot[2]])

		self.measures["waistToHip"] = self.vector_length(waistToHip)
		self.measures["waistToKnee"] = self.vector_length(waistToKnee)
		self.measures["waistToFloor"] = self.vector_length(waistToFloor)

	def calc_girths(self):
		self.calc_crossections()

		for plane in self.crossections:
			good_points = self.points_on_a_plane(self.crossections[plane], self.point_cloud)
			if good_points:
				ellipse = self.fit_ellipse(good_points)
				axis = self.ellipse_axis_length(ellipse)
				if plane == 'hip':
					self.measures[plane] = 2*M_PI*(axis[0])
				else:
					self.measures[plane] = self.approx_measure(axis)
			else:
				self.measure[plane] = self.default[plane]

###### ----------------- Crossection Calculations --------------------- ######

	def calc_crossections(self):
		""" takes a user id, and skeleton capture """
		
		self.crossections["waist"] = self.calc_waist()
		self.crossections["hip"] = self.calc_hip()
		self.crossections["thigh"] = self.calc_thigh()

	def calc_waist(self):
		""" returns O, N, x, y vectors that define the planar crossection at the waist """
		waist = {}
		middle = self.body_parts["torso"]
		waist["O"] = np.array([middle[0], middle[1], middle[2]])
		waist["N"] = self.torso["u"]
		waist["x"] = self.torso["v"]
		waist["y"] = self.torso["w"]
		return waist

	def calc_chest(self):
		""" returns O, N, x, y vectors that define the planar crossection at the chest """
		print "Got to calc.calc_chest"
		chest = {}
		torso = self.body_parts["torso"]
		neck = self.body_parts["neck"]
		chest["O"] = np.array([neck[0]+torso[0], 
					neck[1]+torso[1], neck[2]+torso[2]])*0.5
		chest["N"] = self.torso["u"]
		chest["x"] = self.torso["v"]
		chest["y"] = self.torso["w"]
		return chest 

	def calc_hip(self):
		""" returns O, N, x, y vectors that define the planar crossection at the hip """
		hip = {}
		left_hip = self.body_parts["left_hip"]
		right_hip = self.body_parts["right_hip"]
		hip["O"] = np.array([left_hip[0]+right_hip[0], left_hip[1]+right_hip[1],
				 left_hip[2]+right_hip[2]])*0.5
		hip["N"] = self.torso["u"]
		hip["x"] = self.torso["v"]
		hip["y"] = self.torso["w"]
		return hip

	def calc_thigh(self):
		""" returns O, N, x, y vectors that define the planar crossection at the thigh """
		thigh = {}
		left_hip = self.body_parts["left_hip"]
		left_knee = self.body_parts["knee"]
		thigh["O"] = np.array([left_hip[0]+left_knee[0], left_hip[1]+left_knee[1],
				 left_hip[2]+left_knee[2]])*0.5
		thigh["N"] = self.unit_vector(np.array([left_knee[0]-left_hip[0], left_knee[1]-left_hip[1],
				 left_knee[2]-left_hip[2]]))
		thigh["x"] = self.torso["v"]
		thigh["y"] = self.torso["w"]
		return thigh 

	def snakes_on_a_plane(self):
		return "This is a joke."

	def points_on_a_plane(self, plane, point_cloud):
		""" takes a joint plane and returns a list of points from the point_cloud that intersect that plane 
		correct usage is points_on_a_plane(waist, front_and_back_cloud) 
		all joint planes are assumed be dictionaries with "O", "N", "x", "y" pointing to vectors 
		point_cloud is a list of lists"""

		# a point is a good point if it is within some distance e of the plane defined by a point O and normal N
		projected_x = []
		projected_y = []
		count = 1

		#starting test value for e 
		for epsilon in range(5,100,5):
			count += 1
			O = plane["O"]
			for point in point_cloud:
				point = np.array(point)
				temp = point - O 
				size = self.vector_length(temp)
				# if size > 200:
				#  	continue
				dot_product = np.dot(temp, plane["N"])
				abs_dot = abs(dot_product)
				if abs_dot < epsilon:
					temp = temp - abs_dot*plane["N"];
					projected_x.append(np.dot(temp, plane["x"]))
					projected_y.append(np.dot(temp, plane["y"]))
			if len(projected_x) > 0:
				good_points = [np.array(projected_x), np.array(projected_y)]
				return good_points

		#returns the good points on that plane with x&y coordinates relative to that plane 
		
		#print "Good points:", good_points[0], good_points[1]
		print "No good points!"
		return False

###### ---------------- Sanity Checks -------------------- ######
		
	def waist_across(self, id, skel_cap, point_cloud):
		waist = skel_cap.get_joint_position(id, SKEL_TORSO)
		print point_cloud
		good_points = []
		y = waist.point[1]
		print "Y:", y
		#list of all points at the y value of waist 
		for point in point_cloud:
			if abs(point[1] - y) < 20:
				xy_point = [point[0], point[1]]
				good_points.append(point)

		#find min x point
		minX = good_points[0][0]
		for point in good_points:
			if point[0] < minX:
				minX = point[0]
		#find max x point
		maxX = good_points[0][0]
		for point in good_points:
			if point[0] > maxX:
				maxX = point[0]
		return abs(minX - maxX)

	def chest_across(self, id, skel_cap, point_cloud):
		torso = skel_cap.get_joint_position(id, SKEL_TORSO)
		neck = skel_cap.get_joint_position(id, SKEL_NECK)
		chest = np.array([neck.point[0]+torso.point[0], 
					neck.point[1]+torso.point[1], neck.point[2]+torso.point[2]])*.5
		print point_cloud
		good_points = []
		y = chest[1]
		print "Y:", y
		#list of all points at the y value of chest 
		for point in point_cloud:
			if abs(point[1] - y) < 20:
				xy_point = [point[0], point[1]]
				good_points.append(point)

		#find min x point
		minX = good_points[0][0]
		for point in good_points:
			if point[0] < minX:
				minX = point[0]
		#find max x point
		maxX = good_points[0][0]
		for point in good_points:
			if point[0] > maxX:
				maxX = point[0]
		return abs(minX - maxX)

###### ---------------- Geometry ---------------------- ######

	def unit_vector(self, array):
		""" converts an numpy array into a unit vector """ 
		length = self.vector_length(array)
		x = array[0]/length
		y = array[1]/length
		z = array[2]/length

		return np.array([x, y, z])

	def vector_length(self, array):
		""" returns legnth of a vector represented by a numpy array """
		length = np.sqrt(array[0]*array[0] + array[1]*array[1] + array[2]*array[2])
		return length

	def calc_circle(self, good_points):
		x, y = good_points 
		minx = np.amin(x)
		maxx = np.amax(x)
		miny = np.amin(y)
		maxy = np.amin(y)

	def fit_ellipse(self, good_points):
		"""code from http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html"""
		x = good_points[0]
		y = good_points[1]
		x = x[:,np.newaxis]
		y = y[:,np.newaxis]
		D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
		S = np.dot(D.T,D)
		C = np.zeros([6,6])
		C[0,2] = C[2,0] = 2; C[1,1] = -1
		E, V =  eig(np.dot(inv(S), C))
		n = np.argmax(np.abs(E))
		a = V[:,n]
		#returns a, an array representation of an ellipse
		return a 

	def ellipse_center(self, a):
		"""code from http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html"""	
		b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
		num = b*b-a*c
		x0=(c*d-b*f)/num
		y0=(a*f-b*d)/num
		return np.array([x0,y0])

	def ellipse_angle_of_rotation(self, a):
		"""code from http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html"""
		b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
		return 0.5*np.arctan(2*b/(a-c))

	def ellipse_axis_length(self, a):
		"""code from http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html"""
		b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
		up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
		down1=(b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
		down2=(b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
		res1=np.sqrt(abs(up/down1))
		res2=np.sqrt(abs(up/down2))
		return np.array([res1, res2])

	def exact_measure(self, array):
		""" approdimentation of permiter of ellipse defined by a np array
		axis1 = array[0]
		axis2 = array[1] """
		a = array[0]
		b = array[1]
		t = ((a-b)/(a+b))**2
		return M_PI*(a+b)*hyp2f1(-0.5, -0.5, 1, t)
 
	def approx_measure(self, array):
		""" approdimentation of permiter of ellipse defined by a np array
		axis1 = array[0]
		axis2 = array[1] """
		a = array[0]
		b = array[1]
		t = ((a-b)/(a+b))**2
		return M_PI*(a+b)*(1 + 3*t/(10 + sqrt(4 - 3*t)))

###### -------------------------------------- ######


