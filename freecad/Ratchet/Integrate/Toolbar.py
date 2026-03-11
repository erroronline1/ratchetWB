# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from ..PySide.QtWidgets import QMainWindow , QToolBar
from ..PySide.QtCore import QTimer

from ..Misc.Document import DocumentSwitch
from .Commands import registerCommands

from FreeCAD import Gui , Qt , addDocumentObserver


translate = Qt.translate

tooltip = translate('Toolbar','[ Ratchets ]')
title = translate('Toolbar','Ratchet')


toolbar = None


timer = QTimer()
timer.setSingleShot(True)

def insertToolbar ():

    visible = isPartActive()

    global toolbar

    window : QMainWindow = Gui.getMainWindow()

    if not window:
        return

    if not toolbar:

        toolbar = QToolBar(title)
        toolbar.setToolTip(tooltip)
        toolbar.setObjectName('Ratchet-Toolbar')

        registerCommands(toolbar)

        toolbar.setEnabled(False)
        window.addToolBar(toolbar)

    toolbar.setVisible(visible)


def isPartActive ():

    global timer

    workbench = Gui.activeWorkbench()

    if not workbench:
        return False

    if not hasattr(workbench,'__Workbench__'):
        timer.start(100)
        return False

    name = workbench.name()

    return name == 'PartWorkbench'


timer.timeout.connect(insertToolbar)



window = Gui.getMainWindow()
window.workbenchActivated.connect(insertToolbar)


from FreeCAD import activeDocument


def update ():

    global toolbar

    if not toolbar:
        return

    enabled = not not activeDocument()

    toolbar.setEnabled(enabled)


observer = DocumentSwitch(update)

addDocumentObserver(observer)