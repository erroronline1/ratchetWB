# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from ..PySide.QtWidgets import QToolBar
from ..PySide.QtCore import SIGNAL
from ..PySide.QtGui import QAction , QIcon
from ..Misc import asIcon

from ..Shapes.Directed.View import ViewProvider

from FreeCAD import DocumentObject , activeDocument , GuiUp , Gui , Qt
from typing import Any


translate = Qt.translate

class Command:

    tooltip : str
    shape : Any
    icon : str
    name : str

    def __init__ (
        self ,
        shape : object ,
        toolbar : QToolBar ,
        key : str,
        name: str,
        boolean: str
    ):

        self.shape = shape
        self.icon = asIcon(f'Shapes/{ key }')
        self.boolean = boolean # fuse or cut
        self.name = name

        Tooltip = translate('Command.Tooltip','Generate a {{ Name }}')
        self.tooltip = Tooltip.replace(r'{{ Name }}',self.name)

        Gui.addCommand(f'Ratchet-{ key }',self)

        action = self.action()
        action.setParent(toolbar)
        toolbar.addAction(action)


    def GetResources ( self ):
        return {
            'MenuText' : self.name ,
            'ToolTip' : self.tooltip ,
            'Pixmap' : self.icon
        }


    def Activated ( self ):

        document = activeDocument()

        if not document:
            return

        document.openTransaction(self.tooltip)

        ########################################################################

        if GuiUp:

            view = Gui.activeView()

            body = view.getActiveObject('pdbody')
            part = view.getActiveObject('part')

            type = 'Part::FeaturePython'

            if body:
                type = 'PartDesign::FeaturePython'

            object : DocumentObject = document \
                .addObject(type, self.name)

            view = object.ViewObject

            shape = self.shape(object, self.boolean)

            if view:
                shape.attachView(view)

            if body:
                body.addObject(object)
            elif part:
                part.Group += [ object ]

        else:

            object = document.addObject('Part::FeaturePython',self.name)

            self.shape(object)

        ########################################################################

        document.commitTransaction()
        document.recompute()

        Gui.SendMsgToActiveView('ViewFit')


    def IsActive ( self ):
        return activeDocument() != None

    def action ( self ):

        icon = QIcon( self.icon )

        action = QAction(
            toolTip = self.name ,
            icon = icon
        )

        action.connect(SIGNAL('triggered()'),self.Activated)

        return action