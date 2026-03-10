# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Ratchet addon.

from FreeCAD import DocumentObject , Units


class SymmetricObject ( DocumentObject ):

    Depth : Units.Quantity
    Count : int

    Radius : Units.Quantity
    Height : Units.Quantity