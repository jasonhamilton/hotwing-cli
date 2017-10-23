#!/usr/bin/env python
from __future__ import division
from hotwing_core.profile import Profile
from hotwing_core.rib import Rib
from hotwing_core.machine import Machine
from hotwing_core.panel import Panel
from hotwing_core.coordinate import Coordinate
from .generate_config import generate_config
from .config_options import CONFIG_OPTIONS, get_config, read_config
from .validators import validate_side, vaidate_config_file, validate_trim, validate_kerf
import click
import os


@click.group()
def cli():
    pass

@click.command()
@click.argument('file')
def init(file):
    generate_config(file)
    click.echo("config file generated - %s" % file)
    exit(0)

@click.command()
@click.argument('file', callback=vaidate_config_file)
@click.option('-o', type=str, help='Output file to write to.  If not specified, the output will be written to stdout.')
@click.option('-d', type=str, help='DEBUGGING.  The output will be tab separated values instead of gcode.', is_flag=True)
@click.option('-s', type=str, default='r', callback=validate_side, help='SIDE to cut - \'l\' or \'r\' for left or right wing, respectively. (default=\'r\')')
@click.option('-t', type=str, callback=validate_trim, help='TRIM the wing panel before cutting.  Specifies the section of wing to cut, '
                                                         'starting at the root to the tip. For example \'10-20\' will cut a section '
                                                         'starting at 10 units from the root and ending 20 units from the root (total '
                                                         'width of 10 units).'
                                                         )
@click.option('-p', type=int, default=200, 
                    help='POINTS.  The number of points to interpolate/cut each profile surface (top/bottom).  (default=200)')
@click.option('-l', type=float, metavar='LEFT OFFSET', 
                    help='LEFT OFFSET.  Distance to place the panel from the left machine pillar.  If not specified, the panel will '
                         'be centered between the machine pillars')
def parse(file,o,d,s,t,p,l):

    read_config(file)
    
    try:
        rib1 = Rib( get_config('RootChord',"Profile"), 
                    scale=get_config('RootChord',"Width"), 
                    xy_offset=Coordinate(get_config('RootChord',"LeadingEdgeOffset"),0), 
                    top_sheet=get_config('Panel',"SheetingTop"), 
                    bottom_sheet=get_config('Panel',"SheetingBottom"), 
                    front_stock=get_config('Panel',"StockLeadingEdge"), 
                    tail_stock=get_config('Panel',"StockTrailingEdge"),
                    rotation=get_config('RootChord',"Rotation"),
                    rotation_pos=get_config('RootChord',"RotationPosition"),
                    )
    except IOError:
        click.echo("Error: Could not find the Root Chord file:", get_config('RootChord',"Profile"))
        exit(1)
        
    try:
        rib2 = Rib( get_config('TipChord',"Profile"), 
                    scale=get_config('TipChord',"Width"), 
                    xy_offset=Coordinate(get_config('TipChord',"LeadingEdgeOffset"),0), 
                    top_sheet=get_config('Panel',"SheetingTop"), 
                    bottom_sheet=get_config('Panel',"SheetingBottom"), 
                    front_stock=get_config('Panel',"StockLeadingEdge"), 
                    tail_stock=get_config('Panel',"StockTrailingEdge"),
                    rotation=get_config('TipChord',"Rotation"),
                    rotation_pos=get_config('TipChord',"RotationPosition"),
                    )
    except IOError:
        click.echo("Error: Could not find the Tip Chord file:", get_config('TipChord',"Profile"))
        exit(1)

    # crate panel
    panel = Panel(rib1, rib2, get_config('Panel',"Width"))

    # trim if necessary
    if t:
        panel = Panel.trim(panel, t[0], t[1])

    # flip sides if necessary
    if s == "r":
        panel = Panel.reverse(panel)

    # make sure panel fits in machine, or quit
    if panel.width > get_config('Machine',"Width"):
        click.echo("Error: Panel (%s) is bigger than the machine width (%s)." % (get_config('Machine',"Width"), p.width) )
        exit(1)

    # Create Machine
    machine = Machine(  width = get_config('Machine',"Width"), 
                        kerf =  validate_kerf(get_config('Machine',"Kerf")),
                        profile_points = p,
                        units = get_config('Project',"Units"),
                        feedrate = get_config('Machine',"Feedrate")
                    )

    # Load Panel into Machine
    machine.load_panel(left_offset=l, panel=panel)

    if d:
        machine.gcode_formatter_name = "debug"

    # Generate code
    safe_height = get_config('Machine',"SafeHeight")
    safe_height = safe_height if safe_height else get_config('Machine',"FoamHeight")*2
    gcode = machine.generate_gcode( safe_height = safe_height,
                                    foam_height = get_config('Machine',"FoamHeight"),
                                    normalize = True )

    if o:
        with open(o,"w")as f:
            f.writelines(gcode)
    else:
        click.echo(gcode)


cli.add_command(init)
cli.add_command(parse)

def main():
    cli()


