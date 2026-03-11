# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from datetime import datetime
from FreeCAD import Console


def report ( msg : str ):

    time = datetime.now().strftime('%H:%M:%S')

    Console.PrintMessage(f'\n{ time } { msg }')
