# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from .Document import DirectedObject

from FreeCAD import Qt


translate = Qt.translate


def defineProperties (
    object : DirectedObject
):

    def property (
        description : str ,
        group : str ,
        type : str ,
        name : str
    ):
        object.addProperty(
            f'App::Property{ type }',
            name , group ,
            description
        )

    ############################################################################

    property(
        description = translate('App::Property','Radius') ,
        group = 'Ratchet' ,
        name = 'Radius' ,
        type = 'Length'
    )

    property(
        description = translate('App::Property','Height') ,
        group = 'Ratchet' ,
        name = 'Height' ,
        type = 'Length'
    )

    ############################################################################

    property(
        description = translate('App::Property','Count') ,
        group = 'Teeth' ,
        name = 'Count' ,
        type = 'Integer'
    )

    property(
        description = translate('App::Property','Depth') ,
        group = 'Teeth' ,
        name = 'Depth' ,
        type = 'Length'
    )

    property(
        description = translate('App::Property','Curve') ,
        group = 'Teeth' ,
        name = 'Curve' ,
        type = 'Float'
    )
