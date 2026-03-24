# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from ..Base import BaseRatchet

from .Properties import defineProperties
from .Document import SymmetricObject
from .Shape import generate

from FreeCAD import Qt , Gui


ViewProvider = Gui.ViewProviderDocumentObject
translate = Qt.translate


class Symmetric ( BaseRatchet ):

    __module__ = 'Virtual.Ratchet.Proxy.Document'
    __name__ = 'Symmetric'

    type = 'Symmetric'

    def __init__ ( self , object : SymmetricObject, boolean: str = "fuse" ):

        super().__init__(object, boolean)

        defineProperties(object)

        object.Depth.Value = 5.0
        object.Count = 15

        object.Radius.Value = 25.0
        object.Height.Value = 5.0

        object.Proxy = self

    def generate ( self , object : SymmetricObject ):
        return generate(object)

    def attachView ( self , view : ViewProvider ):

        from .View import ViewProxy

        ViewProxy(view)