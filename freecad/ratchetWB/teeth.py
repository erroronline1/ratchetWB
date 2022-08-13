import math as Math

class DirectedTeeth():
    def __init__(self, properties):
        self.Radius = properties['Radius']
        self.Teeth = properties['Teeth']
        self.Toothheight = properties['Toothheight']
        self.Inset = properties['Inset']
        self.Pad = properties['Pad']
        self._calc_directed()

    def _calc_directed(self):
        tooth = Math.pi*2 / self.Teeth
        floor=self.Radius - self.Toothheight
        if self.Inset:
            middle=floor + self.Toothheight/4
        else:
            middle=floor + self.Toothheight/2
        segments=[];
        segments.append({'type': 'p', 'x': Math.sin(0) * floor, 'y': Math.cos(0) * floor, 'z': 0}) # start point line
        for i in range(self.Teeth):
            segments.append({'type': 'p', 'x': Math.sin(tooth * i) * self.Radius, 'y': Math.cos(tooth * i) * self.Radius, 'z': 0}) # end point line, start point arc
            segments.append({'type': 'r', 'x': Math.sin(tooth * (i + .5)) * middle, 'y': Math.cos(tooth * (i + .5)) * middle, 'z': 0}) # arc rim point
            segments.append({'type': 'p', 'x': Math.sin(tooth * (i + 1)) * floor, 'y': Math.cos(tooth * (i + 1)) * floor, 'z': 0}) # end point arc
        self.segments = segments

    def _update(self):
        self._calc_directed()

class DoubleTeeth():
    def __init__(self, properties):
        self.Radius = properties['Radius']
        self.Teeth = properties['Teeth']
        self.Toothheight = properties['Toothheight']
        self.Pad = properties['Pad']
        self._calc_directed()

    def _calc_directed(self):
        tooth = Math.pi*2 / self.Teeth
        floor=self.Radius - self.Toothheight
        segments=[];
        for i in range(self.Teeth):
            segments.append({'type': 'p', 'x': Math.sin(tooth * i) * floor, 'y': Math.cos(tooth * i) * floor, 'z': 0}) # end point
            segments.append({'type': 'p', 'x': Math.sin(tooth * (i +.5)) * self.Radius, 'y': Math.cos(tooth * (i +.5)) * self.Radius, 'z': 0}) # tip
        self.segments = segments

    def _update(self):
        self._calc_directed()
