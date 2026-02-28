import freecad.ratchetWB as module
from importlib import resources
import json
import FreeCAD

resourcefiles = resources.files(module) / "resources"


def icon(name: str):
	"""	returns an icon file path """
	file = name + ".svg"
	icon = resourcefiles / file
	with resources.as_file(icon) as path:
		return str(path)
