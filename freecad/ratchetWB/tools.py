import os
from datetime import datetime
import json
import FreeCAD, Part
from . import LANGUAGEPATH
from . import teeth

def report(msg):
    now = datetime.now().strftime("%H:%M:%S")
    FreeCAD.Console.PrintMessage(f"\n{now} {msg}")

class language:
    def __init__(self):
        try:
            '''load settings'''
            with open(f'{os.path.join(LANGUAGEPATH, FreeCAD.ParamGet("User parameter:BaseApp/Preferences/General").GetString("Language"))}.json', 'r') as jsonfile:
                self.language = json.loads(jsonfile.read().replace('\n', ''))
        except:
            with open(f'{os.path.join(LANGUAGEPATH, "English")}.json', 'r') as jsonfile:
                self.language = json.loads(jsonfile.read().replace('\n', ''))
    def chunk(self, chunk):
        return self.language[chunk]
LANG = language()

class BaseRatchet(object):
    # taken from https://github.com/looooo/freecad.gears
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
        if hasattr(fp, "BaseFeature") and fp.BaseFeature != None:
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
    def __init__(self, obj):
        super(Directed, self).__init__(obj)
        properties = {
            'Radius': 25,
            'Teeth': 15,
            'Toothheight': 5,
            'Curve': .5,
            'Pad': 5
        }
        self.ratchet = teeth.DirectedTeeth(properties)

        obj.addProperty("App::PropertyLength", "Radius", LANG.chunk("PropertyTitle")[0], LANG.chunk("PropertyRadius")[0])
        obj.addProperty("App::PropertyInteger", "Teeth", LANG.chunk("PropertyTitle")[0], LANG.chunk("PropertyTeeth")[0])
        obj.addProperty("App::PropertyLength", "Toothheight", LANG.chunk("PropertyTitle")[0], LANG.chunk("PropertyToothheight")[0])
        obj.addProperty("App::PropertyFloat", "Curve", LANG.chunk("PropertyTitle")[0], LANG.chunk("PropertyCurve")[0])
        obj.addProperty("App::PropertyLength", "Pad", LANG.chunk("PropertyTitle")[0], LANG.chunk("PropertyPad")[0])
        obj.addProperty("App::PropertyPythonObject", "ratchet", LANG.chunk("PropertyTitle")[0], "ratchet object")

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
        for v in range(len(vector)):
            if v < nextv:
                continue
            if vector[v]['type'] == 'p':
                if v<(len(vector)-1):
                    draft.append(Part.LineSegment(  FreeCAD.Vector(vector[v-1]['x'], vector[v-1]['y'], vector[v-1]['z']),
                                                    FreeCAD.Vector(vector[v]['x'], vector[v]['y'], vector[v]['z'])).toShape())
                else:
                    draft.append(Part.LineSegment(  FreeCAD.Vector(vector[v]['x'], vector[v]['y'], vector[v]['z']),
                                                    FreeCAD.Vector(vector[0]['x'], vector[0]['y'], vector[0]['z'])).toShape())
                nextv = v+1
            elif vector[v]['type'] == 'r':
                draft.append(Part.Arc(  FreeCAD.Vector(vector[v-1]['x'], vector[v-1]['y'], vector[v-1]['z']),
                                        FreeCAD.Vector(vector[v]['x'], vector[v]['y'], vector[v]['z']),
                                        FreeCAD.Vector(vector[v+1]['x'], vector[v+1]['y'], vector[v+1]['z'])).toShape())
                nextv = v+2
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
    def __init__(self, obj):
        super(Double, self).__init__(obj)
        properties = {
            'Radius': 25,
            'Teeth': 15,
            'Toothheight': 5,
            'Pad': 5
        }
        self.ratchet = teeth.DoubleTeeth(properties)

        obj.addProperty("App::PropertyLength", "Radius", LANG.chunk("PropertyTitle")[0], LANG.chunk("PropertyRadius")[0])
        obj.addProperty("App::PropertyInteger", "Teeth", LANG.chunk("PropertyTitle")[0], LANG.chunk("PropertyTeeth")[0])
        obj.addProperty("App::PropertyLength", "Toothheight", LANG.chunk("PropertyTitle")[0], LANG.chunk("PropertyToothheight")[0])
        obj.addProperty("App::PropertyLength", "Pad", LANG.chunk("PropertyTitle")[0], LANG.chunk("PropertyPad")[0])
        obj.addProperty("App::PropertyPythonObject", "ratchet", "Parameter", "ratchet object")

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
        for v in range(len(vector)):
            if vector[v]['type'] == 'p':
                if v<(len(vector)-1):
                    draft.append(Part.LineSegment(  FreeCAD.Vector(vector[v]['x'], vector[v]['y'], vector[v]['z']),
                                                    FreeCAD.Vector(vector[v+1]['x'], vector[v+1]['y'], vector[v+1]['z'])).toShape())
                else:
                    draft.append(Part.LineSegment(  FreeCAD.Vector(vector[v]['x'], vector[v]['y'], vector[v]['z']),
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