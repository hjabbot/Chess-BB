import numpy as np

from board_constants import *



####################################################################################
# ................................................................................ #
# .................................... FUNCTIONS ................................. #
# ................................................................................ #
####################################################################################




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
	bb = EMPTY
	for bit in bblist:
		bb |= int(bit)
	return bb







####################################################################################
# ................................................................................ #
# .................................... BITBOARDS ................................. #
# ................................................................................ #
####################################################################################


# .......................................................................... Squares

a8 = 1 << 56; b8 = 1 << 57; c8 = 1 << 58; d8 = 1 << 59; e8 = 1 << 60; f8 = 1 << 61; g8 = 1 << 62; h8 = 1 << 63
a7 = 1 << 48; b7 = 1 << 49; c7 = 1 << 50; d7 = 1 << 51; e7 = 1 << 52; f7 = 1 << 53; g7 = 1 << 54; h7 = 1 << 55
a6 = 1 << 40; b6 = 1 << 41; c6 = 1 << 42; d6 = 1 << 43; e6 = 1 << 44; f6 = 1 << 45; g6 = 1 << 46; h6 = 1 << 47
a5 = 1 << 32; b5 = 1 << 33; c5 = 1 << 34; d5 = 1 << 35; e5 = 1 << 36; f5 = 1 << 37; g5 = 1 << 38; h5 = 1 << 39
a4 = 1 << 24; b4 = 1 << 25; c4 = 1 << 26; d4 = 1 << 27; e4 = 1 << 28; f4 = 1 << 29; g4 = 1 << 30; h4 = 1 << 31
a3 = 1 << 16; b3 = 1 << 17; c3 = 1 << 18; d3 = 1 << 19; e3 = 1 << 20; f3 = 1 << 21; g3 = 1 << 22; h3 = 1 << 23
a2 = 1 <<  8; b2 = 1 <<  9; c2 = 1 << 10; d2 = 1 << 11; e2 = 1 << 12; f2 = 1 << 13; g2 = 1 << 14; h2 = 1 << 15
a1 = 1 <<  0; b1 = 1 <<  1; c1 = 1 <<  2; d1 = 1 <<  3; e1 = 1 <<  4; f1 = 1 <<  5; g1 = 1 <<  6; h1 = 1 <<  7

CN2BB = {
	"a8": a8, "b8": b8, "c8": c8, "d8": d8, "e8": e8, "f8": f8, "g8": g8, "h8": h8,
	"a7": a7, "b7": b7, "c7": c7, "d7": d7, "e7": e7, "f7": f7, "g7": g7, "h7": h7,
	"a6": a6, "b6": b6, "c6": c6, "d6": d6, "e6": e6, "f6": f6, "g6": g6, "h6": h6,
	"a5": a5, "b5": b5, "c5": c5, "d5": d5, "e5": e5, "f5": f5, "g5": g5, "h5": h5,
	"a4": a4, "b4": b4, "c4": c4, "d4": d4, "e4": e4, "f4": f4, "g4": g4, "h4": h4,
	"a3": a3, "b3": b3, "c3": c3, "d3": d3, "e3": e3, "f3": f3, "g3": g3, "h3": h3,
	"a2": a2, "b2": b2, "c2": c2, "d2": d2, "e2": e2, "f2": f2, "g2": g2, "h2": h2,
	"a1": a1, "b1": b1, "c1": c1, "d1": d1, "e1": e1, "f1": f1, "g1": g1, "h1": h1 
}
BB2CN = {v: k for k, v in CN2BB.items()}

# ........................................................................... Directions

# Rook
N  =  8
E  =  1
S  = -8
W  = -1
ROOK_DIRECTIONS = [N, E, S, W]

# Castling
E2 = 2
E3 = 3
W2 = -2
W3 = -3

# Knight
NNE = 17
ENE = 10
ESE = -6
SSE = -15
SSW = -17
WSW = -10
WNW = 6
NNW = 15
KNIGHT_DIRECTIONS = [NNE, ENE, ESE, SSE, SSW, WSW, WNW, NNW]

# Bishop
NE =  9
SE = -7
SW = -9
NW =  7
BISHOP_DIRECTIONS = [NE, SE, SW, NW]

# Pawn
N2 = 16
S2 = -16
W_PAWN_DIRECTIONS = [N, N2]
W_PAWN_ATTACKS = [NE, NW]
B_PAWN_DIRECTIONS = [S, S2]
B_PAWN_ATTACKS = [SE, SW]


