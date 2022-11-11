"""
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


import uuid


class P2D:
    """
    Simple 2d point class
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.x:.3f} {self.y:.3f}"


def generate_via(loc: P2D, diameter: float, drill: float) -> str:
    """
    Generates a via to be placed in the footprint file
    Args:
        loc: location of via (mm)
        diameter: diameter of the copper of the via (mm)
        drill: size of the hole drilled through the via (mm)

    Returns:
        str: the via, formatted for use in the footprint file
    """
    via = f'  (pad "" thru_hole circle (at {loc}) (size {diameter} {diameter}) (drill {drill}) (layers *.Cu *.Mask) ({gen_tstamp()}))\n'
    return via


def generate_line(start: P2D, stop: P2D, width: float, layer: str) -> str:
    """
    Generates a line to be placed in the footprint file
    Args:
        start: start 2d point (mm)
        stop: stop 2d point (mm)
        width: width of line (mm)
        layer: line layer, one of "F.Cu" or "B.Cu"

    Returns:
        str: the line, formatted for use in the footprint file
    """
    line = f'  (fp_line (start {start}) (end {stop}) (layer "{layer}") (width {width:.3f}) ({gen_tstamp()}))\n'
    return line


def generate_arc(start: P2D, mid:P2D, stop: P2D, width: float, layer: str, swap_start_stop: bool) -> str:
    """
    Generates an arc to be placed in the footprint file
    Args:
        start: start 2d point (mm)
        mid: midpoint 2d point (mm)
        stop: stop 2d point (mm)
        width: width of arc (mm)
        layer: line layer, one of "F.Cu" or "B.Cu"
        swap_start_stop: swaps start and swap point, needed because KiCAD ignores the midpoint in determining arc side,
            and always wraps clockwise from start to stop

    Returns:
        str: the arc, formatted for use in the footprint file
    """
    if not swap_start_stop:
        arc = f'  (fp_arc (start {start}) (mid {mid})(end {stop}) (layer "{layer}") (width {width:.3f}) ' \
              f'({gen_tstamp()}))\n'
    else:
        arc = f'  (fp_arc (start {stop}) (mid {mid})(end {start}) (layer "{layer}") (width {width:.3f}) ' \
              f'({gen_tstamp()}))\n'
    return arc


def generate_pad(pid: int, loc: P2D, width: float, height: float, layer: str) -> str:
    """
    Generates a pad to be placed in the footprint file, note: no soldermask layer is added here like you might expect in
    a typical SMD pad (you could call this func with a different layer if you wanted to though)
    Args:
        pid: pad/pin number in KiCAD
        loc: location of the center of the pad
        width: width of the pad
        height: height of the pad
        layer: pad layer, one of "F.Cu" or "B.Cu"

    Returns:
        str: the arc, formatted for use in the footprint file
    """
    pad = f'  (pad "{pid}" smd roundrect (at {loc}) (size {width} {height}) (layers "{layer}")' \
          f' (roundrect_rratio 0.25) ({gen_tstamp()}))\n'
    return pad


def gen_tstamp() -> str:
    """
    Timestamps in KiCAD are really just UUIDs that pcbnew can link back to later (I think?).
    Source: https://docs.kicad.org/6.0/en/eeschema/eeschema.html#custom-netlist-and-bom-formats

    Returns:
        str: timestamp string
    """
    return f"tstamp {uuid.uuid4()}"


def draw_loop(radius: float, increment: float, width: float, layer: str, wrap_multiplier: int) -> list[str]:
    """
    Creates to arcs (in a loop), starting at radius, and finishing at radius + increment. Also adds increment to radius
    at the end

    Args:
        radius: starting radius (mm)
        increment: how far the arc should exceed the original radius after 1 loop (mm)
        width: trace width (mm)
        layer: "F.Cu" or "B.Cu"
        wrap_multiplier: 1 for CW, -1 for CCW


    Returns:
        list containing 2 arcs in string form (will need to be put in .kicad_mod file)
    """
    arcs = [
        generate_arc(
            P2D(radius, 0),
            P2D(0, -wrap_multiplier * radius),
            P2D(-radius, 0),
            width,
            layer,
            bool(wrap_multiplier + 1)
        ),
        generate_arc(
            P2D(-radius, 0),
            P2D(0, wrap_multiplier * (radius + increment / 2)),
            P2D(radius + increment, 0),
            width,
            layer,
            bool(wrap_multiplier + 1)
        )
    ]
    return arcs
