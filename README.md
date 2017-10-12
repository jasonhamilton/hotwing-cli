
# HotWing-cli

![Hotwing Bird Logo](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/hotwing_logo.png)

HotWing-cli is a is a Gcode generator for cutting model aircraft wings on a 4-axis CNC foam cutter ([like this](http://www.foamlinx.com/foamlinx-small-hot-wire-cnc-foam-cutters.html)). It is based on the [hotwing-core library](https://github.com/jasonhamilton/hotwing-core) and allows a user to quickly and easily design their wings using a config file.

# Usage

## Installation
 
1) Make sure you have Python and Pip installed.
2) Download the repository to your computer.
3) Navigate to the repository folder ```cd /my/folder/hotwing-cli``` in your terminal.
4) Install Dependencies ```pip install -r requirements.txt```
5) Install HotWing-CLI ```pip install .```


## Quick Start

1) Install HotWing-cli per the [Installation Instructions](https://github.com/jasonhamilton/hotwing-cli/blob/master/README.md#installation)
2) Create a copy the [sample config file](https://github.com/jasonhamilton/hotwing-cli/blob/master/sample-config.cfg).
3) Modify the config file.  See the [Config File Options section](https://github.com/jasonhamilton/hotwing-cli/blob/master/sample-config.md) for details.
4) Run HotWing  ```hotwing-cli path-to-my-config.cfg```.  

The previous command output the Gcode to the screen but we can output it to a file.  
```sh
# You can redirect the output
$ hotwing-cli path-to-my-config.cfg > saved-gcode.ngc

# Or specify an output file with the -o parameter
hotwing-cli -o saved-gcode.ngc path-to-my-config.cfg
```
For a more detailed walk through see this [tutorial](https://github.com/jasonhamilton/hotwing-cli/blob/master/tutorial.md)

## Command Line Arguments

```sh
$ python hotwing.py -h # see additional options
```

### Synopsis

hotwing-cli [OPTION]... FILE


### Options
  **-o** Output file to write to.  If not specified, the output will be written to stdout.

  **-d** Turn on debugging.  The output will be tab separated values instead of gcode.  This also outputs images of profiles as they are created (requires PILLOW).

  **-s** Side to cut - 'l' or 'r'. (default='r')

  **-t** Trims the wing panel before cutting.  Specifies the section of wing to cut, starting at the root to the tip. For example '10-20' will cut a section starting at 10 units from the root and ending 20 units from the root (total width of 10 units).

  **-p** The number of points to interpolate/cut each profile surface (top/bottom).  (default=200)