# Queen & King
QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS
KING_DIRECTIONS = QUEEN_DIRECTIONS

# General
POSITIVE_DIRECTIONS = [WNW, NW, NNW, N, NNE, NE, ENE, E]
NEGATIVE_DIRECTIONS = [ESE, SE, SSE, S, SSW, SW, WSW, W]



# ........................................................................... Boards
EMPTY 			= 0b0000000000000000000000000000000000000000000000000000000000000000
START 			= 0b0000000000000000000000000000000000000000000000000000000000000001
END 				= 0b1000000000000000000000000000000000000000000000000000000000000000
FULL 				= 0b1111111111111111111111111111111111111111111111111111111111111111
ROOKSTART 	= 0b1000000100000000000000000000000000000000000000000000000010000001
INNER				= 0b0000000001111110011111100111111001111110011111100111111000000000

CASTLE_MOVES 	= 0b0100010000000000000000000000000000000000000000000000000001000100
W_ROOKSTART 	= 0b0000000000000000000000000000000000000000000000000000000010000001
W_KSC_CHECKS	= 0b0000000000000000000000000000000000000000000000000000000001110000
W_KSC_CLEAR		= 0b0000000000000000000000000000000000000000000000000000000001100000
W_QSC_CHECKS	= 0b0000000000000000000000000000000000000000000000000000000000011100
W_QSC_CLEAR		= 0b0000000000000000000000000000000000000000000000000000000000001110

B_ROOKSTART 	= 0b1000000100000000000000000000000000000000000000000000000000000000
B_KSC_CHECKS	= 0b0111000000000000000000000000000000000000000000000000000000000000
B_KSC_CLEAR		= 0b0110000000000000000000000000000000000000000000000000000000000000
B_QSC_CHECKS	= 0b0001110000000000000000000000000000000000000000000000000000000000
B_QSC_CLEAR		= 0b0000111000000000000000000000000000000000000000000000000000000000



def rank_bbs():
 	current_rank = 0b0000000000000000000000000000000000000000000000000000000011111111
 	ranks = {}
 	for rank in '12345678':
 		ranks[int(rank)] = current_rank
 		current_rank <<= 8
 	return ranks

def file_bbs():
	current_file = 0b0000000100000001000000010000000100000001000000010000000100000001
	files = {}
	for file in 'abcdefgh':
		files[file] = current_file
		current_file <<= 1
	return files

def position_bbs():
	current_position = 0b0000000000000000000000000000000000000000000000000000000000000001
	positions = {}
	for rank in '12345678':
		for file in 'abcdefgh':
			positions[file+rank] = current_position
			current_position <<= 1
	return positions


SQUARE = position_bbs()
FILE = file_bbs()
RANK = rank_bbs()



#--------------STILL NEED ATTACKS
# Shifts bb left or right, works if amount is negative
def shift(bb, amount):
	if amount > 0:
		return bb << amount
	else:
		return bb >> -amount

def iterate_pos(file, rank, direction):
	# Iterate through position in direction
	if direction == N:
		rank += 1
	elif direction == N2:
		rank += 2	
	elif direction == NNE:
		rank += 2
		file += 1
	elif direction == NE:
		rank += 1
		file += 1
	elif direction == ENE:
		rank += 1
		file += 2
	elif direction == E:
		file += 1
	elif direction == ESE:
		rank -= 1
		file += 2
	elif direction == SE:
		rank -= 1
		file += 1
	elif direction == SSE:
		rank -= 2
		file += 1
	elif direction == S:
		rank -= 1
	elif direction == S2:
		rank -= 2
	elif direction == SSW:
		rank -= 2
		file -= 1
	elif direction == SW:
		rank -= 1
		file -= 1
	elif direction == WSW:
		rank -= 1
		file -= 2
	elif direction == W:
		file -= 1
	elif direction == WNW:
		rank += 1
		file -= 2
	elif direction == NW:
		rank += 1
		file -= 1
	elif direction == NNW:
		rank += 2
		file -= 1
	
	return file, rank


def gen_slide(cn, direction):
	ray_bb = EMPTY
	test_bb = SQUARE[cn]
	
	file = ord(cn[0])
	rank = ord(cn[1])

	file, rank = iterate_pos(file, rank, direction)
	# While test_bb still on the board
	while (ord('a')<=file<=ord('h')) and (ord('1')<=rank<=ord('8')):
		# Add it to ray
		ray_bb |= test_bb
		# Shift in direction
		test_bb = shift(test_bb, direction)
		file, rank = iterate_pos(file, rank, direction)

	# Remove start point from ray
	ray_bb ^= test_bb
	return ray_bb

