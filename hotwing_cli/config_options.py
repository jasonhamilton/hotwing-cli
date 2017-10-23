try:
    import ConfigParser
except ModuleNotFoundError:
    import configparser as ConfigParser

## Setup Config Parser
Config = ConfigParser.ConfigParser()

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
                    "SafeHeight":{"type":float,"required":False, "default":0},
                    "Feedrate":{"type":float,"required":True},
                    "Kerf":{"type":str,"required":True},
    }
}


def get_config(section, parameter):
    opt = CONFIG_OPTIONS[section][parameter]
    try:
        if opt['type'] == float:
            return Config.getfloat(section,parameter)
        elif opt['type'] == str:
            return Config.get(section,parameter) 
        else:
            print("ERROR PARSING CONFIG OPTION")
    except ConfigParser.NoOptionError:
        if opt['required']:
            raise
        else:
            return opt["default"]

def read_config(filename):
    Config.read(filename)