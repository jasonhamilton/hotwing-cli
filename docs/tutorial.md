

# Overview


For this tutorial it's assumed that you've already installed HotWing-cli and know how to run the software to generate Gcode from the sample config file.  I will walk you through how to design and create a wing, then output the Gcode file.

Here is the wing we'll be designing in this tutorial:

![Whole Wing](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_wing_whole.png)

As you can see the wing measures 65" long from tip to tip, has a root chord length of 12" and a tip chord length of 7".  In HotWing we work with wing halves, so let's see what that looks like.

![Half Wing](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_wing_half.png)



# Setting up the Config File

## Project

For this project we we'll be working in inches, so in the Project section we will specify the units.

```cfg
[Project]
Units = inches
...
```
**Units** - Defines the project to be in 'inches' or 'millimeters'.  Default is inches if not specified.

## RootChord

For this wing, I'm going to use the RG-14 airfoil. Working with the copied sample config file, I'll start by modifying the [RootChord] section.

```cfg
...
[RootChord]
Profile = http://airfoiltools.com/airfoil/seligdatfile?airfoil=rg14-il
Width = 12
LeadingEdgeOffset = 0
Rotation = 0
RotationPosition = 0.5
```

**Profile** - The profile is a URL to the airfoil coordinates. The software accepts Selig and Lednicer type coordinates files.  You can use an airfoil coordinates file on your computer or a URL to the file.

**Width** - We know the width from the design above is 12" at the root.

**LeadingEdgeOffset** - We want the tip of the airfoil to be at 0 - I.E. we don't want to move it.

**Rotation** - Leave this at 0.  I don't want to rotate this chord.

**RotationPosition** - This doesn't matter since the Rotation Parameter is 0.


## TipChord

Now let's modify the tip chord.  Similar to the Root but let's take a look at some of the other Parameters.

```cfg
...
[TipChord]
Profile = http://m-selig.ae.illinois.edu/ads/coord/ag09.dat
Width = 7
LeadingEdgeOffset = 5
Rotation = -1
RotationPosition = 0.25
...
```

**LeadingEdgeOffset** - To get the shape that we want we need to define the LeadingEdgeOffset.  If we don't define the LeadingEdgeOffset, the leading edge's will be straignt and the trailing edge will sweep forward like this:

![Offset Example 1](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_le_offset_ex_1.png)

By changing the LeadingEdgeOffset to 5, we can produce a wing where the trailing edge has no sweep and the leading edge sweeps back.  Because the root chord is 12 and the tip is 7, we need to define a LeadingEdgeOffset of 5 (12-7) to get our desired wing shape.

![Offset Example 2](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_le_offset_ex_2.png)


**Rotation** - For this design we need 1 degree of washout on the tip, so I need to set the Rotation Parameter to -1.  This will angle the tip downward by 1 degree.  To angle the tip upward, use a positive number.

**RotationPosition** - Since the Rotation value is now being used, the RotationPosition will be takend into account.  This value is the point along the chord (measured from front to back) where the foil will be rotated.  A value of 0.25 tells HotWing to rotate the foil around a point at 25% of the chord distance.  Since our chord is 7 inches long, the rotation will occur 1.75 (25%\*7) inches back from the tip of the foil.

## Panel

```cfg
...
[Panel]
Width = 32.5
StockLeadingEdge = 0.5
StockTrailingEdge = 1
SheetingTop = 0.0625
SheetingBottom = 0.0625
...
```

**Width** - The total width of the half wing.  

**StockLeadingEdge** - The stock leading edge is an allowance for a piece of wood stock that will be glued on the leading edge to give it additional strength.  This wood will then be sanded by hand to the shape of the airfoil.  This wing will use a 0.5" x 0.5" piece of stock, so the StockLeadingEdge parameter is set to 0.5.  You can set this to a lower number if you want some additional allowance, say 0.4".  The software simply trims the indicated amount from the leading edge of the wing.

**StockTrailingEdge** - The StockTrailingEdge parameter is similar to StockLeadingEdge, except it is trimmed from the trailing edge instead.  Typically you'll use aileron stock here.  This amount is just measured from the trailing edge - it's up to you to make sure your stock will cover the specified area.

![Stock Example 1](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_stock_1.png)

Now our cut foam will look like this:

![Stock Example 2](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_stock_2.png)

And after we glue on and shape the stock we will end up with something like this:

![Stock Example 3](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_stock_3.png)

**SheetingTop and SheetingBottom** - The next parameters that need to be set are SheetingTop and SheetingBottom.  These define an allowance for balsa, plywood, or other types of sheeting.  This wing will be sheeted with 1/16 inch balsa on the top and bottom, so I set these to 0.0625.  The sheeting can be visualized in this image:

![Sheeting Example](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_sheeting.png)

## Machine

```cfg
...
[Machine]
Width = 30
FoamHeight = 2
SafeHeight = 4
Feedrate = 5
Kerf = 0.075
```

**Width** - Set Width to the width of your foam cutting machine.

**FoamHeight** - Specify the size of your foam block you'll be using to cut out your wing.

**SafeHeight** - Specify the safe height of your machine to clear any workpieces.

**Feedrate** - CNC feedrate speed in units / minute.

**Kerf** - Kerf is the amount of room to offset the hotwire so an accurate amount of foam is cut.

# Generating Gcode

Now that we've set up the config file, we need to use HotWing to generate the Gcode for us.

Typically you would just run

```sh
# generate the code for the right side (default)
$ hotwing-cli parse myconfig.cfg > right.ngc

# generate the code for the left side (use the "-s l") to specify left
$ hotwing-cli parse myconfig.cfg -s l > left.ngc
```

But this produces the following error:

```
Error: Panel (32.5) is bigger than the machine width (30).
```

This error is telling us that the panel we've defined is 32.5 inches but our machine width is only 30, so it's not physically possible to make this cut.

## Splitting the Panel

In order for the panel to fit into our machine, we need to split the panel into parts.  You can split the panel however you like but in this example I will be splitting the panel in half, which will give us two panels of 16.25 (32.5/2) inches each.  Here's what this looks like visually.

![Splitting Example](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_wing_sections.png)


```sh
# This command splits the panel at 0 distance from the root chord (so no split)
# up to 16.25 inches from the root chord.  This produces panel 1
$ hotwing-cli parse myconfig.cfg -t 0-16.25 -o right_a.ngc

# This command splits the panel at 16.25 distance from the root chord
# up to 32.5 inches from the root chord (so no split).  This produces panel 2
$ hotwing-cli parse myconfig.cfg -t 16.25-32.5 -o right_b.ngc

# This command splits the panel at 0 distance from the root chord (so no split)
# up to 16.25 inches from the root chord.  We also tell the software that we want to cut
# the left side of the wing.  This produces panel 3
$ hotwing-cli parse myconfig.cfg -s l -t 0-16.25 -o left_a.ngc

# This command splits the panel at 16.25 distance from the root chord
# up to 32.5 inches from the root chord (so no split).  This produces panel 2
$ hotwing-cli parse myconfig.cfg -s l -t 16.25-32.5 -o left_b.ngc
```

Now you have 4 gcode files to cut the panels for your wing.