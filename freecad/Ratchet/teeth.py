import math as Math
from . import tools

import FreeCAD

translate = FreeCAD.Qt.translate

class DirectedTeeth():
    """ vector calculation for a directed ratchet """
    def __init__(self, properties):
        self.Outer_radius = properties['Outer_radius']
        self.Number_of_teeth = properties['Number_of_teeth']
        self.Tooth_height = properties['Tooth_height']
        self.Tooth_curve = properties['Tooth_curve']
        self.Pad = properties['Pad']
        self._calc_directed()

    def _calc_directed(self):
        if self.Number_of_teeth < 2:
            tools.report(f"{self.Number_of_teeth} {translate('DirectedTeeth', 'is not a valid number of teeth. Please use 2+ teeth.')}")
            return
        tooth = Math.pi*2 / self.Number_of_teeth
        floor = self.Outer_radius - self.Tooth_height
        middle = floor + self.Tooth_height* self.Tooth_curve
        segments = []
        segments.append({'type': 'p', 'x': Math.sin(0) * floor, 'y': Math.cos(0) * floor, 'z': 0}) # start point line
        for i in range(self.Number_of_teeth):
            segments.append({'type': 'p', 'x': Math.sin(tooth * i) * self.Outer_radius, 'y': Math.cos(tooth * i) * self.Outer_radius, 'z': 0}) # end point line, start point arc
            segments.append({'type': 'r', 'x': Math.sin(tooth * (i + .5)) * middle, 'y': Math.cos(tooth * (i + .5)) * middle, 'z': 0}) # arc rim point
            segments.append({'type': 'p', 'x': Math.sin(tooth * (i + 1)) * floor, 'y': Math.cos(tooth * (i + 1)) * floor, 'z': 0}) # end point arc
        self.segments = segments

    def _update(self):
        self._calc_directed()

class SymmetricalTeeth():
    """ vector calculation for a symmetrical ratchet """
    def __init__(self, properties):
        self.Outer_radius = properties['Outer_radius']
        self.Number_of_teeth = properties['Number_of_teeth']
        self.Tooth_height = properties['Tooth_height']
        self.Pad = properties['Pad']
        self._calc_directed()

    def _calc_directed(self):
        tooth = Math.pi*2 / self.Number_of_teeth
        floor = self.Outer_radius - self.Tooth_height
        segments=[]
        for i in range(self.Number_of_teeth):
            segments.append({'type': 'p', 'x': Math.sin(tooth * i) * floor, 'y': Math.cos(tooth * i) * floor, 'z': 0}) # end point
            segments.append({'type': 'p', 'x': Math.sin(tooth * (i +.5)) * self.Outer_radius, 'y': Math.cos(tooth * (i +.5)) * self.Outer_radius, 'z': 0}) # tip
        self.segments = segments

    def _update(self):
        self._calc_directed()
