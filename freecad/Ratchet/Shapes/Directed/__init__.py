# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from ..Base import BaseRatchet

from .Properties import defineProperties
from .Document import DirectedObject
from .Shape import generate

from ...Misc import report

from FreeCAD import Qt , Gui


ViewProvider = Gui.ViewProviderDocumentObject
translate = Qt.translate


class Directed ( BaseRatchet ):

    __module__ = 'Virtual.Ratchet.Proxy.Document'
    __name__ = 'Directed'

    type = 'Directed'

    def __init__ ( self , object : DirectedObject ):

        super().__init__(object)

        defineProperties(object)

        object.Depth.Value = 5.0
        object.Count = 15
        object.Curve = .5

        object.Radius.Value = 25.0
        object.Height.Value = 5.0

        object.Proxy = self

    def generate ( self , object : DirectedObject ):
        result = generate(object)
        if result is None:
            report(f'{ object.Count } { translate("DirectedTeeth","is not a valid number of teeth. Please use 2+ teeth.") }')
        return result

    def attachView ( self , view : ViewProvider ):

        from .View import ViewProxy

        ViewProxy(view)