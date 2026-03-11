# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from FreeCAD import Vector
from Part import LineSegment , Wire , Face
from math import sin , cos , pi

from .Document import SymmetricObject


def generate (
    object : SymmetricObject
):

    tooth_depth = object.Depth.Value
    tooth_count = object.Count

    radius = object.Radius.Value
    height = object.Height.Value

    ############################################################################

    tooth_sector = pi * 2 / tooth_count
    inner_radius = radius - tooth_depth

    ############################################################################

    vectors = []

    for i in range( tooth_count ):

        valley = Vector(
            sin( tooth_sector * i ) * inner_radius ,
            cos( tooth_sector * i ) * inner_radius ,
            0
        )

        tip = Vector(
            sin( tooth_sector * ( i + .5 ) ) * radius ,
            cos( tooth_sector * ( i + .5 ) ) * radius ,
            0
        )

        vectors.append(valley)
        vectors.append(tip)

    ############################################################################

    lines = []

    for index , current in enumerate(vectors):

        follow = ( index + 1 ) % len( vectors )

        follow = vectors[ follow ]

        line = LineSegment(current,follow)

        lines.append( line.toShape() )

    wire = Wire(lines)
    face = Face(wire)

    ############################################################################

    if height == 0 :
        return face

    vector = Vector(0,0,height)

    return face.extrude(vector)

