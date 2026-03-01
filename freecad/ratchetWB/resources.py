from importlib import resources
import freecad.ratchetWB as module
import FreeCAD

resourcefiles = resources.files(module) / "resources"


def icon(name: str):
	"""	returns an icon file path """
	file = name + ".svg"
	iconpath = resourcefiles / file
	with resources.as_file(iconpath) as path:
		return str(path)
