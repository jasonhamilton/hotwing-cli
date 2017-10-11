
For this tutorial it's assumed that you've already installed HotWing-cli and know how to run the software to generate Gcode from the sample config file.  I will walk you through how to design and create a wing, then output the Gcode file.

## Overview of the design

Here is the wing we'll be designing in this tutorial:

![Whole Wing](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_wing_whole.png)

As you can see the wing measures 65" long from tip to tip, has a root chord length of 12" and a tip chord length of 7".  In HotWing we work with wing halves, so let's see what that looks like.

![Half Wing](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_wing_half.png)

## Define the Root Chord

For this wing, I'm going to use the RG-14 airfoil. Working with the copied sample config file, I'll start by modifying the [RootChord] section.

```cfg
[RootChord]
Profile = http://airfoiltools.com/airfoil/seligdatfile?airfoil=rg14-il
Width = 12
LeadingEdgeOffset = 0
Rotation = 0
RotationPosition = 0.5
```

**Profile** - The profile is a URL to the airfoil coordinates. The software accepts Selig and Lednicer type coordinates files.  You can use an airfoil coordinates file on your computer or a URL to the file.

**Width** - We know the width from the design above is 12" at the root.

**LeadingEdgeOffset** - We want the tip of the airfoil to be at 0, I.E: we don't want to move it.

**Rotation** - Leave this at 0.  I don't want to rotate this chord.
**RotationPosition** - This doesn't matter since the Rotation Parameter is 0.


## Define the Tip Chord

Now let's modify the tip chord.

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

For this I need to define the LeadingEdgeOffset.  If I don't define the LeadingEdgeOffset, the tip of the airfoil will be at 0, which is the same tip as the root chord.  This means the leading edge of the wing will be projected out at a 90 degree angle and the trailing edge will sweep forward like this:

![Offset Example 1](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_le_offset_ex_1.png)

By changing the LeadingEdgeOffset to 5, we can produce a wing where the trailing edge has no sweep and the leading edge sweeps back.  Because the root chord is 12 and the tip is 7, we need to define a LeadingEdgeOffset of 5 (12-7) to get our desired wing shape.

![Offset Example 2](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_le_offset_ex_2.png)


I want 1 degree of washout on the tip, so I need to set the rotation to -1.  This will angle the tip downward by 1 degree.  If we want to angle the tip upward, you can us a positive number.

Since the Rotation value is now not 0, the RotationPosition will be used.  This value is where along the chord (measured from front to back) the foil will be rotated.  A value of 0.25 tells HotWing to rotate the foil around a point at 25% of the chord distance.  Since our chord is 7 inches long, the rotation will occur 1.75 (25%\*7) inches back from the tip of the foil.

## Define the Panel

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

The width is 32.5 inches since we are working with a wing half.  

The stock leading edge is an allowance for a piece of wood stock that will be glued on the leading edge to give it additional strength.  This wood will then be sanded by hand to the shape of the airfoil.  This wing will use a 0.5" x 0.5" piece of stock, so the StockLeadingEdge parameter is set to 0.5.  You can set this to a lower number if you want some additional allowance, say 0.4".  The software simply trims the indicated amount from the leading edge of the wing.

The StockTrailingEdge parameter is similar to StockLeadingEdge, except it is trimmed from the trailing edge instead.  Typically you'll use aileron stock here.  This amount is just measured from the trailing edge - it's up to you to make sure your stock will cover the specified area.

![Stock Example 1](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_stock_1.png)

Now our cut foam will look like this:

![Stock Example 2](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_stock_2.png)

And after we glue on and shape the stock we will end up with something like this:

![Stock Example 3](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_stock_3.png)

The next parameters that need to be set are SheetingTop and SheetingBottom.  These define an allowance for balsa, plywood, or other types of sheeting.  This wing will be sheeted with 1/16 inch balsa on the top and bottom, so I set these to 0.0625.  The sheeting can be visualized in this image:

![Sheeting Example](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/tutorial_sheeting.png)

## Setup the Machine

```cfg
...
[Machine]
Width = 30
FoamHeight = 2
FoamDepth = 10
Kerf = 0.075
```

Set Width to the width of your foam cutting machine.

FoamHeight and FoamDepth specify the size of your foam.

Kerf is the amount of room to offset the hotwire so an accurate amount of foam is cut.