# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from FreeCAD import Vector , Qt
from typing import TypedDict
from Part import LineSegment , Wire , Face , Arc
from math import sin , cos , pi

from ...Misc import report

from .Document import DirectedObject


translate = Qt.translate


class Point ( TypedDict ):
    axis : Vector
    type : str


def generate (
    object : DirectedObject
):

    tooth_depth = object.Depth.Value
    tooth_count = object.Count
    tooth_curve = object.Curve

    radius = object.Radius.Value
    height = object.Height.Value


    ############################################################################

    if tooth_count < 2 :
        report(f'{ tooth_count } { translate("DirectedTeeth","is not a valid number of teeth. Please use 2+ teeth.") }')
        return

    ############################################################################

    tooth_sector = pi * 2 / tooth_count
    inner_radius = radius - tooth_depth
    middle_radius = inner_radius + tooth_depth * tooth_curve

    ############################################################################

    vectors : list[ Point ] = []

    vectors.append({
        'type' : 'Line' ,
        'axis' : Vector(
            sin(0) * inner_radius ,
            cos(0) * inner_radius ,
            0
        )
    })

    for i in range(tooth_count):

        def vec ( offset : float , radius : float ):
            return Vector(
                sin( tooth_sector * ( i + offset ) ) * radius ,
                cos( tooth_sector * ( i + offset ) ) * radius ,
                0
            )

        tip : Point = {
            'type' : 'Line' ,
            'axis' : vec(0,radius)
        }

        rim  : Point = {
            'type' : 'Arc' ,
            'axis' : vec(.5,middle_radius)
        }

        valley : Point = {
            'type' : 'Line' ,
            'axis' : vec(1,inner_radius)
        }

        vectors.append(tip)
        vectors.append(rim)
        vectors.append(valley)

    ############################################################################

    lines = []
    skip = 1

    for index , current in enumerate(vectors):

        skip -= 1

        if skip > 0:
            continue

        type = current[ 'type' ]

        if type == 'Line' :

            if index < ( len(vectors) - 1 ):
                start = vectors[ index - 1 ]
                end = current
            else:
                start = current
                end = vectors[ 0 ]

            lines.append(
                LineSegment(
                    start[ 'axis' ] ,
                    end[ 'axis' ]
                ).toShape()
            )

            skip = 1

        elif type == 'Arc' :

            before = vectors[ index - 1 ]
            after = vectors[ index + 1 ]

            lines.append(
                Arc(
                    before[ 'axis' ] ,
                    current[ 'axis' ] ,
                    after[ 'axis' ]
                ).toShape()
            )

            skip = 2

    wire = Wire(lines)
    face = Face(wire)

    ############################################################################

    if height == 0 :
        return face

    vector = Vector(0,0,height)

    return face.extrude(vector)

