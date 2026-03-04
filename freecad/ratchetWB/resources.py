import os
from importlib import resources
import freecad.ratchetWB as module
import FreeCAD

resourcefiles = resources.files(module) / "resources"

languagePath = os.path.join(
	os.path.dirname(__file__),
	"resources",
	"translations"
)

def icon(name: str):
	"""	returns an icon file path """
	file = name + ".svg"
	iconpath = resourcefiles / file
	with resources.as_file(iconpath) as path:
		return str(path)
