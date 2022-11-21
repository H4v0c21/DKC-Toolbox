[DKC Toolbox]
[Created by H4v0c21]

DISCLAIMER:
This tool is currently in its early prototyping stage and is subject to major changes. Feedback is always welcome and is extremely helpful.

DKC Toolbox is a tool written in python designed to provide basic data conversion and IO for the Donkey Kong Country SNES Trilogy.
It is designed to be the successor to BMP2SNES.

Notable features include being able to import/export a variety of unique DKC formats like color palettes.

REQUIREMENTS:
Python 3.10 or later
Pillow (Python Library)

This script is console based meaning there is no GUI and the interface is handled via console commands.
Commands can be fed into the script in two distinct ways.
You can also use the numeric ID of a command in place of its name.

If the script isn't passed any arguments it will prompt the user to enter a command and will ask for parameters to the command one at a time.
If the user runs the script with arguments it will take the command and parameters all at once. All parameters for a given command are required.

All addresses must be hexadecimal.
SNES and ROM addresses are allowed.
For example FD0CD0 and 3D0CD0 will both work.

Quantities and lengths must always be decimal.

Spaces should work for paths but you MUST enclose them in ""
For example: "test folder/spa ces.sfc"

All PNG paths must end in .png

Example use of command line arguments:
python.exe toolbox.py export_palette_image dkc2.sfc FD0CD0 128 exported_palette.png



COMMANDS:
x	exit
c/h	commands/help			(lists all commands)
1	import_palette_image		<input_image_path> <rom_path> <palette_address>
2	export_palette_image		<rom_path> <palette_address> <number_of_colors> <output_image_path>
3	import_palette_pal		<input_pal_path> <rom_path> <palette_address>
4	export_palette_pal		<rom_path> <palette_address> <number_of_colors> <output_image_path>
5	import_raw_bin			<input_bin_path> <rom_path> <data_address>
6	export_raw_bin			<rom_path> <data_address> <number_of_bytes> <output_bin_path>
7	import_rareware_palette_image	<input_image_path> <rom_path> <palette_address>
8	export_rareware_palette_image	<rom_path> <palette_address> <output_image_path>
9	import_gangplank_palette_image	<image_a_path> <image_b_path> <rom_path> <palette_address> <sub_table_address>
10	export_gangplank_palette_image 	<rom_path> <palette_address> <sub_table_address> <palette_a_output_image_path> <palette_b_output_image path>



Contact Info:
Discord:	H4v0c21#5523
YouTube		https://www.youtube.com/h4v0c21
Email:		alexcorley01@gmail.com

VERSION INFO:
Toolbox 0.02
Python 3.10.2
Pillow 9.0.1

Doc last updated 11/21/22