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
    args = parser.parse_args()
    DEBUG = args.d
    OUTPUT_FILE = args.o
    CONFIG_FILE = args.input

    # Configparser
    if not os.path.isfile(CONFIG_FILE):
        print("ERROR: Could not find config file named: '%s'" % CONFIG_FILE)
        exit(1)
    Config = ConfigParser.ConfigParser()
    Config.read(CONFIG_FILE)
    trim_root = Config.getfloat('Panel',"TrimFromRootSide")
    trim_tip = Config.getfloat('Panel',"TrimFromTipSide")
    side = Config.get('Panel',"Side").lower

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


    if side == "left" or side == "l":
        r1, r2 = r2, r1

    # Create panel
    p = Panel(r1, r2, Config.getfloat('Panel',"Width"))

    # Trim Panel, if necessary
    if not trim_root == 0 or not trim_tip == 0:
        if side == "left":
            p = Panel.trim_panel(p, trim_root, Config.getfloat('Panel',"Width") - trim_tip )
        if side == "right":
            p = Panel.trim_panel(p, trim_tip, Config.getfloat('Panel',"Width") - trim_root )

    # Create Machine
    m = Machine(    width = Config.getfloat('Machine',"Width"), 
                    kerf =  Config.getfloat('Machine',"Kerf"),
                    profile_points = Config.getint('Machine',"ProfilePoints"),
                    output_profile_images=args.d
                )
    # Load Panel into Machine
    m.load_panel(p)

    if DEBUG:
        m.gcode_formatter_name = "debug"

    # Generate code
    gcode = m.generate_gcode(   le_offset = Config.getfloat('Machine',"StartOffsetLeadingEdge"), 
                                te_offset = Config.getfloat('Machine',"EndOffsetTrailingEdge"),
                                safe_height = Config.getfloat('Machine',"SafeHeight"),
                                normalize = True )

    if OUTPUT_FILE:
        with open(OUTPUT_FILE,"w")as f:
            f.writelines(gcode)
    else:
        print(gcode)

if __name__ == "__main__":
    main()