def gen_jump(cn, direction):
	
	jump_bb = shift(SQUARE[cn], direction)
	
	file = ord(cn[0])
	rank = ord(cn[1])

	file, rank = iterate_pos(file, rank, direction)

	# If test_bb still on the board
	if (ord('a')<=file<=ord('h')) and (ord('1')<=rank<=ord('8')):
		# Add it to ray
		return jump_bb
	else:
		return EMPTY

def ray_bbs():
	#Initialise empty dict
	all_rays = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			rays = {}
			# Start with empty bb
			bb = EMPTY
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in QUEEN_DIRECTIONS:
				# Create slide, remove starting square
				rays[direction] = gen_slide(cn, direction) ^ SQUARE[cn]
			all_rays[cn] = rays

	return all_rays
	

def w_pawn_jumps_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY
			# Create key
			cn = file + rank
			# Add single jump
			bb |= gen_jump(cn, N)
			# Add double jump on start row
			bb |= gen_jump(cn, N2) if rank == '2' else EMPTY
			# Remove starting square and append
			moves[cn] = bb ^ CN2BB[cn]
	return moves

def w_pawn_attacks_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in W_PAWN_ATTACKS:
				bb |= gen_jump(cn, direction)
			# Remove starting square and append
			moves[cn] = bb ^ CN2BB[cn]
	return moves

def b_pawn_jumps_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY
			# Create key
			cn = file + rank
			# Add single jump
			bb |= gen_jump(cn, S)
			# Add double jump on start row
			bb |= gen_jump(cn, S2) if rank == '7' else EMPTY
			# Remove starting square and append
			moves[cn] = bb ^ CN2BB[cn]
	return moves

def b_pawn_attacks_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in B_PAWN_ATTACKS:
				bb |= gen_jump(cn, direction)
			# Remove starting square and append
			moves[cn] = bb ^ CN2BB[cn]
	return moves

def rook_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in ROOK_DIRECTIONS:
				bb |= gen_slide(cn, direction)
			# Remove starting square and append
			moves[cn] = bb ^ CN2BB[cn]

	return moves

def knight_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in KNIGHT_DIRECTIONS:
				bb |= gen_jump(cn, direction)
			# Remove starting square and append
			moves[cn] = bb ^ CN2BB[cn]
	return moves

def bishop_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in BISHOP_DIRECTIONS:
				bb |= gen_slide(cn, direction)
			# Remove starting square and append
			moves[cn] = bb ^ CN2BB[cn]
	return moves

def queen_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in QUEEN_DIRECTIONS:
				bb |= gen_slide(cn, direction)
			# Remove starting square and append
			moves[cn] = bb ^ CN2BB[cn]
	return moves

def king_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in KING_DIRECTIONS:
				bb |= gen_jump(cn, direction)
			# Remove starting square and append
			moves[cn] = bb ^ CN2BB[cn]
	return moves

RAYS = ray_bbs()
W_PAWN_JUMPS = w_pawn_jumps_bbs()
W_PAWN_ATTACKS = w_pawn_attacks_bbs()
B_PAWN_JUMPS = b_pawn_jumps_bbs()
B_PAWN_ATTACKS = b_pawn_attacks_bbs()
ROOK_MOVES = rook_moves_bbs()
BISHOP_MOVES = bishop_moves_bbs()
KNIGHT_MOVES = knight_moves_bbs()
QUEEN_MOVES = queen_moves_bbs()
KING_MOVES = king_moves_bbs()



####################################################################################
# ................................................................................ #
# .................................. MAGIC NUMBERS ............................... #
# ................................................................................ #
####################################################################################

