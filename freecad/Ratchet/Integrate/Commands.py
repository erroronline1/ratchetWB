# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from ..PySide.QtWidgets import QToolBar
from ..Shapes import Symmetric , Directed
from .Command import Command

from FreeCAD import Qt

translate = Qt.translate

def registerFuseCommands (
    toolbar : QToolBar
):

    Command(
        toolbar = toolbar ,
        shape = Symmetric ,
        key = 'Symmetric',
        name = translate('Command','Symmetric ratchet'),
        boolean = 'fuse'
    )

    Command(
        toolbar = toolbar ,
        shape = Directed ,
        key = 'Directed',
        name = translate('Command','Directed ratchet'),
        boolean = 'fuse'
    )

def registerCutCommands (
    toolbar : QToolBar
):

    Command(
        toolbar = toolbar ,
        shape = Symmetric ,
        key = 'SymmetricCut',
        name = translate('Command','Symmetric ratchet cut'),
        boolean = 'cut'
    )

    Command(
        toolbar = toolbar ,
        shape = Directed ,
        key = 'DirectedCut',
        name = translate('Command','Directed ratchet cut'),
        boolean = 'cut'
    )
