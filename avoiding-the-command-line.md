# Avoiding The Command Line

For those of you who don't like using the command line, we've included scripts in the binary files that allow you to simply double click a file to run the program.  This page will show you how to use the software without opening up a terminal.

## Download Contents
This tutorial assumes you're working with the binary downloads. With each of the binary downloads, you'll receive a folder containing a few files.

![Binary Contents](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/avoiding_cli_contents.png)

1) **The executable** named hotwing-cli.exe (Windows) or hotwing-cli (Mac and Linux).
2) **A sample config** named config.txt
3) **A script file** named parse_config.bat (Windows), parse_config.command (Mac), or parse_config.sh (Linux)

## Editing The Config File

All you need to do is open the config.txt file in your favorite text editor or Notepad (if you're on Windows) and modify the code according to the  [Config File Options section](https://github.com/jasonhamilton/hotwing-cli/blob/master/config-options.md).

![Binary Contents](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/avoiding_cli_config_edit.png)

## Running The Script

Just double click!

The script file - parse_config.bat (Windows), parse_config.command (Mac), or parse_config.sh (Linux) - invokes the software and sets any configuration options for HotWire.  The default script crates a left and right panel and outputs the gcode to output_right.txt and output_left.txt, respectively.  After running the default script the folder will looks something like:

![Binary Contents](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/avoiding_cli_script_output.png)


## Editing The Script File

In order to access some of the more advanced functionality you'll need to open the script file in your text editor and modify the line(s) that start with hotwing-cli.  The default config file looks something like:

![Binary Contents](https://raw.githubusercontent.com/jasonhamilton/hotwing-cli/master/img/avoiding_cli_config_script.png)

You can see the different configuration options in the [Command Line Arguments](https://github.com/jasonhamilton/hotwing-cli#command-line-arguments) section of the README.

After you are done editing the file, all you have to do is save it and then double click it!
