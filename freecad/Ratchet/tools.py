# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet workbench addon.

from datetime import datetime
from . import teeth

import FreeCAD, Part

translate = FreeCAD.Qt.translate

def report(msg):
    """ (error)-reporting to console """
    now = datetime.now().strftime("%H:%M:%S")
    FreeCAD.Console.PrintMessage(f"\n{now} {msg}")

class BaseRatchet():
    """ taken from https://github.com/looooo/freecad.gears """
    def __init__(self, obj):
        pass

    def make_attachable(self, obj):
        # Needed to make this object "attachable",
        # aka able to attach parameterically to other objects
        # cf. https://wiki.freecadweb.org/Scripted_objects_with_attachment
        if int(FreeCAD.Version()[0]) == 0 and int(FreeCAD.Version()[1]) >= 19 or int(FreeCAD.Version()[0]) == 1:
            obj.addExtension('Part::AttachExtensionPython')
        else:
            obj.addExtension('Part::AttachExtensionPython', obj)
        # unveil the "Placement" property, which seems hidden by default in PartDesign
        obj.setEditorMode('Placement', 0) #non-readonly non-hidden

    def execute(self, fp):
        # checksbackwardcompatibility:
        if not hasattr(fp, "positionBySupport"):
            self.make_attachable(fp)
        fp.positionBySupport()
        ratchet_shape = self._generate_ratchet(fp)
        if hasattr(fp, "BaseFeature") and fp.BaseFeature is not None:
            # we're inside a PartDesign Body, thus need to fuse with the base feature
            ratchet_shape.Placement = fp.Placement # ensure the gear is placed correctly before fusing
            result_shape = fp.BaseFeature.Shape.fuse(ratchet_shape)
            result_shape.transformShape(fp.Placement.inverse().toMatrix(), True) # account for setting fp.Shape below moves the shape to fp.Placement, ignoring its previous placement
            fp.Shape = result_shape
        else:
            fp.Shape = ratchet_shape

    def _generate_ratchet(self, fp):
        # This method has to return the TopoShape of the gear.
        raise NotImplementedError("_generate_ratchet not implemented")

