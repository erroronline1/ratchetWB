# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from ..Misc import Paths, asIcon

from FreeCAD import Gui, activeDocument, Qt

translate = Qt.translate

class TaskPanel:
    def __init__(self, object):

        self.object = object

        self.initial = {
            "Radius": self.object.Radius.Value,
            "Height": self.object.Height.Value,
            "Count": self.object.Count,
            "Depth": self.object.Depth.Value,
            "Curve": self.object.Curve if hasattr(self.object, 'Curve') else None
        }

        self.form = Gui.PySideUic.loadUi(f"{Paths['Panels']}/Panel.ui")

        # translations
        self.form.setWindowTitle(translate('TaskPanel','Ratchet Settings'))
        self.form.RadiusLabel.setProperty("text", translate('App::Property','Radius'))
        self.form.HeightLabel.setProperty("text", translate('App::Property','Height'))
        self.form.CountLabel.setProperty("text", translate('App::Property','Count'))
        self.form.DepthLabel.setProperty("text", translate('App::Property','Depth'))
        self.form.CurveLabel.setProperty("text", translate('App::Property','Curve'))
        self.form.Preview.setProperty("text", translate('App::Property','Preview'))

        # value filling
        self.form.Radius.setProperty("rawValue", self.object.Radius.Value)
        self.form.Height.setProperty("rawValue", self.object.Height.Value)
        self.form.Count.setProperty("rawValue", self.object.Count)
        self.form.Depth.setProperty("rawValue", self.object.Depth.Value)
        if hasattr(self.object, 'Curve'):
            self.form.Curve.setProperty("rawValue", self.object.Curve)
        else:
            self.form.Curve.setEnabled(False)

        # bindings to update and recompute if not deselected
        self.form.Radius.valueChanged.connect(self.set)
        self.form.Height.valueChanged.connect(self.set)
        self.form.Count.valueChanged.connect(self.set)
        self.form.Depth.valueChanged.connect(self.set)
        self.form.Curve.valueChanged.connect(self.set)
        self.form.Preview.clicked.connect(self.set)

    def accept(self):
        self.set()

        self.object.touch()
        activeDocument().recompute()
        Gui.Control.closeDialog()

    def reject(self):
        # reset to initial values
        self.object.Radius.Value = self.initial.get("Radius")
        self.object.Height.Value = self.initial.get("Height")
        self.object.Count = self.initial.get("Count")
        self.object.Depth.Value = self.initial.get("Depth")
        if hasattr(self.object, 'Curve'):
            self.object.Curve = self.initial.get("Curve")

        self.object.touch()
        activeDocument().recompute()
        Gui.Control.closeDialog()

    def set(self):
        self.object.Radius.Value = float(self.form.Radius.property("value"))
        self.object.Height.Value = float(self.form.Height.property("value"))
        self.object.Count = int(self.form.Count.property("value"))
        self.object.Depth.Value = float(self.form.Depth.property("value"))
        if hasattr(self.object, 'Curve'):
            self.object.Curve = float(self.form.Curve.property("value"))

        if self.form.Preview.property("checked"):
            self.object.touch()
            activeDocument().recompute()
