## Ratchet Workbench 

A FreeCAD workbench to create ratchets

### Background
Considering manually constructing circular ratchets an annoying task you can now choose between the automated creation of ratchets that allow only for one direction or ratches that allow both directions. For inset mechanisms you can just subtract the generated shape.

Heavily <s>stolen</s> inspired from [looooos freecad.gears](https://github.com/looooo/freecad.gears).

![screenshot](https://raw.githubusercontent.com/erroronline1/ratchetWB/master/resources/media/screenshot.png)

### Version compatibility

<details>
<summary>Confirmed latest stable FreeCad version 1.0 - Expand for more</summary>

* 1.1rc build 40041 x86_64
* 1.0
* 0.21.2
* 0.20

</details>

### Usage

Add one of the desired geometries either as a part or as part of an active body. Change values regarding e.g. size and number of teeth within the models property settings. Possibly edit the Curve-property for inset directed ratchets.

There is not a complete failsafe mechanism to avoid all possible meaningless values! 

### Installation 

#### Manual Installation

<details>
<summary>Expand for directions to manually install this workbench</summary>

This workbench can be installed manually by adding the whole folder into the personal FreeCAD folder

- for Linux `/home/user/.local/share/FreeCAD/Mod/` or `~/.var/app/org.freecad.FreeCAD/data/FreeCAD/Mod`
- for Windows `%APPDATA%\FreeCAD\Mod\` or `C:\Users\username\Appdata\Roaming\FreeCAD\Mod\`
- for Windows as portable app `wherever_stored\FreeCADPortable\Data\FreeCADAppData\Mod`
- for macOS `~/Library/Preferences/FreeCAD/Mod/`

Occasionally rename from Ratchet-master to Ratchet if downloaded as zip from github

</details>

### Bug/Feedback

Please report bugs to the [issue queue](https://github.com/erroronline1/ratchetWB/issues) and ping the [dedicated Ratchet FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=22&t=71072) to discuss said issue or feedback in general.   

## License

Ratchet is released under the LGPL3+ license. See [LICENSE](LICENSE).
