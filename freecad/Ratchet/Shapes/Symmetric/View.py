# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from ...Misc import asIcon

from FreeCAD import Gui


ViewProvider = Gui.ViewProviderDocumentObject


class ViewProxy:

    __module__ = 'Virtual.Ratchet.Proxy.ViewProvider'
    __name__ = 'Symmetric'

    def __init__( self , view : ViewProvider ):
        view.Proxy = self

    def attach ( self , view : ViewProvider ):
        pass

    def updateData ( self , fp , prop ):
        pass

    def onChanged( self , vobj , prop ):
        pass

    def getIcon ( self ):
        return asIcon(f'Shapes/Symmetric')

    def loads ( self , state ):
        pass

    def dumps ( self ):
        return None