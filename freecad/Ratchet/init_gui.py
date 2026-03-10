# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from .Misc import Paths

from FreeCAD import Gui


Gui.addLanguagePath(str(Paths[ 'Locales' ]))

Gui.updateLocale()


import freecad.Ratchet.Integrate.Toolbar