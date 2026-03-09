# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet workbench addon.

from .resources import icon, languagePath
from . import commands
import FreeCAD, FreeCADGui

FreeCADGui.addLanguagePath(languagePath)
FreeCADGui.updateLocale()

class Ratchet(FreeCADGui.Workbench):
	"""
		this is the main workbench class that embeds the menu and toolbar buttons with assigned functions
	"""

	translate = FreeCAD.Qt.translate

	MenuText = "Ratchet"
	ToolTip = translate("Ratchet", "Create a ratchet")
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

FreeCADGui.addWorkbench(Ratchet())
