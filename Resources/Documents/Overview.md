<!-- SPDX-License-Identifier: LGPL-3.0-or-later -->
<!-- SPDX-FileNotice: Part of the Ratchet addon. -->

# Ratchet Workbench 

A FreeCAD workbench to create ratchets

Considering manually constructing circular ratchets an annoying task you can now choose between the automated creation of ratchets that allow only for one direction or ratches that allow both directions. For inset mechanisms you can just subtract the generated shape.

![screenshot](https://raw.githubusercontent.com/erroronline1/ratchetWB/master/Resources/Media/Preview.png)

### Usage

The functions are available through the Part- and PartDesign-workbench.

Add one of the desired geometries either as a part or as part of an active body. Change values regarding e.g. size and number of teeth within the models property settings or the task panel by double clicking on the geometry within the tree. Possibly edit the Curve-property for inset directed ratchets.

There is not a complete failsafe mechanism to avoid all possible meaningless values!  
Subtractive directed ratchets in PartDesign may not render correct, if faces intersect. I can only assume it has something to do with the curvatures. You can however
* either select the contained shape and create a pocket with it
* or make it slightly bigger than the parent geometry and cut through all of it

### Bug/Feedback

Please report bugs to the [issue queue](https://github.com/erroronline1/ratchetWB/issues) and ping the [dedicated Ratchet FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=22&t=71072) to discuss said issue or feedback in general.