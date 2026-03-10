# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

import freecad.Ratchet as module
from importlib.resources import as_file , files


resources = files(module) / 'Resources'

locales = resources / 'Locales'
icons = resources / 'Icons'


Paths = {
    'Locales' : locales
}


def asIcon ( name : str ):

    file = name + '.svg'

    icon = icons / file

    with as_file(icon) as path:
        return str( path )