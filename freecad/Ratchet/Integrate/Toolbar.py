# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from ..PySide.QtWidgets import QMainWindow , QToolBar
from ..PySide.QtCore import QTimer

from ..Misc.Document import DocumentSwitch
from .Commands import registerFuseCommands, registerCutCommands

from FreeCAD import Gui , Qt , addDocumentObserver


translate = Qt.translate

tooltip = translate('Toolbar','[ Ratchets ]')
title = translate('Toolbar','Ratchet')


PartToolbar = None
PartDesignToolbar = None

timer = QTimer()
timer.setSingleShot(True)

def insertPartToolbar ():

    visible = _activeWorkbench()

    global PartToolbar

    window : QMainWindow = Gui.getMainWindow()

    if not window:
        return

    if not PartToolbar:

        PartToolbar = QToolBar(title)
        PartToolbar.setToolTip(tooltip)
        PartToolbar.setObjectName('Ratchet-Toolbar')

        registerFuseCommands(PartToolbar)

        PartToolbar.setEnabled(False)
        window.addToolBar(PartToolbar)

    PartToolbar.setVisible(visible in ('PartWorkbench') if visible else False)


def insertPartDesignToolbar ():

    visible = _activeWorkbench()

    global PartDesignToolbar

    window : QMainWindow = Gui.getMainWindow()

    if not window:
        return

    if not PartDesignToolbar:

        PartDesignToolbar = QToolBar(title)
        PartDesignToolbar.setToolTip(tooltip)
        PartDesignToolbar.setObjectName('Ratchet-Toolbar')

        registerFuseCommands(PartDesignToolbar)
        registerCutCommands(PartDesignToolbar)

        PartDesignToolbar.setEnabled(False)
        window.addToolBar(PartDesignToolbar)

    PartDesignToolbar.setVisible(visible in ('PartDesignWorkbench') if visible else False)

def _activeWorkbench ():

    global timer

    workbench = Gui.activeWorkbench()

    if not workbench:
        return False

    if not hasattr(workbench,'__Workbench__'):
        timer.start(100)
        return False

    return workbench.name()


timer.timeout.connect(insertPartToolbar)
timer.timeout.connect(insertPartDesignToolbar)



window = Gui.getMainWindow()
window.workbenchActivated.connect(insertPartToolbar)
window.workbenchActivated.connect(insertPartDesignToolbar)


from FreeCAD import activeDocument


def update ():

    global PartToolbar
    global PartDesignToolbar

    if not PartToolbar:
        return

    enabled = not not activeDocument()

    PartToolbar.setEnabled(enabled)
    PartDesignToolbar.setEnabled(enabled)


observer = DocumentSwitch(update)

addDocumentObserver(observer)