from datetime import datetime
from .resources import icon
from . import teeth

import FreeCAD, Part

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

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
            'Radius': 25,
            'Teeth': 15,
            'Toothheight': 5,
            'Curve': .5,
            'Pad': 5
        }
        self.ratchet = teeth.DirectedTeeth(properties)

        obj.addProperty("App::PropertyLength", "Radius", QT_TRANSLATE_NOOP("App::Property", "Parameter"), QT_TRANSLATE_NOOP("App::Property", "Outer radius"))
        obj.addProperty("App::PropertyInteger", "Teeth", QT_TRANSLATE_NOOP("App::Property", "Parameter"), QT_TRANSLATE_NOOP("App::Property", "Number of Teeth"))
        obj.addProperty("App::PropertyLength", "Toothheight", QT_TRANSLATE_NOOP("App::Property", "Parameter"), QT_TRANSLATE_NOOP("App::Property", "Tooth height"))
        obj.addProperty("App::PropertyFloat", "Curve", QT_TRANSLATE_NOOP("App::Property", "Parameter"), QT_TRANSLATE_NOOP("App::Property", "Curve"))
        obj.addProperty("App::PropertyLength", "Pad", QT_TRANSLATE_NOOP("App::Property", "Parameter"), QT_TRANSLATE_NOOP("App::Property", "Pad"))
        obj.addProperty("App::PropertyPythonObject", "ratchet", QT_TRANSLATE_NOOP("App::Property", "Parameter"), "ratchet object")

        obj.Radius = f"{properties['Radius']}. mm"
        obj.Teeth = properties['Teeth']
        obj.Toothheight = f"{properties['Toothheight']}. mm"
        obj.Curve = properties['Curve']
        obj.Pad = f"{properties['Pad']}. mm"
        obj.ratchet = self.ratchet
        obj.Proxy = self

    def _generate_ratchet(self, fp):
        fp.ratchet.Radius = fp.Radius
        fp.ratchet.Teeth = fp.Teeth
        fp.ratchet.Toothheight = fp.Toothheight
        fp.ratchet.Curve = fp.Curve
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


class Double(BaseRatchet):
    """ make a freecad object by applying the calculated vector coordinates fro the teeth class """
    def __init__(self, obj):
        super().__init__(obj)
        properties = {
            'Radius': 25,
            'Teeth': 15,
            'Toothheight': 5,
            'Pad': 5
        }
        self.ratchet = teeth.DoubleTeeth(properties)

        obj.addProperty("App::PropertyLength", "Radius", QT_TRANSLATE_NOOP("App::Property", "Parameter"), QT_TRANSLATE_NOOP("App::Property", "Outer radius"))
        obj.addProperty("App::PropertyInteger", "Teeth", QT_TRANSLATE_NOOP("App::Property", "Parameter"), QT_TRANSLATE_NOOP("App::Property", "Number of Teeth"))
        obj.addProperty("App::PropertyLength", "Toothheight", QT_TRANSLATE_NOOP("App::Property", "Parameter"), QT_TRANSLATE_NOOP("App::Property", "Tooth height"))
        obj.addProperty("App::PropertyLength", "Pad", QT_TRANSLATE_NOOP("App::Property", "Parameter"), QT_TRANSLATE_NOOP("App::Property", "Pad"))
        obj.addProperty("App::PropertyPythonObject", "ratchet", QT_TRANSLATE_NOOP("App::Property", "Parameter"), "ratchet object")

        obj.Radius = f"{properties['Radius']}. mm"
        obj.Teeth = properties['Teeth']
        obj.Toothheight = f"{properties['Toothheight']}. mm"
        obj.Pad = f"{properties['Pad']}. mm"
        obj.ratchet = self.ratchet
        obj.Proxy = self

    def _generate_ratchet(self, fp):
        fp.ratchet.Radius = fp.Radius
        fp.ratchet.Teeth = fp.Teeth
        fp.ratchet.Toothheight = fp.Toothheight
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
