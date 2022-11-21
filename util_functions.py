import os
import math
from struct import *
from PIL import Image

def load_file(path):
	try:
		file = open(path, 'rb')
		while True:
			data = file.read(-1)  
			if not data:
				break
			return bytes(data)
	except IOError:
		print('ERROR 01: Failed to read ROM File.')
		return bytes()

def save_file(path, address, data):
	try:
		file = open(path, 'wb')
		if True:
			file.seek(address)
			file.write(data)
			return
	except IOError:
		print('ERROR 02: Failed to write ROM File.')
		return

def write_to_chunk(chunk, data, address):
	chunk = bytearray(chunk)
	chunk[address:address+len(data)] = data
	return chunk

def get_data_chunk(data, address, size):
	chunk = data[address:address+size]
	return chunk

def snes_to_rom_address(address):
	address &= 0x3FFFFF
	return address

#convert a color from 2 byte SNES to 24 bit RGB
def snes_to_rgb(snes_color):
	r = (snes_color & 0x1F) << 3
	g = (snes_color >> 5 & 0x1F) << 3
	b = (snes_color >> 10 & 0x1F) << 3
	r += r // 32
	g += g // 32
	b += b // 32
	return r,g,b

#convert a color from 24 bit RGB to 2 byte SNES
def rgb_to_snes(r,g,b):
	r = ((r >> 3) & 0xFF)
	g = ((g >> 3) & 0xFF)
	b = ((b >> 3) & 0xFF)
	snes_color = r + (g << 5) + (b << 10)
	return snes_color

#convert a block of bytes from 2 byte SNES to 24 bit RGB
def bin_to_pal(data):
	pal_pack = bytes()
	for i in range(0, len(data), 2):
		color = int.from_bytes(data[i:i+2], byteorder='little')
		r,g,b = snes_to_rgb(color)
		pal_pack += pack('BBB', r,g,b)
	return pal_pack

#convert a block of bytes from 24 bit RGB to 2 byte SNES
def pal_to_bin(data):
	bin_pack = bytes()
	for i in range(0, len(data), 3):
		r = int.from_bytes(data[i:i+1], byteorder='big')
		g = int.from_bytes(data[i+1:i+2], byteorder='big')
		b = int.from_bytes(data[i+2:i+3], byteorder='big')
		color = rgb_to_snes(r,g,b)
		bin_pack += pack('<h', color)
	return bin_pack

#convert a block of bytes from 2 byte SNES to an image file
def bin_to_image(data, width, path):
	color_count = len(data) / 2
	height = math.ceil(color_count / width)
	palette_image = Image.new("RGB", (width, height), (255, 0, 255))
	for y in range(height):
		for x in range(width):
			r,g,b = snes_to_rgb(int.from_bytes(data[((width*y)*2)+(x*2):((width*y)*2)+(x*2)+2], byteorder='little'))
			pixel_position = (x, y)
			palette_image.putpixel(pixel_position, (r,g,b))
	palette_image.save(path, os.path.splitext(path)[1].replace('.', ''))

#convert an image file to 2 byte SNES
def image_to_bin(path):
	with Image.open(path) as palette_image:
		palette_image = palette_image.convert('RGB')
		width, height = palette_image.size
		pixels = palette_image.load()
		bin_pack = bytes()
		for y in range(height):
			for x in range(width):
				pixel_position = (x, y)
				r, g, b = pixels[pixel_position]
				color = rgb_to_snes(r,g,b)
				bin_pack += pack('<h', color)
	return bin_pack
	
def rare_logo_to_image(data, width, path):
	color_count = len(data) // 3
	height = math.ceil(color_count / width)
	palette_image = Image.new("RGB", (width, height), (255, 0, 255))
	for y in range(height):
		for x in range(width):

			r = int.from_bytes(data[(y * width + x) * 3:(y * width + x) * 3 + 1], byteorder='big')
			g = int.from_bytes(data[(y * width + x) * 3 + 1:(y * width + x) * 3 + 2], byteorder='big')
			b = int.from_bytes(data[(y * width + x) * 3 + 2:(y * width + x) * 3 + 3], byteorder='big')
			
			r = (r & 0x1F) << 3
			g = (g & 0x1F) << 3
			b = (b & 0x1F) << 3
			r += r // 32
			g += g // 32
			b += b // 32
			pixel_position = (x, y)
			palette_image.putpixel(pixel_position, (r,g,b))		
	palette_image.save(path, os.path.splitext(path)[1].replace('.', ''))

def image_to_rare_logo(path):
	with Image.open(path) as palette_image:
		palette_image = palette_image.convert('RGB')
		width, height = palette_image.size
		pixels = palette_image.load()
		bin_pack = bytes()
		for y in range(height):
			for x in range(width):
				pixel_position = (x, y)
				r, g, b = pixels[pixel_position]
				r = ((r >> 3) & 0x1F)
				g = ((g >> 3) & 0x1F)
				b = ((b >> 3) & 0x1F)
				bin_pack += pack('>B', r)
				bin_pack += pack('>B', g)
				bin_pack += pack('>B', b)
	return bin_pack

