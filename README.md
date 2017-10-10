
# HotWing-cli

![Hotwing Bird Logo](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/hotwing_logo.png)

HotWing-cli is a is a Gcode generator for cutting model aircraft wings on a 4-axis CNC foam cutter. It is based on the [hotwing-core library](https://github.com/jasonhamilton/hotwing-core) and allows a user to design and modify their wings through a config file.

# Usage

## Getting Started
 
1) Make sure you have Python and Pip installed
2) Download the repository to your computer
3) Navigate to the repository folder ```cd /my/folder/hotwing-cli```
4) Install Dependencies ```pip install -r requirements.txt```
5) Install HotWing-CLI ```pip install .```
6) Copy the sample-config.cfg file and modify it to customize your wing - see the config customization options below.
7) Run HotWing!  ```hotwing-cli my-config.cfg```


## Command Line Args

    ```sh
    $ python hotwing.py -h # see additional options
    usage: hotwing-cli [-h] [-o output] [-d] input

    Gcode generator for cutting model aircraft wings on a 4-axis CNC foam cutter.

    positional arguments:
      input       Config file to process and create gcode from.

    optional arguments:
      -h, --help  show this help message and exit
      -o output   Output file to write to
      -d          Turn on debugging - draws images of profiles as they are
                  created.
    ```


# Config File Options

The program requires a config file to operate.  A config file contains the contains the variables that define the wing.  The config file is organized into multiple sections that you can edit to get the perfect wing.  Start by copying the sample config file and use it as a starting point for creating your wing.  A config file looks something like (do not use - it is not complete):

```cfg
[RootChord]
Profile = profiles/rg14.dat
Width = 10
LeadingEdgeOffset = 0
Rotation = 0
RotationPosition = 0.5

[TipChord]
...
```

## Config File Sections

### RootChord
Define the properties of your root chord here

* **Profile** - Filename of the profile to use for the chord.
* **Width** - Width of the chord, measured from the front to back of the wing at the chord position.
* **LeadingEdgeOffset** - How far should the chord be offset forward or backwards.  Positive value moves chord aft  - see below for detailed explanation.  
* **Rotation** - defines washout - positive value angles leading edge upwards
* **RotationPosition** - Position to rotate as a percentage of the chord to rotate.  ex: 0.5 = 50%; 0.25 = 25%

### TipChord
Define the properties of your tip chord here

* **Profile** - Filename of the profile to use for the chord.
* **Width** - Width of the chord, measured from the front to back of the wing at the chord position.
* **LeadingEdgeOffset** - How far should the chord be offset forward or backwards.  Positive value moves chord aft  - see below for detailed explanation.  
* **Rotation** - defines washout - positive value angles leading edge upwards
* **RotationPosition** - Position to rotate as a percentage of the chord to rotate.  ex: 0.5 = 50%; 0.25 = 25%


### Panel
 * **Side** - Which side to cut.  Left or Right.
 * **Width** - Width of the total wing panel.  This is usually going to be half of the total span unless you are creating multiple panels.
 * **SheetingTop** - Allowance for sheeting on the top of the profile - the profile will be reduced by this amount.
 * **SheetingBottom** - Allowance for sheeting on the bottom of the profile - the profile will be reduced by this amount.
 * **StockLeadingEdge** - Allowance for stock on the leading edge.  This is useful if you want to glue on a wooden block on the leading edge that you will eventually sand down to the airfoil shape.
 * **StockTrailingEdge** - Allowance for stock on the trailing edge.  This is useful if you want to glue on a wooden trailing edge stock that you will sand down to the airfoil shape.
 * **TrimFromRootSide** - You can shorten the panel to cut.  Say you design a half wing as a panel but want to cut it in two or more sections.  This is the amount the panel will be trimmed down from the Root side of the wing.
 * **TrimFromTipSide** - This is the amount the panel will be trimmed down from the Tip side of the wing.

### Machine

 * **Width** -  Width of the distance between the pillars of your foam cutter.  This should be measured to where the hotwire is anchored on each pillar
 * **SafeHeight** - Height where the machine can move without worring about hitting anything
 * **StartOffsetLeadingEdge** - Position in front of the leading edge the hotwire will start from and then travel to the leading edge.
 * **EndOffsetTrailingEdge** -  Position behind the trailing edge the hotwire will extend/cut to.
 * **Kerf** -  Amount of room to offset the hotwire so an accurate amount of foam is cut
 * **ProfilePoints** - The number of points that will be used to cut each of the top and bottom profiles
 * **Normalize** -  Normalization makes sure none of the gcode values are < 0


```
# OFFSET EXAMPLE
# 
# For example if you have a chord of length 10
# and another with length 5 and you don't include an offset the leading 
# edge will be straight and the trailing edge will be angled.
#
# Example 1 - Straight Leading Edge
# Root:                             Tip: 
#   Width  = 10                       Width  = 6
#   Offset = 0                        Offset = 0
#        ............................................
#        |                                          |   6           
#        |                                          |
#    10  |                            .....---- ````
#        |              .....---- ````
#        |.....---- ````
#
#
#
# Example 2 - Straight Trailing Edge
# Root:                             Tip: 
#   Width  = 10                       Width  = 6
#   Offset = 0                        Offset = 4
#        .....
#        |    ````---- ....                                 ```|           
#        |                  ```` ----.....                     | ---  Offset 4  
#    10  |                                 ```` ....        ...|
#        |                                          |   6
#        |..........................................|
#
#
#
# Example 3 - Same angle front and back
# Root:                             Tip: 
#   Width  = 10                       Width  = 6
#   Offset = 0                        Offset = 2
#         ........                                         ```|
#        |         ``````` -------- ..........                | ---- Offset 2              
#        |                                     `````|      ````
#    10  |                                          |  6
#        |                          .......... -----`
#        |........ ------- ````````
```