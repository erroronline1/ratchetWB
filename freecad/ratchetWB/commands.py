import FreeCAD, FreeCADGui
import os
from . import ICONPATH
from . import tools

class BaseCommand():
    # taken from https://github.com/looooo/freecad.gears
    def __init__(self):
        pass

    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        return True

    def GetResources(self):
        return {'Pixmap': self.pixmap,
                'MenuText': self.menuText,
                'ToolTip': self.toolTip}

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        FreeCADGui.doCommandGui("import freecad.ratchetWB.commands")
        doc.openTransaction(self.toolTip)
        FreeCADGui.doCommandGui(f'freecad.ratchetWB.commands.{self.__class__.__name__}.create()')
        doc.commitTransaction()
        doc.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    @classmethod
    def create(cls):
        if FreeCAD.GuiUp:
            body = FreeCADGui.ActiveDocument.ActiveView.getActiveObject("pdbody")
            part = FreeCADGui.ActiveDocument.ActiveView.getActiveObject("part")

            if body:
                obj = FreeCAD.ActiveDocument.addObject("PartDesign::FeaturePython", cls.name)
            else:
                obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", cls.name)
            ViewRatchet(obj.ViewObject, cls.pixmap)
            cls.function(obj)

            if body:
                body.addObject(obj)
            elif part:
                part.Group += [obj]
        else:
            obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", cls.name)
            cls.function(obj)
        return obj

################################################################################

class ViewRatchet(object):
    # taken from https://github.com/looooo/freecad.gears
    def __init__(self, obj, icon):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self
        self.icon = icon

    def attach(self, vobj):
        self.vobj = vobj

    def getIcon(self):
        return self.icon

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

################################################################################

class Create_Directed(BaseCommand):
    name = tools.LANG.chunk("DirectedName")[0]
    function = tools.Directed
    pixmap = os.path.join(ICONPATH, "icon.svg")
    menuText = tools.LANG.chunk("DirectedMenuText")[0]
    toolTip = tools.LANG.chunk("DirectedToolTip")[0]

class Create_Double(BaseCommand):
    name = tools.LANG.chunk("DoubleName")[0]
    function = tools.Double
    pixmap = os.path.join(ICONPATH, "Double.svg")
    menuText = tools.LANG.chunk("DoubleMenuText")[0]
    toolTip = tools.LANG.chunk("DoubleToolTip")[0]
