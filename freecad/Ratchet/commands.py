from .resources import icon
from . import tools

import FreeCAD, FreeCADGui

translate = FreeCAD.Qt.translate

class BaseCommand():
    """
        taken from https://github.com/looooo/freecad.gears
        TMYK: here the commands are defined by child classes, each their own
        * name
        * function
        * pixmap (icon)
        * menu text
        * tooltip

        available commands (classes extending the base command) are initialized with their
        respective properties before FreeCAD calls their methods on interaction.
        basically there is no need to change anything in this class as far as i know
    """
    name = ''
    function = lambda obj: None
    pixmap = ''
    menuText = ''
    toolTip = ''

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
        FreeCADGui.doCommandGui("import freecad.Ratchet.commands")
        doc.openTransaction(self.toolTip)
        FreeCADGui.doCommandGui(f'freecad.Ratchet.commands.{self.__class__.__name__}.create()')
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

class ViewRatchet():
    """ taken from https://github.com/looooo/freecad.gears """
    icon = ''
    def __init__(self, obj, fnicon):
        """ Set this object to the proxy object of the actual view provider """
        obj.Proxy = self
        self.icon = fnicon

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
    name = translate("Create_Directed", "directed ratchet")
    function = tools.Directed
    pixmap = icon("icon")
    menuText = translate("Create_Directed", "directed")
    toolTip = translate("Create_Directed", "directed ratchet")

class Create_Symmetrical(BaseCommand):
    name = translate("Create_Symmetrical", "symmetrical ratchet")
    function = tools.Symmetrical
    pixmap = icon("Double")
    menuText = translate("Create_Symmetrical", "symmetrical")
    toolTip = translate("Create_Symmetrical", "symmetrical ratchet")
