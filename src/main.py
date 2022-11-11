"""
This script is used to generate pcb coils
Copyright (C) 2022 Colton Baldridge

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from coilgen import *

"""  ~~~  ENTER PARAMETERS BELOW  ~~~  """
NAME = "COIL_GENERATOR_1"  # Name of footprint
DUAL_LAYER = True  # Determines if bottom layer should be used or not
WRAP_CLOCKWISE = True  # Wraps CCW if false
N_TURNS = 10  # Must be an int
TRACE_WIDTH = 0.15  # (mm)
TRACE_SPACING = 0.15  # (mm)
VIA_DIAMETER = 0.7  # (mm)
VIA_DRILL = 0.3  # (mm)
VIA_OFFSET = 2.8  # (mm)
BREAKOUT_LEN = 0.5  # (mm) scalar used to affect location of the breakouts
TEMPLATE_FILE = "template.kicad_mod"
TOP_LAYER = "F.Cu"
BOTTOM_LAYER = "B.Cu"

if __name__ == '__main__':
    with open(TEMPLATE_FILE, 'r') as file:
        template = file.read()

    arcs = []
    vias = []
    lines = []
    pads = []

    # place center via where it belongs
    vias.append(
        generate_via(
            P2D(VIA_DIAMETER/2 + VIA_OFFSET, 0),
            VIA_DIAMETER,
            VIA_DRILL)
    )

    # build out arcs to spec, until # turns is reached
    wrap_multiplier = 1 if WRAP_CLOCKWISE else -1
    radius = VIA_OFFSET + VIA_DIAMETER - TRACE_WIDTH/2
    increment = TRACE_WIDTH + TRACE_SPACING

    for arc in range(N_TURNS):
        loop = draw_loop(radius, increment, TRACE_WIDTH, TOP_LAYER, wrap_multiplier)
        arcs.extend(loop)
        if DUAL_LAYER:
            loop = draw_loop(radius, increment, TRACE_WIDTH, BOTTOM_LAYER, -wrap_multiplier)
            arcs.extend(loop)
        radius += increment

    # draw breakout line(s)
    lines.append(
        generate_line(
            P2D(radius, 0),
            P2D(radius + BREAKOUT_LEN, BREAKOUT_LEN * -wrap_multiplier),
            TRACE_WIDTH,
            TOP_LAYER
        )
    )
    lines.append(
        generate_line(
            P2D(radius + BREAKOUT_LEN, BREAKOUT_LEN * -wrap_multiplier),
            P2D(radius + 3 * BREAKOUT_LEN, BREAKOUT_LEN * -wrap_multiplier),
            TRACE_WIDTH,
            TOP_LAYER
        )
    )

    if DUAL_LAYER:
        lines.append(
            generate_line(
                P2D(radius, 0),
                P2D(radius + BREAKOUT_LEN, BREAKOUT_LEN * wrap_multiplier),
                TRACE_WIDTH,
                BOTTOM_LAYER
            )
        )
        lines.append(
            generate_line(
                P2D(radius + BREAKOUT_LEN, BREAKOUT_LEN * wrap_multiplier),
                P2D(radius + 2 * BREAKOUT_LEN, BREAKOUT_LEN * wrap_multiplier),
                TRACE_WIDTH,
                BOTTOM_LAYER
            )
        )
        # draw outer via
        vias.append(
            generate_via(
                P2D(radius + 2 * BREAKOUT_LEN, BREAKOUT_LEN * wrap_multiplier),
                VIA_DIAMETER,
                VIA_DRILL
            )
        )

        # draw last line to pad
        lines.append(
            generate_line(
                P2D(radius + 2 * BREAKOUT_LEN, BREAKOUT_LEN * wrap_multiplier),
                P2D(radius + 3 * BREAKOUT_LEN, BREAKOUT_LEN * wrap_multiplier),
                TRACE_WIDTH,
                TOP_LAYER
            )
        )

    # connect to pads

    # NOTE: there are some oddities in KiCAD here. The pad must be sufficiently far away from the last line such that
    # KiCAD does not display the "Cannot start routing from a graphic" error. It also must be far enough away that the
    # trace does not throw the "The routing start point violates DRC error". I have found that a 0.5mm gap works ok in
    # most scenarios, with a 1.2mm wide pad. Feel free to adjust to your needs, but you've been warned.
    pads.append(
        generate_pad(
            1,
            P2D(radius + 3 * BREAKOUT_LEN + 0.5, BREAKOUT_LEN * -wrap_multiplier),
            1.2,
            TRACE_WIDTH,
            TOP_LAYER
        )
    )

    if DUAL_LAYER:
        pads.append(
            generate_pad(
                2,
                P2D(radius + 3 * BREAKOUT_LEN + 0.5, BREAKOUT_LEN * wrap_multiplier),
                1.2,
                TRACE_WIDTH,
                TOP_LAYER
            )
        )

    substitution_dict = {
        "NAME": NAME,
        "LINES": ''.join(lines),
        "ARCS": ''.join(arcs),
        "VIAS": ''.join(vias),
        "PADS": ''.join(pads),
        "TIMESTAMP1": gen_tstamp(),
        "TIMESTAMP2": gen_tstamp(),
        "TIMESTAMP3": gen_tstamp(),
    }

    template = template.format(**substitution_dict)

    with open(f'{NAME}.kicad_mod', 'w') as outfile:
        outfile.write(template)
        outfile.close()

