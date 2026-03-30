# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from FreeCAD import DocumentObject
from typing import Any
from abc import ABC

from ..Misc import Version


class AttachExtensionPython ( DocumentObject , ABC ):
    def positionBySupport ( self ): ...

class BaseRatchet ():

    boolean = "fuse"
    type : str

    def __init__ ( self , _object, boolean: str = "fuse" ):
        self.boolean = boolean
        pass

    def execute ( self , object : AttachExtensionPython ):

        if not hasattr(object,'positionBySupport'):
            self.extend(object)

        object.positionBySupport()

        shape = self.generate(object)

        if hasattr(object,'BaseFeature') and object.BaseFeature is not None:

            # We're inside a PartDesign Body, thus need
            # to fuse with the base feature ensure the
            # gear is placed correctly before fusing

            shape.Placement = object.Placement

            if self.boolean == 'cut':
                shape = object.BaseFeature.Shape.cut(shape)
            else:
                shape = object.BaseFeature.Shape.fuse(shape)

            shape.transformShape(object.Placement.inverse().toMatrix(),True) # account for setting fp.Shape below moves the shape to fp.Placement, ignoring its previous placement


        object.Shape = shape


    def extend ( self , object : DocumentObject ):
        object.addExtension('Part::AttachExtensionPython')
        object.setEditorMode('Placement',0) # Mutable & Visible

    def generate ( self , object : Any ):
        raise NotImplementedError()

    def defineProperties ( self ,
        object : DocumentObject
    ):

        object.addProperty(
            read_only = True ,
            hidden = True ,
            type = 'App::PropertyString',
            name = 'Version'
        )

        object.addProperty(
            read_only = True ,
            hidden = True ,
            type = 'App::PropertyString',
            name = 'Type'
        )

        setattr(object,'Version',Version)
        setattr(object,'Type',self.type)
