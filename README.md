<!-- SPDX-License-Identifier: LGPL-3.0-or-later -->
<!-- SPDX-FileNotice: Part of the Ratchet addon. -->

<div align = 'center' >

# Ratchet 

FreeCAD addon for ratchet creation.

[ [Forum Discussion][Forum] ]

![Preview]

</div>

<br/>

## Usage

The functions are available through the Part-workbench.

Add one of the desired geometries either as a part or as part of an active body. Change values regarding e.g. size and number of teeth within the models property settings. Possibly edit the Curve-property for inset directed ratchets.

There is not a complete failsafe mechanism to avoid all possible meaningless values!  
Subtractive directed ratchets in PartDesign may not render correct. I can only assume it has something to do with the curvatures. You can however select the contained shape and create a pocket with it.

<br/>

## Background

Considering manually constructing circular ratchets an annoying task you can now choose between the automated creation of ratchets that allow only for one direction or ratches that allow both directions. For inset mechanisms you can just subtract the generated shape.

*Originally inspired by looooos [Gears] addon.*

<br/>


[Preview]: ./Resources/Media/Preview.png
[Forum]: https://forum.freecadweb.org/viewtopic.php?f=22&t=71072
[Gears]: https://github.com/looooo/freecad.gears