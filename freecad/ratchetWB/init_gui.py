from .resources import icon, LANG

import FreeCADGui

class ratchetWB(FreeCADGui.Workbench):
	MenuText = "Ratchet"
	ToolTip = LANG.chunk("wbToolTip")[0]
	Icon = icon("icon")

	commands = [
		"Create_Directed", "Create_Double"]

	def Initialize(self):
		"""This function is executed when FreeCAD starts"""
		from . import commands #, import here all the needed files that create your FreeCAD commands
		self.appendToolbar("Ratchet", self.commands)
		self.appendMenu("Ratchet", self.commands)
		FreeCADGui.addCommand(f"Create_Directed", commands.Create_Directed())
		FreeCADGui.addCommand(f"Create_Double", commands.Create_Double())

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