def gangplank_to_image(data, width, path):
	color_count = len(data) // 6	#each color uses 6 bytes
	height = math.ceil(color_count / width)
	palette_image = Image.new("RGB", (width, height), (255, 0, 255))	#create a blank image
	
	for y in range(height):
		for x in range(width):
			#extract values from table
			#table format RRRR GGGG BBBB RRRR GGGG BBBB .... ....
			r = int.from_bytes(data[(y * width + x) * 6:(y * width + x) * 6 + 2], byteorder='little')	#get the red 16 bit value from the interleaved RGB table
			g = int.from_bytes(data[(y * width + x) * 6 + 2:(y * width + x) * 6 + 4], byteorder='little')	#get the green 16 bit value from the interleaved RGB table
			b = int.from_bytes(data[(y * width + x) * 6 + 4:(y * width + x) * 6 + 6], byteorder='little')	#get the blue 16 bit value from the interleaved RGB table
			
			#extract color from value
			r = ((r >> 8) & 0x1F)	#XBA, AND #$001F
			g = ((g >> 5) & 0x1F)	#AND #$03E0
			b = ((b >> 10) & 0x1F)	#AND #$7C00
			
			#convert to RGB24
			r = (r << 3) + (r // 32)
			g = (g << 3) + (g // 32)
			b = (b << 3) + (b // 32)
			
			#place pixels in image
			pixel_position = (x, y)
			palette_image.putpixel(pixel_position, (r,g,b))		
	palette_image.save(path, os.path.splitext(path)[1].replace('.', ''))

def image_to_gangplank(path):
	with Image.open(path) as palette_image:
		palette_image = palette_image.convert('RGB')
		width, height = palette_image.size
		pixels = palette_image.load()
		bin_pack = bytes()
		for y in range(height):
			for x in range(width):
				pixel_position = (x, y)
				r, g, b = pixels[pixel_position]
				
				r = ((r >> 3) & 0x1F)
				g = ((g >> 3) & 0x1F)
				b = ((b >> 3) & 0x1F)
				
				r = (r << 8)
				g = (g << 5)
				b = (b << 10)
				
				bin_pack += pack('<h', r)
				bin_pack += pack('<h', g)
				bin_pack += pack('<h', b)
	return bin_pack

def subtract_from_table(color_table, sub_table, amount):
	new_table = bytes()
	
	for i in range(0, len(color_table), 2):	#for every 16 bit word in the color table
		value_a = int.from_bytes(color_table[i:i+2], byteorder='little')	#get value from color table
		value_b = int.from_bytes(sub_table[i:i+2], byteorder='little')		#get value from subtraction table
		
		for j in range(amount):	#subtract from the color table multiple times
			value_a -= value_b
			value_a &= 0xFFFF	#because we are using 32 bit so underflow is different
		new_table += pack('<H', value_a)
	return new_table

#not the most accurate
def generate_subtraction_table(color_table_a, color_table_b):
	sub_table = bytes()
	
	for i in range(0, len(color_table_a), 2):	#for every 16 bit word in the color table
		value_a = int.from_bytes(color_table_a[i:i+2], byteorder='little')
		value_b = int.from_bytes(color_table_b[i:i+2], byteorder='little')

		value_c = (value_a - value_b) // 32
		value_c &= 0xFFFF
		
		sub_table += pack('<H', value_c)
	return sub_table

def nintendo_logo_to_image(data, width, path):
	color_count = len(data) // 2
	height = math.ceil(color_count / width)
	palette_image = Image.new("RGB", (width, height), (255, 0, 255))
	for y in range(height):
		for x in range(width):

			w = int.from_bytes(data[(y * width + x) * 2:(y * width + x) * 2 + 1], byteorder='big') & 0x1F
			b = int.from_bytes(data[(y * width + x) * 2 + 1:(y * width + x) * 2 + 2], byteorder='big') & 0x1F

			#convert to RGB24
			w = (w << 3) + (w // 32)
			b = (b << 3) + (b // 32)
			pixel_position = (x, y)
			palette_image.putpixel(pixel_position, (w,w,b))		
	palette_image.save(path, os.path.splitext(path)[1].replace('.', ''))

def image_to_nintendo_logo(path):
	with Image.open(path) as palette_image:
		palette_image = palette_image.convert('RGB')
		width, height = palette_image.size
		pixels = palette_image.load()
		bin_pack = bytes()
		for y in range(height):
			for x in range(width):
				pixel_position = (x, y)
				w, b = pixels[pixel_position]
				
				w = ((r >> 3) & 0x1F)
				b = ((b >> 3) & 0x1F)

				bin_pack += pack('>B', w)
				bin_pack += pack('>B', b)
	return bin_pack

def hdma_to_image(data, width, path):
	height = 512
	palette_image = Image.new("RGB", (width, height), (255, 0, 255))
	
	y = 0
	
	for index in range(0, len(data), 2):
		draw_height = int.from_bytes(data[index:index + 1], byteorder='big')
		color = int.from_bytes(data[index + 1:index + 2], byteorder='big')
		
		
		#print(color)
		
		brightness = color & 0x1F
		
		#print(brightness)
		
		brightness = (brightness << 3) + (brightness // 32)
		
		
		r = ((color & 0x20) >> 5) * brightness
		g = ((color & 0x40) >> 6) * brightness
		b = ((color & 0x80) >> 7) * brightness
		
		
		
		#r = (r << 3) + (r // 32)
		#g = (g << 3) + (g // 32)
		#b = (b << 3) + (b // 32)
		
		#print(r,g,b)
		
		for y_offset in range(y, y + draw_height, 1):
			for x in range(width):
				pixel_position = (x, y_offset)
				
				#print(draw_height, pixel_position)
				palette_image.putpixel(pixel_position, (r,g,b))
				
			palette_image.save(path, os.path.splitext(path)[1].replace('.', ''))
			
		y += draw_height
