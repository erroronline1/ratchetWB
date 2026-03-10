# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from ..PySide.QtWidgets import QToolBar
from ..Shapes import Symmetric , Directed
from .Command import Command


def registerCommands (
    toolbar : QToolBar
):

    Command(
        toolbar = toolbar ,
        shape = Symmetric ,
        key = 'Symmetric'
    )

    Command(
        toolbar = toolbar ,
        shape = Directed ,
        key = 'Directed'
    )