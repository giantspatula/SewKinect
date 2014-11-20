from __future__ import division
from math import pi
import sys

class Measurement():

    def __init__(self, measure, inches):
        self.measure = measure
        self.inch = inches
        self.point = inches*72

    def __repr__(self):
        return "%s measures %d inches and %d points" % (self.measure, self.inch, self.point)

inch_measurements = { 
    "waist": 28,
    "hip": 40,
    "thigh": 24,
    "knee": 18,
    "ankle": 14,
    "waist_to_ankle": 42,
    "ankle_to_knee": 10,
    "knee_to_thigh": 10,
    "front_rise": 8,
    "back_rise": 10,
    "waist_to_hip": 8,
    "waist_to_floor": 42,
    "ease": 1.5
    }

def create_point_measures():
    measures = {}
    for measurement in inch_measurements:
        measures[measurement] = 72*inch_measurements.get(measurement)
    rise_depth = measures["thigh"] - (measures["waist"]/2)
    measures["front_rise_depth"] = rise_depth/3
    measures["back_rise_depth"] = (rise_depth*2)/3
    return measures

    