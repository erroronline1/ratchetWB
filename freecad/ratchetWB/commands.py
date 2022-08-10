import FreeCADGui
import os
from . import ICONPATH
from . import tools

class BaseCommand():
	fnParams = None
	FreeCADGui.doCommandGui("import freecad.ratchetWB.commands")

	def __init__(self):
		pass

	def GetResources(self):
		return {'Pixmap': self.pixmap,
				'MenuText': self.menuText,
				'ToolTip': self.toolTip}

	def Activated(self):
		FreeCADGui.doCommandGui(f"freecad.ratchetWB.commands.{self.__class__.__name__}.do('{self.fnParams}')")

	@classmethod
	def do(self, fnParams=None):
		self.function(fnParams)

################################################################################

class ExternalDirected(BaseCommand):
	name = tools.LANG.chunk("ExternalDirectedName")[0]
	function = tools.ExternalDirected
	pixmap = os.path.join(ICONPATH, "icon.svg")
	menuText = tools.LANG.chunk("ExternalDirectedMenuText")[0]
	toolTip = tools.LANG.chunk("ExternalDirectedToolTip")[0]
	def IsActive(self):
		pass

class InternalDirected(BaseCommand):
	name = tools.LANG.chunk("InternalDirectedName")[0]
	function = tools.InternalDirected
	pixmap = os.path.join(ICONPATH, "InternalDirected.svg")
	menuText = tools.LANG.chunk("InternalDirectedMenuText")[0]
	toolTip = tools.LANG.chunk("InternalDirectedToolTip")[0]
	def IsActive(self):
		pass

class ExternalDouble(BaseCommand):
	name = tools.LANG.chunk("ExternalDoubleName")[0]
	function = tools.ExternalDouble
	pixmap = os.path.join(ICONPATH, "ExternalDouble.svg")
	menuText = tools.LANG.chunk("ExternalDoubleMenuText")[0]
	toolTip = tools.LANG.chunk("ExternalDoubleToolTip")[0]
	def IsActive(self):
		pass

class InternalDouble(BaseCommand):
	name = tools.LANG.chunk("InternalDoubleName")[0]
	function = tools.InternalDouble
	pixmap = os.path.join(ICONPATH, "InternalDouble.svg")
	menuText = tools.LANG.chunk("InternalDoubleMenuText")[0]
	toolTip = tools.LANG.chunk("InternalDoubleToolTip")[0]
	def IsActive(self):
		pass