# .................................................................... Magic Numbers
ROOK_MAGICS = {
	'a8': 2308097008050839568,
	'b8': 4755801344479068288,
	'c8': 576478619376097312,
	'd8': 15762976653447680,
	'e8': 90072731290173440,
	'f8': 216172799698731010,
	'g8': 9516669048520184832,
	'h8': 2308094817652441122,
	'a7': 72058839646240867,
	'b7': 562949964955648,
	'c7': 9223372041690857474,
	'd7': 137439485957,
	'e7': 9007362480276992,
	'f7': 4611835861850403841,
	'g7': 360292643676131840,
	'h7': 9799832789242220545,
	'a6': 1130297957875972,
	'b6': 1156388015661777201,
	'c6': 2405752637488,
	'd6': 13836256557450660864,
	'e6': 648588751592752161,
	'f6': 9943952375314120832,
	'g6': 2018457083856551938,
	'h6': 2322445584433152,
	'a5': 2594117447585960547,
	'b5': 4611694816937377792,
	'c5': 5188146850187727240,
	'd5': 1152956689249468483,
	'e5': 289391804296728576,
	'f5': 1135245959102496,
	'g5': 4398583398402,
	'h5': 1157427376276129808,
	'a4': 86694498985459728,
	'b4': 4612811918602940433,
	'c4': 37013964808257536,
	'd4': 1153203050855284736,
	'e4': 22536707014393858,
	'f4': 6958342899264258256,
	'g4': 2251842897575936,
	'h4': 562968748105795,
	'a3': 864699924565459584,
	'b3': 590130980380147712,
	'c3': 6917529062101778436,
	'd3': 2396232348307816452,
	'e3': 3458765652154679296,
	'f3': 10133391219953680,
	'g3': 4611756456025264256,
	'h3': 1192328022972171408,
	'a2': 1155173613695975680,
	'b2': 9223513942591151112,
	'c2': 4612886859607965698,
	'd2': 5251072,
	'e2': 844424963706888,
	'f2': 9799832789158414600,
	'g2': 2341943026462695442,
	'h2': 4684378030683340800,
	'a1': 4674879625142599682,
	'b1': 288793600983068738,
	'c1': 2832498992283906,
	'd1': 562949955522561,
	'e1': 4405563359232,
	'f1': 140774129795076,
	'g1': 596731359477629972,
	'h1': 6768595862290432
}

BISHOP_MAGICS = {
	'a8': 145250025826418688,
	'b8': 288239176539703424,
	'c8': 1202532658992123905,
	'd8': 148618805151580196,
	'e8': 9223372191746394376,
	'f8': 2468007805975594016,
	'g8': 442483061436186624,
	'h8': 288265698030502146,
	'a7': 13835164729384894464,
	'b7': 612771574323347464,
	'c7': 73258260737609732,
	'd7': 137438954114,
	'e7': 36029976524359168,
	'f7': 4503600449454082,
	'g7': 9817847187669909520,
	'h7': 2251799915413504,
	'a6': 580964421732548736,
	'b6': 3378285448855552,
	'c6': 4620703113430959120,
	'd6': 9223372389042129536,
	'e6': 1143492092888064,
	'f6': 14124418729523544068,
	'g6': 72063091598166018,
	'h6': 1152939165512385568,
	'a5': 1161929253617467396,
	'b5': 72093877922168856,
	'c5': 1135246295961600,
	'd5': 1765433053020422162,
	'e5': 4622980206298157072,
	'f5': 4620763861438431241,
	'g5': 281476067237889,
	'h5': 162345146715734020,
	'a4': 9223372071215039488,
	'b4': 5810224336476316736,
	'c4': 288925267504677952,
	'd4': 9802122118396116994,
	'e4': 9223373274073792512,
	'f4': 824652599296,
	'g4': 6989608612180001028,
	'h4': 2815299556485136,
	'a3': 1152921676405551104,
	'b3': 5700040077084960,
	'c3': 144115224587272392,
	'd3': 108095329961771136,
	'e3': 23723063956736008,
	'f3': 290482193146314752,
	'g3': 2308167385930301968,
	'h3': 7730941166224,
	'a2': 79024116963819520,
	'b2': 108157034679238656,
	'c2': 2267786776576,
	'd2': 1152921658690535492,
	'e2': 1157425181545735433,
	'f2': 2216471625859,
	'g2': 4899952128711229505,
	'h2': 4661967956652064,
	'a1': 9226186829571556353,
	'b1': 217312159636428810,
	'c1': 5260240786099798016,
	'd1': 144155872164061472,
	'e1': 576531276471730432,
	'f1': 4665729216103579680,
	'g1': 9223373170759778320,
	'h1': 1170935903141627392
}


def masked_bishop_attacks():
	masked_attacks = {}
	for cn, bb in SQUARE.items():
		attacks  = EMPTY
		attacks |= RAYS[cn][NE] & ~(FILE['h'] | RANK[8])
		attacks |= RAYS[cn][SE] & ~(FILE['h'] | RANK[1])
		attacks |= RAYS[cn][SW] & ~(FILE['a'] | RANK[1])
		attacks |= RAYS[cn][NW] & ~(FILE['a'] | RANK[8])

		masked_attacks[cn] = attacks
	return masked_attacks


