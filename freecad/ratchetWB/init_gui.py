import os
from .resources import icon
from . import commands
import FreeCAD, FreeCADGui

trans_path = os.path.join(
	os.path.dirname(__file__),
	"resources",
	"translations"
)

FreeCADGui.addLanguagePath(trans_path)
FreeCADGui.updateLocale()

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

class ratchetWB(FreeCADGui.Workbench):
	"""
		this is the main workbench class that embeds the menu and toolbar buttons with assigned functions
	"""
	MenuText = "Ratchet"
	ToolTip = QT_TRANSLATE_NOOP("ratchetWB", "Create a ratchet")
	Icon = icon("icon")

	def Initialize(self):
		"""
			This function is executed when FreeCAD starts
		"""

		fn = {
			"Create_Directed": commands.Create_Directed(),
			"Create_Symmetrical": commands.Create_Symmetrical()
		}
		self.appendToolbar("Ratchet", list(fn.keys()))
		self.appendMenu("Ratchet", list(fn.keys()))
		for commandname, commandfunction in fn.items():
			FreeCADGui.addCommand(commandname, commandfunction)

	def Activated(self):
		pass

	def Deactivated(self):
		pass

	def ContextMenu(self, recipient):
		# self.appendContextMenu("My commands",self.list) # add commands to the context menu / right click
		pass

	def GetClassName(self): 
		# This function is mandatory if this is a full Python workbench
		# This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
		return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(ratchetWB())
