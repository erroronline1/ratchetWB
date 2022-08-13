import math as Math

class DirectedTeeth():
    def __init__(self, properties):
        self.radius = properties['radius']
        self.teeth = properties['teeth']
        self.toothheight = properties['toothheight']
        self.inset = properties['inset']
        self.pad = properties['pad']
        self._calc_directed()

    def _calc_directed(self):
        tooth = Math.pi*2 / self.teeth
        floor=self.radius - self.toothheight
        if self.inset:
            middle=floor + self.toothheight/4
        else:
            middle=floor + self.toothheight/2
        segments=[];
        segments.append({'type': 'p', 'x': Math.sin(0) * floor, 'y': Math.cos(0) * floor, 'z': 0}) # start point line
        for i in range(self.teeth):
            segments.append({'type': 'p', 'x': Math.sin(tooth * i) * self.radius, 'y': Math.cos(tooth * i) * self.radius, 'z': 0}) # end point line, start point arc
            segments.append({'type': 'r', 'x': Math.sin(tooth * (i + .5)) * middle, 'y': Math.cos(tooth * (i + .5)) * middle, 'z': 0}) # arc rim point
            segments.append({'type': 'p', 'x': Math.sin(tooth * (i + 1)) * floor, 'y': Math.cos(tooth * (i + 1)) * floor, 'z': 0}) # end point arc
        self.segments = segments

    def _update(self):
        self._calc_directed()

class DoubleTeeth():
    def __init__(self, properties):
        self.radius = properties['radius']
        self.teeth = properties['teeth']
        self.toothheight = properties['toothheight']
        self.pad = properties['pad']
        self._calc_directed()

    def _calc_directed(self):
        tooth = Math.pi*2 / self.teeth
        floor=self.radius - self.toothheight
        segments=[];
        for i in range(self.teeth):
            segments.append({'type': 'p', 'x': Math.sin(tooth * i) * floor, 'y': Math.cos(tooth * i) * floor, 'z': 0}) # end point
            segments.append({'type': 'p', 'x': Math.sin(tooth * (i +.5)) * self.radius, 'y': Math.cos(tooth * (i +.5)) * self.radius, 'z': 0}) # tip
        self.segments = segments

    def _update(self):
        self._calc_directed()