def masked_rook_attacks():
	masked_attacks = {}
	for cn, bb in SQUARE.items():
		attacks  = EMPTY
		attacks |= RAYS[cn][N] & ~RANK[8]	
		attacks |= RAYS[cn][E] & ~FILE['h']	
		attacks |= RAYS[cn][S] & ~RANK[1]		
		attacks |= RAYS[cn][W] & ~FILE['a']	

		masked_attacks[cn] = attacks

	return masked_attacks

def masked_queen_attacks():
	b = masked_bishop_attacks()
	r = masked_rook_attacks()
	q = {k: b[k]|r[k] for k,v in b.items()}
	return q

def init_slider_attack_tables(piece_type):
	# Initialise attack table
	attacks = {}
	# For each square on board
	for cn, bb in SQUARE.items():
		# Initialise that square's attack table
		attacks[cn] = {}

		# Initialise masks, magic numebrs, directions
		if piece_type == 'R':
			attack_mask 		= MASKED_ROOK_ATTACKS[cn]
			MAGICS 				= ROOK_MAGICS
			NUM_RELEVANT_BITS 	= NUM_RELEVANT_BITS_ROOK
			directions 			= ROOK_DIRECTIONS
		elif piece_type == 'B':
			attack_mask 		= MASKED_BISHOP_ATTACKS[cn]
			MAGICS 				= BISHOP_MAGICS
			NUM_RELEVANT_BITS 	= NUM_RELEVANT_BITS_BISHOP
			directions 			= BISHOP_DIRECTIONS

		relevant_bit_count = count_bits(attack_mask)

		occupancy_indicies = 1 << relevant_bit_count

		for index in range(occupancy_indicies):

			occupancy = set_occupancy(index, relevant_bit_count, attack_mask)
			magic_index = (occupancy * MAGICS[cn]) >> (64 - NUM_RELEVANT_BITS[cn])
			attacks[cn][magic_index] = gen_slide_attacks(cn, occupancy, directions)

	return attacks

def gen_slide_attacks(square, occupancy, directions):
	moves = EMPTY
	for direction in directions:
		# Set nearest piece to be non-existant
		nearest_piece 	= EMPTY
		shadow 			= EMPTY
		# Get bb of squares in direction of piece.position
		unblocked_ray 	= RAYS[square][direction]
		blocking_pieces = unblocked_ray & occupancy
		# If there is a piece in the way
		if blocking_pieces: 
			nearest_piece = BB2CN[find_nth_piece(blocking_pieces, direction)]
			shadow 		  = RAYS[nearest_piece][direction]
		# Remove squares behind blocking piece
		blocked_ray =  unblocked_ray ^ shadow
		# Add blocked ray to movable positions, including piece at end position
		moves |= blocked_ray

	return moves


# Set potential occupancies along attack mask
def set_occupancy(index, bit_count, attack_mask):
	occupancy = EMPTY

	for count in range(bit_count):
		square_index = find_LSB(attack_mask)
		attack_mask ^=  1 << square_index

		if index & (1 << count):
			occupancy |= 1 << square_index

	return occupancy\

def magic_rook_attacks(cn, occupancy):
	attacks    = ROOK_ATTACK_TABLE
	occupancy &= MASKED_ROOK_ATTACKS[cn]
	occupancy *= ROOK_MAGICS[cn]
	occupancy >>= 64 - NUM_RELEVANT_BITS_ROOK[cn]
	return attacks[cn][occupancy]

def magic_bishop_attacks(cn, occupancy):
	attacks    = BISHOP_ATTACK_TABLE
	occupancy &= MASKED_BISHOP_ATTACKS[cn]
	occupancy *= BISHOP_MAGICS[cn]
	occupancy >>= 64 - NUM_RELEVANT_BITS_BISHOP[cn]
	return attacks[cn][occupancy]

def magic_queen_attacks(cn, occupancy):
	return magic_rook_attacks(cn, occupancy) | magic_bishop_attacks(cn, occupancy)

MASKED_BISHOP_ATTACKS 		= masked_bishop_attacks()
MASKED_ROOK_ATTACKS 		= masked_rook_attacks()

NUM_RELEVANT_BITS_ROOK 		= {k: count_bits(MASKED_ROOK_ATTACKS[k]) for k, v in CN2BB.items()}
NUM_RELEVANT_BITS_BISHOP 	= {k: count_bits(MASKED_BISHOP_ATTACKS[k]) for k, v in CN2BB.items()}

ROOK_ATTACK_TABLE 			= init_slider_attack_tables('R')
BISHOP_ATTACK_TABLE 		= init_slider_attack_tables('B')
