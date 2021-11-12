from constants import *
import pygame as pg
import numpy as np
from functools import reduce
from operator import or_


'''
 Performs bit shifting on a bitboard
-------------------------------------
bb (int)		:	Bitboard to shift

amount (int)	:	How many places to shift by
					Positive shifts right
					Negative shifts left
'''
def shift(bb, amount):
	if amount > 0:
		return bb << amount
	else:
		return bb >> -amount


'''
 Prints a bitboard as a chess board in terminal
------------------------------------------------
'''
def bbprint(bb):
	# Creates string (length 64) from binary
	binary_str = str(bin(bb))[2:]
	binary_str = binary_str.zfill(64)
	print('\nBitboard: {}\n'.format(binary_str))
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

'''
  Prints binary representation of number
 with </> showing if positive or negative
------------------------------------------
'''
def binprint(bb):
	if bb < 0:
		print('<', format(((1<<64)-1) & bb,'#066b'))
	else:
		print('>', format(bb, '#066b'))


'''
 Return Least/Most Significant Bit
-----------------------------------
'''
def find_LSB(n):
	return int(np.log2(n & -n))
def find_MSB(n):
	return int(np.log2(n))


'''
 Return number of bits in Bitboard
-----------------------------------
'''
def count_bits(bb):
	count = 0
	while bb:
		count += 1
		bb 		&= bb-1
	return count



'''
 Finds nearest bit in a direction
----------------------------------
'''
def find_nth_piece(pieces, direction, n=1):
	if pieces:
		# Initialise no nearest bit
		closest_bit = EMPTY
		
		# Find smallest bit index if moving in positive direction
		if direction in POSITIVE_DIRECTIONS:
			find_closest_bit = find_LSB
		# Otherwise fine largest bit index
		else:
			find_closest_bit = find_MSB


		# While diving to depth 'n'
		while n > 0:
			# Get the closest bit
			closest_bit = 1 << find_closest_bit(pieces)
			# Remove from bitboard of pieces
			pieces ^= closest_bit
			# Iterate
			n -= 1

		return closest_bit
	else:
		return 0



'''
 Import image as pygame image object
-------------------------------------
'''
def import_image(name):
	filename = 'img/{}.png'.format(name)
	img = pg.image.load(filename).convert_alpha()
	img = pg.transform.smoothscale(img, (SQ_SIZE, SQ_SIZE))
	return img

'''
 Convert between 3 representations of position: bb, cn and xy
--------------------------------------------------------------
'''
def cn2bb(cn):
	col = ord(cn[0]) - ord('a')
	row = ord(cn[1]) - ord('1')

	bb = shift(START, row*8 + col)
	return bb

def cn2xy(cn):
	col = ord(cn[0]) - ord('a')
	row = ord(cn[1]) - ord('1')

	x = col * SQ_SIZE
	y = BOARD_HEIGHT - (row*SQ_SIZE) - SQ_SIZE

	return(x,y)

def bb2cn(bb):
	# Find the bit location, assuming it's a single bit bb
	bb_bit = find_LSB(bb)

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


'''
 Take in a list of single-bit bitboards and return a combined bitboard
-----------------------------------------------------------------------
'''
def bblist2bb(bblist):
	# bb = EMPTY
	# for bit in bblist:
	# 	bb |= int(bit)
	# return bb
	return reduce(or_, bblist)
