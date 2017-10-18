#!/usr/bin/env python
from __future__ import division
from hotwing_core.profile import Profile
from hotwing_core.rib import Rib
from hotwing_core.machine import Machine
from hotwing_core.panel import Panel
from hotwing_core.coordinate import Coordinate
from .generate_config import generate_config
import argparse
import os
try:
    import ConfigParser
except ModuleNotFoundError:
    import configparser as ConfigParser


CONFIG_OPTIONS = {
    'Project':{
                    "Units":{"type":str,"required":False,"default":"inches"},

    },
    'RootChord':{   "Profile":{"type":str,"required":True},
                    "Width":{"type":float,"required":True},
                    "LeadingEdgeOffset":{"type":float,"required":False,"default":0},
                    "Rotation":{"type":float,"required":False,"default":0},
                    "RotationPosition":{"type":float,"required":False,"default":0}
                },
    'TipChord':{    "Profile":{"type":str,"required":True},
                    "Width":{"type":float,"required":True},
                    "LeadingEdgeOffset":{"type":float,"required":False,"default":0},
                    "Rotation":{"type":float,"required":False,"default":0},
                    "RotationPosition":{"type":float,"required":False,"default":0}
    },
    'Panel':{
                    "Width":{"type":float,"required":True},
                    "StockLeadingEdge":{"type":float,"required":False,"default":0},
                    "StockTrailingEdge":{"type":float,"required":False,"default":0},
                    "SheetingTop":{"type":float,"required":False,"default":0},
                    "SheetingBottom":{"type":float,"required":False,"default":0}

    },
    'Machine':{
                    "Width":{"type":float,"required":True},
                    "FoamHeight":{"type":float,"required":True},
                    "Feedrate":{"type":float,"required":True},
                    "Kerf":{"type":float,"required":True},
    }
}



def main():
    # argparse
    parser = argparse.ArgumentParser(description='Gcode generator for cutting model aircraft wings on a 4-axis CNC foam cutter.')
    parser.add_argument('command', metavar='command', type=str, help='Command.  Available: parse, init. Parse takes an input config file and '
                                                                    'converts it to gcode.  Init creates a new config file.', nargs="+")
    parser.add_argument('-i', metavar='input', type=str, help='Config file to process and create gcode from.')
    parser.add_argument('-o', metavar='output', type=str, help='Output file to write to.  If not specified, the output will be written to stdout.')
    parser.add_argument('-d', action='store_true', help='Turn on debugging.  The output will be tab separated values instead of gcode.')
    parser.add_argument('-s', metavar='side', default='r', type=str, help='Side to cut - \'l\' or \'r\'. (default=\'r\')')
    parser.add_argument('-t', metavar='trim', type=str, help='Trims the wing panel before cutting.  Specifies the section of wing to cut, '
                                                             'starting at the root to the tip. For example \'10-20\' will cut a section '
                                                             'starting at 10 units from the root and ending 20 units from the root (total '
                                                             'width of 10 units).'
                                                             )
    parser.add_argument('-p', metavar='points', default=200, type=int, 
                        help='The number of points to interpolate/cut each profile surface (top/bottom).  (default=200)')
    parser.add_argument('-l', metavar='left_offset', type=float, 
                        help='Distance to place the panel from the left machine pillar.  If not specified, the panel will '
                             'be centered between the machine pillars')
    

    args = parser.parse_args()
    DEBUG = args.d
    OUTPUT_FILE = args.o
    CONFIG_FILE = args.i
    COMMAND = str(args.command[0])

    if COMMAND == "init":
        if len(args.command) == 2:
            generate_config(args.command[1])
            print("config file generated - %s" % args.command[1])
            exit(0)
        else:
            print("Error generating config file. One command expected")
            exit(1)
    elif COMMAND == "parse":
        if not CONFIG_FILE:
            if len(args.command) == 2:
                CONFIG_FILE = args.command[1]
                # try using the positional parameter
            else:
                # no additional positional parameter
                print("Error: no config file received.  Try using 'hotwing-cli parse myconfig.cfg' or use the -i parameter "
                      "to specify your config file.")
                exit(1)
    else:
        print("Error: Unknown command %s" % COMMAND)
        exit(1)


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


    def get_config(section, parameter):
        opt = CONFIG_OPTIONS[section][parameter]
        if opt['type'] == float:
            try:
                return Config.getfloat(section,parameter) 
            except ConfigParser.NoOptionError:
                if opt['required']:
                    raise
                else:
                    if DEBUG:
                        print("using default for %s - %s"%(section,parameter) )
                    return opt["default"]
        elif opt['type'] == str:
            try:
                return Config.get(section,parameter) 
            except ConfigParser.NoOptionError:
                if opt['required']:
                    raise
                else:
                    if DEBUG:
                        print("using default for %s - %s"%(section,parameter) )
                    return opt["default"]



    try:
        r1 = Rib(   get_config('RootChord',"Profile"), 
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
        print("Error: Could not find the Root Chord file:", get_config('RootChord',"Profile"))
        exit(1)
        
    try:
        r2 = Rib(   get_config('TipChord',"Profile"), 
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
        print("Error: Could not find the Tip Chord file:", get_config('TipChord',"Profile"))
        exit(1)


    if SIDE == "left":
        r1, r2 = r2, r1

    # Create panel
    p = Panel(r1, r2, get_config('Panel',"Width"))

    # Trim Panel, if necessary
    if TRIM:
        if SIDE == "left":
            p = Panel.trim_panel(p, get_config('Panel',"Width") - TRIM_B, get_config('Panel',"Width") - TRIM_A )
        if SIDE == "right":
            p = Panel.trim_panel(p, TRIM_A, TRIM_B )

    if p.width > get_config('Machine',"Width"):
        print("Error: Panel (%s) is bigger than the machine width (%s)." % (get_config('Machine',"Width"), p.width) )
        exit(1)

    # Create Machine
    m = Machine(    width = get_config('Machine',"Width"), 
                    kerf =  get_config('Machine',"Kerf"),
                    profile_points = args.p,
                    units = get_config('Project',"Units"),
                    feedrate = get_config('Machine',"Feedrate")
                )
    
    # Set offset
    if args.l:
        offset = args.l
    else:
        # center panel by default
        offset = (get_config('Machine',"Width") - p.width)/2

    # Load Panel into Machine
    m.load_panel(left_offset=offset, panel=p)

    if DEBUG:
        m.gcode_formatter_name = "debug"


    # Generate code
    gcode = m.generate_gcode(   safe_height = get_config('Machine',"FoamHeight")*1.25,
                                normalize = True )

    if OUTPUT_FILE:
        with open(OUTPUT_FILE,"w")as f:
            f.writelines(gcode)
    else:
        print(gcode)

if __name__ == "__main__":
    main()