class Directed(BaseRatchet):
    """ make a freecad object by applying the calculated vector coordinates fro the teeth class """
    def __init__(self, obj):
        super().__init__(obj)
        properties = {
            'Outer_radius': 25,
            'Number_of_teeth': 15,
            'Tooth_height': 5,
            'Tooth_curve': .5,
            'Pad': 5
        }
        self.ratchet = teeth.DirectedTeeth(properties)

        obj.addProperty("App::PropertyLength", "Outer_radius", "Parameter", translate("App::Property", "Outer_radius"))
        obj.addProperty("App::PropertyInteger", "Number_of_teeth", "Parameter", translate("App::Property", "Number_of_teeth"))
        obj.addProperty("App::PropertyLength", "Tooth_height", "Parameter", translate("App::Property", "Tooth_height"))
        obj.addProperty("App::PropertyFloat", "Tooth_curve", "Parameter", translate("App::Property", "Tooth_curve"))
        obj.addProperty("App::PropertyLength", "Pad", "Parameter", translate("DirectApp::Propertyed", "Pad"))
        obj.addProperty("App::PropertyPythonObject", "ratchet", "Parameter", "ratchet object")

        obj.Outer_radius = f"{properties['Outer_radius']}. mm"
        obj.Number_of_teeth = properties['Number_of_teeth']
        obj.Tooth_height = f"{properties['Tooth_height']}. mm"
        obj.Tooth_curve = properties['Tooth_curve']
        obj.Pad = f"{properties['Pad']}. mm"
        obj.ratchet = self.ratchet
        obj.Proxy = self

    def _generate_ratchet(self, fp):
        fp.ratchet.Outer_radius = fp.Outer_radius
        fp.ratchet.Number_of_teeth = fp.Number_of_teeth
        fp.ratchet.Tooth_height = fp.Tooth_height
        fp.ratchet.Tooth_curve = fp.Tooth_curve
        fp.ratchet.Pad = fp.Pad
        fp.ratchet._update()

        vector = fp.ratchet.segments
        draft = []
        nextv = 1
        for index, current_vector in enumerate(vector):
            if index < nextv:
                continue
            if current_vector['type'] == 'p':
                if index < (len(vector) - 1):
                    draft.append(Part.LineSegment(  FreeCAD.Vector(vector[index - 1]['x'], vector[index - 1]['y'], vector[index - 1]['z']),
                                                    FreeCAD.Vector(vector[index]['x'], vector[index]['y'], vector[index]['z'])).toShape())
                else:
                    draft.append(Part.LineSegment(  FreeCAD.Vector(vector[index]['x'], vector[index]['y'], vector[index]['z']),
                                                    FreeCAD.Vector(vector[0]['x'], vector[0]['y'], vector[0]['z'])).toShape())
                nextv = index + 1
            elif current_vector['type'] == 'r':
                draft.append(Part.Arc(  FreeCAD.Vector(vector[index - 1]['x'], vector[index - 1]['y'], vector[index - 1]['z']),
                                        FreeCAD.Vector(vector[index]['x'], vector[index]['y'], vector[index]['z']),
                                        FreeCAD.Vector(vector[index + 1]['x'], vector[index + 1]['y'], vector[index + 1]['z'])).toShape())
                nextv = index + 2
        wire = Part.Wire(draft)
        face = Part.Face(wire)
        if fp.ratchet.Pad > 0:
            return face.extrude(FreeCAD.Vector(0, 0, fp.ratchet.Pad))
        return face

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class Symmetrical(BaseRatchet):
    """ make a freecad object by applying the calculated vector coordinates fro the teeth class """
    def __init__(self, obj):
        super().__init__(obj)
        properties = {
            'Outer_radius': 25,
            'Number_of_teeth': 15,
            'Tooth_height': 5,
            'Pad': 5
        }
        self.ratchet = teeth.SymmetricalTeeth(properties)

        obj.addProperty("App::PropertyLength", "Outer_radius", "Parameter", translate("App::Property", "Outer_radius"))
        obj.addProperty("App::PropertyInteger", "Number_of_teeth", "Parameter", translate("App::Property", "Number_of_teeth"))
        obj.addProperty("App::PropertyLength", "Tooth_height", "Parameter", translate("App::Property", "Tooth_height"))
        obj.addProperty("App::PropertyLength", "Pad", "Parameter", translate("App::Property", "Pad"))
        obj.addProperty("App::PropertyPythonObject", "ratchet", "Parameter", "ratchet object")

        obj.Outer_radius = f"{properties['Outer_radius']}. mm"
        obj.Number_of_teeth = properties['Number_of_teeth']
        obj.Tooth_height = f"{properties['Tooth_height']}. mm"
        obj.Pad = f"{properties['Pad']}. mm"
        obj.ratchet = self.ratchet
        obj.Proxy = self

    def _generate_ratchet(self, fp):
        fp.ratchet.Outer_radius = fp.Outer_radius
        fp.ratchet.Number_of_teeth = fp.Number_of_teeth
        fp.ratchet.Tooth_height = fp.Tooth_height
        fp.ratchet.Pad = fp.Pad
        fp.ratchet._update()

        vector = fp.ratchet.segments
        draft = []
        for index, current_vector in enumerate(vector):
            if current_vector['type'] == 'p':
                if index < (len(vector) - 1):
                    draft.append(Part.LineSegment(  FreeCAD.Vector(vector[index]['x'], vector[index]['y'], vector[index]['z']),
                                                    FreeCAD.Vector(vector[index + 1]['x'], vector[index + 1]['y'], vector[index + 1]['z'])).toShape())
                else:
                    draft.append(Part.LineSegment(  FreeCAD.Vector(vector[index]['x'], vector[index]['y'], vector[index]['z']),
                                                    FreeCAD.Vector(vector[0]['x'], vector[0]['y'], vector[0]['z'])).toShape())
        wire = Part.Wire(draft)
        face = Part.Face(wire)
        if fp.ratchet.Pad > 0:
            return face.extrude(FreeCAD.Vector(0, 0, fp.ratchet.Pad))
        return face

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
