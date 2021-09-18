from constants import *
import pygame as pg
from math import log2
import numpy as np



'''
Holds all position information in chess notation (cn), bitboards (bb), pygame coordinates (xy)

a1 == 0b0000000000000000000000000000000000000000000000000000000000000001
a2 == 0b0000000000000000000000000000000000000000000000000000000000000010
...
h8 == 0b1000000000000000000000000000000000000000000000000000000000000000
'''

class Position:
	def __init__(self, cn=None, bb=None, xy=None):
		# Reads in one of cn, bb or xy, and creates otehrs from that
		if cn and not(bb) and not(xy):
			self.cn = cn
			self.bb = cn2bb(cn)
			self.x, self.y = cn2xy(cn)
		elif bb and not(cn) and not(xy):
			self.cn = bb2cn(bb)
			self.bb = bb
			self.x, self.y = bb2xy(bb)
		elif xy and not(cn) and not(bb):
			x, y = xy
			self.cn = xy2cn(x, y)
			self.bb = xy2bb(x, y)
			self.x, self.y = bb2xy(self.bb)
		else:
			raise(Exception('''Position object has incorrect number of input arguments!
							   ONE of the following should have a value:
							   CN:{}
							   BB:{}
							   XY:{}'''.format(cn, bb, xy)))

	@property
	def file(self):
		return self.cn[0]


	@property
	def rank(self):
		return int(self.cn[1])
		
	
	# Positions are equal if their bitboards are the same
	def __eq__(self, other):
		return self.bb == other.bb


'''
Generates lines of attack accounting for blocking pieces

'''

def line_of_attack(position, gs, direction):
	# Create the ray as per empty board
	ray_bb = RAY_BBS[position.cn][direction]
	# Get location of all pieces on board
	occupancy = gs.active_bb
	# Find overlap
	overlap = ray_bb & occupancy
	# If there's any overlap
	if overlap:
		# Find the first square in array that's occupied
		if direction > 0:
			blocking_piece = START_BB << (find_LS1B(overlap))
		else:
			blocking_piece = START_BB << (find_MS1B(overlap))
		blocking_piece_cn = bb2cn(blocking_piece)
		# XOR these rays to get blocked ray
		ray_bb ^= RAY_BBS[blocking_piece_cn][direction]

	return ray_bb

def limit_absolute_pins(position, gs):
	xray_bb = FULL_BB
	# For each xray on king
	for xray in gs.xrays_on_king:
		# If this piece is the xrayed piece
		if position.bb & xray:
			# Limit to moving along xray axis
			xray_bb &= xray
	return xray_bb

def limit_check_escapes(position, gs):
	defend_bb = FULL_BB
	# Limit defending squares to those that block ray and capture jumper
	if gs.check:
		# Block ray attack, or capture ray piece
		for line in gs.lines_on_king:
			defend_bb &= line

		# Capture jump piece
		for jump in gs.jumps_on_king:
			defend_bb &= jump

	return defend_bb

'''
Misc functions
'''
def print_bb(bb):
	print('')
	print('')
	# Creates string (length 64) from binary
	binary_str = str(bin(bb))[2:]
	binary_str = binary_str.zfill(64)
	# Resize the array into 8x8
	char_array = np.array(list(binary_str))
	char_array = np.reshape(char_array, (8, 8))
	char_array = np.fliplr(char_array)

	for i in range(8):
		rank = '{}| '.format(8-i)
		for j in range(8):
			char =  char_array[i,j]
			if char == '0':
				rank += '. '
			else:
				rank += '# '
		print(rank)
	# print(' |        ')
	print('-+-----------------')
	print(' | a b c d e f g h ')
	print('<=================>')


	

# Returns location of first non-zero bit in n
def bit_location(n):
	return int(log2(n & -n))

# Return least significant 1 bit
def find_LS1B(n):
	return int(log2(n & -n))

# Return most significant 1 bit
def find_MS1B(n):
	return int(log2(n))

# # Shifts bb left or right, works if amount is negative
# def shift(bb, amount):
# 	if amount > 0:
# 		return bb << amount
# 	else:
# 		return bb >> -amount

# Import image as pygame image object
def import_image(name):
	filename = 'img/{}.png'.format(name)
	img = pg.image.load(filename).convert_alpha()
	img = pg.transform.smoothscale(img, (SQ_SIZE, SQ_SIZE))
	return img





'''
Convert between 3 representations of position:
bb, cn and xy

'''
def cn2bb(cn):
	col = ord(cn[0]) - ord('a')
	row = ord(cn[1]) - ord('1')

	bb = shift(START_BB, row*8 + col)
	return bb

def cn2xy(cn):
	col = ord(cn[0]) - ord('a')
	row = ord(cn[1]) - ord('1')

	x = col * SQ_SIZE
	y = BOARD_HEIGHT - (row*SQ_SIZE) - SQ_SIZE

	return(x,y)

def bb2cn(bb):
	bb_bit = bit_location(bb)

	col = bb_bit % 8
	row = bb_bit // 8

	col += ord('a')
	row += ord('1')

	cn = chr(col)+chr(row)
	return cn

def bb2xy(bb):
	return cn2xy(bb2cn(bb))

def xy2cn(x, y):
	col = x // SQ_SIZE
	row = (BOARD_HEIGHT - y) // SQ_SIZE

	col += ord('a')
	row += ord('1')

	cn = chr(col)+chr(row)
	return cn

def xy2bb(x, y):
	return cn2bb(xy2cn(x, y))
