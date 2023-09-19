# kicad-coil-creator
Creates coil footprints in KiCAD, what more could you want?

### How to use
Open main.py, put in the desired specs of your coil (described below), then let run `python3 main.py`. It's that simple!

### Coil Parameters
|Parameter|Type|Description|
|---|---|---|
|NAME|String| Name of the KiCAD footprint being created |
|DUAL_LAYER|Bool| Whether the coil should be 2 layers of not |
|WRAP_CLOCKWISE|Bool| Coil wraps clockwise if true, counter-clockwise if false |
|N_TURNS|Int| Turns the coil should make |
|TRACE_WIDTH|Float| Width of the trace making the coil |
|TRACE_SPACING|Float| Distance between the traces of the coil |
|VIA_DIAMETER|Float| Diameter of the via at the center and, if dual layer, at the outside of the coil |
|VIA_DRILL|Float| Drill hole size of the via at the center and, if dual layer, at the outside of the coil |
|VIA_OFFSET|Float| Distance from the center of the coil to the left innermost edge of the central via |
|BREAKOUT_LEN|Float| Scalar used to affect location of the breakout traces |
|TEMPLATE_FILE|String| Template file that the script fills in, default "template.kicad_mod" is included |
|TOP_LAYER|String| Layer to place the top of the coil onto |
|BOTTOM_LAYER|String| = Layer to place the bottom of the coil onto |

### Useful Links
 - [TI's app note on coil design for sensing](https://www.ti.com/lit/an/snoa930c/snoa930c.pdf)
 - [TI's coil design calculator](https://webench.ti.com/wb5/LDC/)
