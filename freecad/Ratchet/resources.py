# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet workbench addon.

import os
from importlib import resources
import freecad.Ratchet as module
import FreeCAD

iconfiles = resources.files(module) / "resources" / "icons"

languagePath = os.path.join(
	os.path.dirname(__file__),
	"resources",
	"translations"
)

def icon(name: str):
	"""	returns an icon file path """
	file = name + ".svg"
	iconpath = iconfiles / file
	with resources.as_file(iconpath) as path:
		return str(path)
