# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from ...Misc import asIcon
from ...Panels.TaskPanel import TaskPanel

from FreeCAD import Gui

ViewProvider = Gui.ViewProviderDocumentObject


class ViewProxy:

    __module__ = 'Virtual.Ratchet.Proxy.ViewProvider'
    __name__ = 'Directed'

    def __init__( self , view : ViewProvider ):
        view.Proxy = self

    def attach ( self , view : ViewProvider ):
        self.ViewObject = view
        self.Object = view.Object

    def updateData ( self , fp , prop ):
        pass

    def onChanged( self , vobj , prop ):
        pass

    def getIcon ( self ):
        if self.Object.Proxy.boolean == 'cut':
            return asIcon(f'Shapes/DirectedCut')
        return asIcon(f'Shapes/Directed')

    def loads ( self , state ):
        pass

    def dumps ( self ):
        return None

    def setEdit(self, object, mode=0):
        obj = object.Object
        ui = TaskPanel(obj)
        Gui.Control.showDialog(ui)
        return True

    def unsetEdit(self, object, mode):
        Gui.Control.closeDialog()
        return

    def doubleClicked(self,object):
        self.setEdit(object)
