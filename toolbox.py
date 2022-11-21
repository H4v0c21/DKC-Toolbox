import sys
import util_functions as util



command_list = [
	'x: exit',
	'c, commands, h, help: (lists all commands)',
	'1: import_palette_image',
	'2: export_palette_image',
	'3: import_palette_pal',
	'4: export_palette_pal',
	'5: import_raw_bin',
	'6: export_raw_bin',
	'7: import_rareware_palette_image',
	'8: export_rareware_palette_image',
	'9: import_gangplank_palette_image',
	'10: export_gangplank_palette_image'
]

def command_parser(command_id, arg_mode, arg_count):
	match command_id:

		case 'c' | 'commands' | 'h' | 'help':
			print('COMMANDS:')
			for command_name in command_list:
				print(command_name)

		case 'import_palette_image' | '1':
			print('Importing palette from image file\n')
		
			if arg_mode == True:
				if arg_count != 5:
					print('ERROR 00: Incorrect number of arguments specified.')
					return
				
				image_path = str(sys.argv[2])
				rom_path = str(sys.argv[3])
				palette_address = int(sys.argv[4], 16)
				
			else:
				image_path = str(input('Enter image file path (palette input):\n'))
				rom_path = str(input('Enter ROM file path:\n'))
				palette_address = int(input('Enter data address:\n'), 16)
			
			palette_bin = util.image_to_bin(image_path)
			rom_data = util.load_file(rom_path)
			palette_address = util.snes_to_rom_address(palette_address)

			rom_data = util.write_to_chunk(rom_data, palette_bin, palette_address)
			util.save_file(rom_path, 0, rom_data)
			return
		
		
		
		case 'export_palette_image' | '2':
			print('Exporting palette to image file\n')
		
			if arg_mode == True:
				if arg_count != 6:
					print('ERROR 00: Incorrect number of arguments specified.')
					return
				
				rom_path = str(sys.argv[2])
				palette_address = int(sys.argv[3], 16)
				color_count = int(sys.argv[4])
				output_path = str(sys.argv[5])
				
			else:
				rom_path = str(input('Enter ROM file path:\n'))
				palette_address = int(input('Enter palette address:\n'), 16)
				color_count = int(input('Enter number of colors:\n'))
				output_path = str(input('Enter image file path (palette output):\n'))
			
			rom_data = util.load_file(rom_path)
			palette_address = util.snes_to_rom_address(palette_address)
			palette_bin = util.get_data_chunk(rom_data, palette_address, color_count * 2)
			
			if color_count > 15:
				util.bin_to_image(palette_bin, 16, output_path)
			else:
				util.bin_to_image(palette_bin, color_count, output_path)
			return
		
		
		
		case 'import_palette_pal' | '3':
			print('Importing PAL file\n')
		
			if arg_mode == True:
				if arg_count != 5:
					print('ERROR 00: Incorrect number of arguments specified.')
					return
				
				pal_path = str(sys.argv[2])
				rom_path = str(sys.argv[3])
				palette_address = int(sys.argv[4], 16)
				
			else:
				pal_path = str(input('Enter PAL file path (input):\n'))
				rom_path = str(input('Enter ROM file path:\n'))
				palette_address = int(input('Enter palette address:\n'), 16)
			
			pal_data = util.load_file(pal_path)
			palette_bin = util.pal_to_bin(pal_data)
			rom_data = util.load_file(rom_path)
			palette_address = util.snes_to_rom_address(palette_address)

			rom_data = util.write_to_chunk(rom_data, palette_bin, palette_address)
			util.save_file(rom_path, 0, rom_data)
			return
		
		
		
		case 'export_palette_pal' | '4':
		
			print('Exporting PAL file\n')
		
			if arg_mode == True:
				if arg_count != 6:
					print('ERROR 00: Incorrect number of arguments specified.')
					return
				
				rom_path = str(sys.argv[2])
				palette_address = int(sys.argv[3], 16)
				color_count = int(sys.argv[4])
				output_path = str(sys.argv[5])
				
			else:
				rom_path = str(input('Enter ROM file path:\n'))
				palette_address = int(input('Enter palette address:\n'), 16)
				color_count = int(input('Enter number of colors:\n'))
				output_path = str(input('Enter PAL file path (output):\n'))
			
			rom_data = util.load_file(rom_path)
			palette_address = util.snes_to_rom_address(palette_address)
			palette_bin = util.get_data_chunk(rom_data, palette_address, color_count * 2)

			palette_pal = util.bin_to_pal(palette_bin)
			util.save_file(output_path, 0, palette_pal)
			return
		
		
		
		case 'import_raw_bin' | '5':
			print('Importing raw data from file\n')
		
			if arg_mode == True:
				if arg_count != 5:
					print('ERROR 00: Incorrect number of arguments specified.')
					return
				
				input_path = str(sys.argv[2])
				rom_path = str(sys.argv[3])
				data_address = int(sys.argv[4], 16)

			else:
				input_path = str(input('Enter data file path (input):\n'))
				rom_path = str(input('Enter ROM file path:\n'))
				data_address = int(input('Enter data address:\n'), 16)
			
			rom_data = util.load_file(rom_path)
			input_data = util.load_file(input_path)
			data_address = util.snes_to_rom_address(data_address)

			rom_data = util.write_to_chunk(rom_data, input_data, data_address)
			util.save_file(rom_path, 0, rom_data)
			return
		
		case 'export_raw_bin' | '6':
			print('Exporting raw data to file\n')
		
			if arg_mode == True:
				if arg_count != 6:
					print('ERROR 00: Incorrect number of arguments specified.')
					return
				
				rom_path = str(sys.argv[2])
				data_address = int(sys.argv[3], 16)
				data_size = int(sys.argv[4])
				output_path = str(sys.argv[5])
				
			else:
				rom_path = str(input('Enter ROM file path:\n'))
				data_address = int(input('Enter data address:\n'), 16)
				data_size = int(input('Enter data size (Bytes):\n'))
				output_path = str(input('Enter data file path (output):\n'))
			
			rom_data = util.load_file(rom_path)
			data_address = util.snes_to_rom_address(data_address)
			data = util.get_data_chunk(rom_data, data_address, data_size)
			
			util.save_file(output_path, 0, data)
			return
		
		
		
		case 'import_rareware_palette_image' | '7':
			print('Importing Rareware logo palette from image file\n')
		
			if arg_mode == True:
				if arg_count != 5:
					print('ERROR 00: Incorrect number of arguments specified.')
					return
				
				image_path = str(sys.argv[2])
				rom_path = str(sys.argv[3])
				palette_address = int(sys.argv[4], 16)

			else:
				image_path = str(input('Enter image file path (input):\n'))
				rom_path = str(input('Enter ROM file path:\n'))
				palette_address = int(input('Enter Rareware palette address (Default is 80B337):\n'), 16)
				
			rom_data = util.load_file(rom_path)
			palette_address = util.snes_to_rom_address(palette_address)
			
			palette_bin = util.image_to_rare_logo(image_path)
			
			rom_data = util.write_to_chunk(rom_data, palette_bin, palette_address)
			util.save_file(rom_path, 0, rom_data)

			return



		case 'export_rareware_palette_image' | '8':
			print('Exporting Rareware logo palette to image file\n')
		
			if arg_mode == True:
				if arg_count != 5:
					print('ERROR 00: Incorrect number of arguments specified.')
					return
				
				rom_path = str(sys.argv[2])
				palette_address = int(sys.argv[3], 16)
				output_path = str(sys.argv[4])
				
			else:
				rom_path = str(input('Enter ROM file path:\n'))
				palette_address = int(input('Enter Rareware palette address (Default is 80B337):\n'), 16)
				output_path = str(input('Enter image file path (output):\n'))
			
			rom_data = util.load_file(rom_path)
			palette_address = util.snes_to_rom_address(palette_address)
			palette_bin = util.get_data_chunk(rom_data, palette_address, 96)
			
			util.rare_logo_to_image(palette_bin, 16, output_path)
			return


		
		case 'import_gangplank_palette_image' | '9':
			print('Importing Gangplank Galley palette from image file\n')
			
			if arg_mode == True:
				if arg_count != 7:
					print('ERROR 00: Incorrect number of arguments specified.')
					return
				
				image_a_path = str(sys.argv[2])
				image_b_path = str(sys.argv[3])
				rom_path = str(sys.argv[4])
				palette_address = int(sys.argv[5], 16)
				table_address = int(sys.argv[6], 16)

			else:
				image_a_path = str(input('Enter palette A image file path (input):\n'))
				image_b_path = str(input('Enter palette B image file path (input):\n'))
				rom_path = str(input('Enter ROM File Path:\n'))
				palette_address = int(input('Enter Gangplank Galley palette address (Default is FD334E):\n'), 16)
				table_address = int(input('Enter Gangplank Galley sub table address (Default is FD364E):\n'), 16)

			palette_a_bin = util.image_to_gangplank(image_a_path)
			palette_b_bin = util.image_to_gangplank(image_b_path)
			sub_table = util.generate_subtraction_table(palette_a_bin, palette_b_bin)

			rom_data = util.load_file(rom_path)
			palette_address = util.snes_to_rom_address(palette_address)
			table_address = util.snes_to_rom_address(table_address)

			rom_data = util.write_to_chunk(rom_data, palette_a_bin, palette_address)
			rom_data = util.write_to_chunk(rom_data, sub_table, table_address)
			
			util.save_file(rom_path, 0, rom_data)

			return



		case 'export_gangplank_palette_image' | '10':
			print('Exporting Gangplank Galley palette to image file\n')
			
			if arg_mode == True:
				if arg_count != 7:
					print('ERROR 00: Incorrect number of arguments specified.')
					return
				
				rom_path = str(sys.argv[2])
				palette_address = int(sys.argv[3], 16)
				table_address = int(sys.argv[4], 16)
				output_a_path = str(sys.argv[5])
				output_b_path = str(sys.argv[6])
				
			else:
				rom_path = str(input('Enter ROM file path:\n'))
				palette_address = int(input('Enter Gangplank Galley palette address (Default is FD334E):\n'), 16)
				table_address = int(input('Enter Gangplank Galley sub table address (Default is FD364E):\n'), 16)
				output_a_path = str(input('Enter start palette file path (output):\n'))
				output_b_path = str(input('Enter end palette file path (output):\n'))
			
			rom_data = util.load_file(rom_path)
			
			palette_address = util.snes_to_rom_address(palette_address)
			table_address = util.snes_to_rom_address(table_address)
			
			palette_bin = util.get_data_chunk(rom_data, palette_address, 0x300)
			table_bin = util.get_data_chunk(rom_data, table_address, 0x300)
			
			util.gangplank_to_image(palette_bin, 16, output_a_path)
			palette_bin = util.subtract_from_table(palette_bin, table_bin, 32)
			util.gangplank_to_image(palette_bin, 16, output_b_path)

			return
		
		
		
		case _:
			print('ERROR 03: Invalid command.')



def main():
	print('[DKC Toolbox v0.02]\n[Created By: H4v0c21]\n')
	
	arg_count = len(sys.argv)

	if arg_count == 1:
		arg_mode = False
		
		print('COMMANDS:')
		for command_name in command_list:
			print(command_name)

		while True:
			command_id = input('\nEnter a command or command number (You can also use command line arguments, see the readme for details):\n')
			if command_id == 'exit' or command_id == 'x':
				print('Exiting')
				return
			command_parser(command_id, arg_mode, arg_count)
			print('Done.')
		return
	else:
		print('Running command from provided arguments')
		arg_mode = True
		command_id = sys.argv[1]
		command_parser(command_id, arg_mode, arg_count)
		print('Done.')
		return



if __name__ == '__main__':
	main()