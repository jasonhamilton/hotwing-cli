<p align="center">
  <img src="https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/hotwing_logo.png"/>
</p>

HotWing-cli is a is a command-line-based Gcode generator for cutting model aircraft wings on a 4-axis CNC foam cutter ([like this](http://www.foamlinx.com/foamlinx-small-hot-wire-cnc-foam-cutters.html)). The user defines wing design parameters in a config file, which is then parsed by and converted to gcode by HotWing-cli. HotWing-cli is built on the [hotwing-core library](https://github.com/jasonhamilton/hotwing-core).

[![Build Status](https://travis-ci.org/jasonhamilton/hotwing-cli.svg?branch=master)](https://travis-ci.org/jasonhamilton/hotwing-cli)
![Versions](https://img.shields.io/badge/Python-2.7%2C%203.6-blue.svg)

# Installation

## Install From Source

1) Make sure you have Python and Pip installed.
2) Download the repository to your computer.
3) Navigate to the repository folder ```cd /my/folder/hotwing-cli``` in your terminal.
4) Install Dependencies ```pip install -r requirements.txt```
5) Install HotWing-CLI ```pip install .```

## Download Binaries

The stand-alone binaries are an easy way to get started.  The binaries have scripts that allow you to run the software without using the command line.  If you want to avoid the command like see the article on [avoiding the command line](https://github.com/jasonhamilton/hotwing-cli/blob/master/docs/avoiding-the-command-line.md).

<center>

| [![Windows Binary](https://png.icons8.com/windows8/color/96)](https://github.com/jasonhamilton/hotwing-cli/raw/master/bin/hotwing-cli-win.zip) |  [![OSX Binary](https://png.icons8.com/apple-logo/color/96)](https://github.com/jasonhamilton/hotwing-cli/raw/master/bin/hotwing-cli-osx.zip) |  [![Linux Binary](https://png.icons8.com/linux/color/96)]() |
| :---:  	|     :---:      |         :---: |
| [Windows](https://github.com/jasonhamilton/hotwing-cli/raw/master/bin/hotwing-cli-win.zip) |  [OSX](https://github.com/jasonhamilton/hotwing-cli/raw/master/bin/hotwing-cli-osx.zip)    | Linux   |

</center>

# Usage

## Quick Start

1) Install HotWing-cli per the [Installation Instructions](https://github.com/jasonhamilton/hotwing-cli/blob/master/README.md#installation)
2) Generate a config file by running ```hotwing-cli init myconfig.cfg``` or copy the [sample config file](https://github.com/jasonhamilton/hotwing-cli/blob/master/sample-config.cfg).
3) Modify the config file.  See the [Config File Options section](https://github.com/jasonhamilton/hotwing-cli/blob/master/docs/config-options.md) for details.
4) Run HotWing  ```hotwing-cli parse path-to-my-config.cfg```.  

The previous command output the Gcode to the screen but we can output it to a file.  
```sh
# You can redirect the output
$ hotwing-cli parse path-to-my-config.cfg > saved-gcode.ngc

# Or specify an output file with the -o parameter
hotwing-cli parse path-to-my-config.cfg -o saved-gcode.ngc 
```
For a more detailed walk through see this [tutorial](https://github.com/jasonhamilton/hotwing-cli/blob/master/docs/tutorial.md)

## Command Line Arguments

```sh
$ hotwing-cli -h # see additional options
```

### Synopsis

hotwing-cli COMMAND FILE [OPTION]...

### Options
  **command** Available: parse, init. Parse takes an input config file and converts it to gcode.  Init creates a new config file.

  **-o** Output file to write to.  If not specified, the output will be written to stdout.

  **-d** Turn on debugging.  The output will be tab separated values instead of gcode.  This also outputs images of profiles as they are created (requires PILLOW).

  **-s** Side to cut - 'l' or 'r'. (default='r')

  **-t** Trims the wing panel before cutting.  Specifies the section of wing to cut, starting at the root to the tip. For example '10-20' will cut a section starting at 10 units from the root and ending 20 units from the root (total width of 10 units).

  **-p** The number of points to interpolate/cut each profile surface (top/bottom).  (default=200)

  **-l** Distance to place the panel from the left machine pillar.  If not specified, the panel will be centered between the machine pillars.

