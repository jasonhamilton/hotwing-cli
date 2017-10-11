from hotwing_core.profile import Profile
from hotwing_core.rib import Rib
from hotwing_core.machine import Machine
from hotwing_core.panel import Panel
from hotwing_core.coordinate import Coordinate
import argparse
import os
try:
    import ConfigParser
except ModuleNotFoundError:
    import configparser as ConfigParser


def main():
    # argparse
    parser = argparse.ArgumentParser(description='Gcode generator for cutting model aircraft wings on a 4-axis CNC foam cutter.')
    parser.add_argument('input', metavar='input', type=str, help='Config file to process and create gcode from.')
    parser.add_argument('-o', metavar='output', type=str, help='Output file to write to')
    parser.add_argument('-d', action='store_true', help='Turn on debugging - draws images of profiles as they are created.')
    parser.add_argument('-s', metavar='side', default='r', type=str, help='Side to cut - \'l\' or \'r\'')
    parser.add_argument('-t', metavar='trim', type=str, help='Section of wing to cut starting at the root to the tip. '
                                                             'e.g: 10-20 will use the panel but only cut a 10 unit section '\
                                                             'starting at 10 units from the root and ending 20 units from the root.')
    parser.add_argument('-p', metavar='points', default=200, type=int, 
                        help='The number of points to interpolate/cut each profile surface (top/bottom).')


    args = parser.parse_args()
    DEBUG = args.d
    OUTPUT_FILE = args.o
    CONFIG_FILE = args.input

    # PARSE SIDE PARAMETER
    if args.s.lower() not in ['l','r','left','right']:
        print("Invalid input for side (-s) parameter '%s'" % args.s)
        exit(1)
    else:
        if args.s.lower() in ['l','left']:
            SIDE = 'left'
        else:
            SIDE = 'right'

    # PARSE TRIM PARAMETER
    if args.t:
        try:
            a,b = args.t.split("-")
            TRIM_A = float(a)
            TRIM_B = float(b)
            TRIM = True
        except:
            print("Invalid input for trim (-t) parameter '%s'" % args.t)
            exit(1)
    else:
        TRIM=False

    # Configparser
    if not os.path.isfile(CONFIG_FILE):
        print("ERROR: Could not find config file named: '%s'" % CONFIG_FILE)
        exit(1)
    Config = ConfigParser.ConfigParser()
    Config.read(CONFIG_FILE)

    try:
        r1 = Rib(   Config.get('RootChord',"Profile"), 
                    scale=Config.getfloat('RootChord',"Width"), 
                    xy_offset=Coordinate(Config.getfloat('RootChord',"LeadingEdgeOffset"),0), 
                    top_sheet=Config.getfloat('Panel',"SheetingTop"), 
                    bottom_sheet=Config.getfloat('Panel',"SheetingBottom"), 
                    front_stock=Config.getfloat('Panel',"StockLeadingEdge"), 
                    tail_stock=Config.getfloat('Panel',"StockTrailingEdge"),
                    rotate=Config.getfloat('RootChord',"Rotation"),
                    rotate_pos=Config.getfloat('RootChord',"RotationPosition"),
                    )
    except IOError:
        print("Error: Could not find the Root Chord file:", Config.get('RootChord',"Profile"))
        exit(1)
        
    try:
        r2 = Rib(   Config.get('TipChord',"Profile"), 
                    scale=Config.getfloat('TipChord',"Width"), 
                    xy_offset=Coordinate(Config.getfloat('TipChord',"LeadingEdgeOffset"),0), 
                    top_sheet=Config.getfloat('Panel',"SheetingTop"), 
                    bottom_sheet=Config.getfloat('Panel',"SheetingBottom"), 
                    front_stock=Config.getfloat('Panel',"StockLeadingEdge"), 
                    tail_stock=Config.getfloat('Panel',"StockTrailingEdge"),
                    rotate=Config.getfloat('TipChord',"Rotation"),
                    rotate_pos=Config.getfloat('TipChord',"RotationPosition"),
                    )
    except IOError:
        print("Error: Could not find the Tip Chord file:", Config.get('TipChord',"Profile"))
        exit(1)


    if SIDE == "left":
        r1, r2 = r2, r1

    # Create panel
    p = Panel(r1, r2, Config.getfloat('Panel',"Width"))

    # Trim Panel, if necessary
    if TRIM:
        if SIDE == "left":
            p = Panel.trim_panel(p, Config.getfloat('Panel',"Width") - TRIM_B, Config.getfloat('Panel',"Width") - TRIM_A )
        if SIDE == "right":
            p = Panel.trim_panel(p, TRIM_A, TRIM_B )

    if p.width > Config.getfloat('Machine',"Width"):
        print("Error: Panel (%s) is bigger than the machine width (%s)." % (Config.getfloat('Machine',"Width"), p.width) )
        exit(1)

    # Create Machine
    m = Machine(    width = Config.getfloat('Machine',"Width"), 
                    kerf =  Config.getfloat('Machine',"Kerf"),
                    profile_points = args.p,
                    output_profile_images=args.d
                )
    # Load Panel into Machine
    m.load_panel(p)

    if DEBUG:
        m.gcode_formatter_name = "debug"

    
    foam_width = Config.getfloat('Machine',"FoamDepth")
    max_chord_length = max(r1.scale, r2.scale)
    le_offset = te_offset = (foam_width - max_chord_length)/2 + Config.getfloat('Machine',"FoamDepth")* 0.05

    # Generate code
    gcode = m.generate_gcode(   le_offset = le_offset, 
                                te_offset = te_offset,
                                safe_height = Config.getfloat('Machine',"FoamHeight")*1.25,
                                normalize = True )

    if OUTPUT_FILE:
        with open(OUTPUT_FILE,"w")as f:
            f.writelines(gcode)
    else:
        print(gcode)

if __name__ == "__main__":
    main()
