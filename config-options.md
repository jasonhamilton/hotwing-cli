# Config File Options

A config file contains the contains the variables that define your wing.  The config file is organized into multiple sections that you can edit to get the perfect wing.  Start by copying the [sample config file](https://github.com/jasonhamilton/hotwing-cli/blob/master/sample-config.cfg) and use it as a starting point for creating your wing.  A sample config file looks like:

```cfg
[Project]
Units = inches

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
Width = 24
StockLeadingEdge = 0
StockTrailingEdge = 0
SheetingTop = 0.0625
SheetingBottom = 0.0625

[Machine]
Width = 30
FoamHeight = 2
FoamDepth = 10
Kerf = 0.075
```

## Config File Sections

### Project
Define the properties of your project herer
```cfg
[Project]
Units = inches
...
```
* **Units** - Defines the project's units to be in 'inches' or 'millimeters'.  Default is inches if not specified.


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