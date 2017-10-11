
# HotWing-cli

![Hotwing Bird Logo](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/hotwing_logo.png)

HotWing-cli is a is a Gcode generator for cutting model aircraft wings on a 4-axis CNC foam cutter. It is based on the [hotwing-core library](https://github.com/jasonhamilton/hotwing-core) and allows a user to design and modify their wings through a config file.

# Usage

## Installation
 
1) Make sure you have Python and Pip installed
2) Download the repository to your computer
3) Navigate to the repository folder ```cd /my/folder/hotwing-cli```
4) Install Dependencies ```pip install -r requirements.txt```
5) Install HotWing-CLI ```pip install .```


## Quick Start

1) Install HotWing-cli
2) Create a copy the [sample config file](https://github.com/jasonhamilton/hotwing-cli/blob/master/sample-config.cfg).
3) Modify the config file.  See the Config File Options section for help.
4) Run HotWing!  ```hotwing-cli path-to-my-config.cfg```.  
5) The previous command output the gcode to the screen but we want it in a file.  You can do so by redirecting the output to a file ```hotwing-cli path-to-my-config.cfg > saved-gcode.ngc``` or specifying the output file as a parameter ```hotwing-cli -o saved-gcode.ngc path-to-my-config.cfg```

For a more detailed walk through see this [tutorial](https://github.com/jasonhamilton/hotwing-cli/blob/master/tutorial.md)

## Command Line Args

```sh
$ python hotwing.py -h # see additional options
usage: hotwing-cli [-h] [-o output] [-d] [-s side] [-t trim] [-p points] input

Gcode generator for cutting model aircraft wings on a 4-axis CNC foam cutter.

positional arguments:
  input       Config file to process and create gcode from.

optional arguments:
  -h, --help  show this help message and exit
  -o output   Output file to write to
  -d          Turn on debugging - draws images of profiles as they are
              created.
  -s side     Side to cut - 'l' or 'r'
  -t trim     Section of wing to cut starting at the root to the tip. e.g:
              10-20 will use the panel but only cut a 10 unit section starting
              at 10 units from the root and ending 20 units from the root.
  -p points   The number of points to interpolate/cut each profile surface
              (top/bottom).

```


# Config File Options

A config file contains the contains the variables that define your wing.  The config file is organized into multiple sections that you can edit to get the perfect wing.  Start by copying the [sample config file](https://github.com/jasonhamilton/hotwing-cli/blob/master/sample-config.cfg) and use it as a starting point for creating your wing.  A sample config file looks like:

```cfg
[RootChord]
Profile = http://m-selig.ae.illinois.edu/ads/coord/ag04.dat
Width = 10
LeadingEdgeOffset = 0
Rotation = 0
RotationPosition = 0.5

[TipChord]
Profile = http://m-selig.ae.illinois.edu/ads/coord/ag09.dat
Width = 8
LeadingEdgeOffset = 2
Rotation = 0
RotationPosition = 0.5

[Panel]
Side = right
Width = 24
SheetingTop = 0.0625
SheetingBottom = 0.0625
StockLeadingEdge = 0
StockTrailingEdge = 0
TrimFromRootSide = 0
TrimFromTipSide = 0

[Machine]
Width = 30
FoamHeight = 2
FoamDepth = 10
Kerf = 0.075
```

## Config File Sections

### RootChord
Define the properties of your root chord here
```cfg
[RootChord]
Profile = http://m-selig.ae.illinois.edu/ads/coord/ag04.dat
Width = 10
LeadingEdgeOffset = 0
Rotation = 0
RotationPosition = 0.5
...
```
* **Profile** - Filename of the profile to use for the chord.
* **Width** - Width of the chord, measured from the front to back of the wing at the chord position.
* **LeadingEdgeOffset** - How far should the chord be offset forward or backwards.  Positive value moves chord aft  - see below for detailed explanation.  
* **Rotation** - defines washout - positive value angles leading edge upwards
* **RotationPosition** - Position to rotate as a percentage of the chord to rotate.  ex: 0.5 = 50%; 0.25 = 25%

### TipChord
Define the properties of your tip chord here
```cfg
...
[TipChord]
Profile = http://m-selig.ae.illinois.edu/ads/coord/ag09.dat
Width = 8
LeadingEdgeOffset = 2
Rotation = 0
RotationPosition = 0.5
...
```

Definitions are the same as the RootChord


### Panel
```cfg
...
[Panel]
Width = 24
StockLeadingEdge = 0
StockTrailingEdge = 0
SheetingTop = 0.0625
SheetingBottom = 0.0625
...
```
 * **Width** - Width of the total wing panel.  This is usually going to be half of the total span unless you are creating multiple panels.
 * **StockLeadingEdge** - Allowance for stock on the leading edge.  This is useful if you want to glue on a wooden block on the leading edge that you will eventually sand down to the airfoil shape.
 * **StockTrailingEdge** - Allowance for stock on the trailing edge.  This is useful if you want to glue on a wooden trailing edge stock that you will sand down to the airfoil shape.
 * **SheetingTop** - Allowance for sheeting on the top of the profile - the profile will be reduced by this amount.
 * **SheetingBottom** - Allowance for sheeting on the bottom of the profile - the profile will be reduced by this amount.



### Machine
```cfg
...
[Machine]
Width = 30
FoamHeight = 2
FoamDepth = 10
Kerf = 0.075
```
 * **Width** -  Width of the distance between the pillars of your foam cutter.  This should be measured to where the hotwire is anchored on each pillar
 * **FoamHeight** 
 * **FoamDepth**
 * **Kerf** -  Amount of room to offset the hotwire so an accurate amount of foam is cut


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