# ...................................................................... Game Set-up

BACKGROUND = (0,0,0)
FPS = 60

# Initial board layout in human readable format. 
# Will be converted to bitboard before using

# INITIAL_BOARD = [
# 			['bR','bN','bB','bQ','bK','bB','bN','bR'],
# 			['bp','bp','bp','bp','bp','bp','bp','bp'],
# 			['--','--','--','--','--','--','--','--'],
# 			['--','--','--','--','--','--','--','--'],
# 			['--','--','--','--','--','--','--','--'],
# 			['--','--','--','--','--','--','--','--'],
# 			['wp','wp','wp','wp','wp','wp','wp','wp'],
# 			['wR','wN','wB','wQ','wK','wB','wN','wR']
# 			]

# INITIAL_BOARD = [
# 			['bR','--','--','--','--','--','--','bK'],
# 			['--','--','bN','--','--','--','bp','--'],
# 			['--','--','--','--','--','--','--','--'],
# 			['--','bQ','--','bB','--','--','--','--'],
# 			['--','--','--','--','wB','--','--','--'],
# 			['--','--','--','--','--','wN','wQ','--'],
# 			['--','wp','--','--','--','--','--','--'],
# 			['--','--','--','--','wK','--','--','wR']
# 			]

INITIAL_BOARD = [
			['--','--','--','--','bK','--','--','--'],
			['--','bp','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','bR','--','--','--'],
			['--','--','--','--','bN','--','--','--'],
			['wp','--','--','--','--','--','--','--'],
			['--','--','--','--','wK','--','--','--']
			]


PIECE_LABELS = ['wp','wR','wN','wB','wQ','wK',
				'bp','bR','bN','bB','bQ','bK'
				]


# .................................................................. Size parameters
BOARD_WIDTH 	= 1024
BOARD_HEIGHT 	= 1024

SQ_SIZE 		= BOARD_WIDTH // 8
IMAGE_SIZE		= BOARD_WIDTH // 8
CAPTURED_SIZE	= BOARD_WIDTH // 16

SCOREBAR_WIDTH	= 30
SCOREBAR_HEIGHT	= BOARD_HEIGHT
SCOREBAR_BORDER = 3

SIDEBAR_WIDTH 	= 250
SIDEBAR_HEIGHT 	= BOARD_HEIGHT


WINDOW_HEIGHT 	= BOARD_HEIGHT
WINDOW_WIDTH 	= BOARD_WIDTH + SCOREBAR_WIDTH + SIDEBAR_WIDTH


# .......................................................................... Colours
BLACK 	= 'grey30'
WHITE	= 'gray97'

SCOREBAR_BORDER_COLOUR	= 'black'

SIDEBAR_BACKGROUND_COLOUR = 'wheat'

DARK_SQUARE_COLOUR	= 'darkolivegreen4'
LIGHT_SQUARE_COLOUR	= 'beige'

SELECTION_COLOUR 			= 'deepskyblue'
SELECTION_BORDER_THICKNESS 	= SQ_SIZE // 10
SELECTION_ALPHA  			= 150 	# 0-255

HIGHLIGHT_COLOUR 	= 'gold'
HIGHLIGHT_ALPHA  	= 150	# 0-255

CHECK_COLOUR		= 'firebrick'

MOVES_COLOUR 		= 'deepskyblue'
MOVES_ALPHA 		= 150


# ............................................................................ Fonts
MOVES_FONT = 'Courier'
ENDGAME_FONT = 'Courier'











# ........................................................................ Bitboards
EMPTY_BB 		= 0b0000000000000000000000000000000000000000000000000000000000000000
START_BB 		= 0b0000000000000000000000000000000000000000000000000000000000000001
END_BB 			= 0b1000000000000000000000000000000000000000000000000000000000000000
FULL_BB 		= 0b1111111111111111111111111111111111111111111111111111111111111111
ROOKSTART_BB 	= 0b1000000100000000000000000000000000000000000000000000000010000001

W_ROOKSTART_BB 	= 0b0000000000000000000000000000000000000000000000000000000010000001
W_KSC_CHECKS_BB	= 0b0000000000000000000000000000000000000000000000000000000001110000
W_KSC_CLEAR_BB	= 0b0000000000000000000000000000000000000000000000000000000001100000
W_QSC_CHECKS_BB	= 0b0000000000000000000000000000000000000000000000000000000000011100
W_QSC_CLEAR_BB	= 0b0000000000000000000000000000000000000000000000000000000000001110

B_ROOKSTART_BB 	= 0b1000000100000000000000000000000000000000000000000000000000000000
B_KSC_CHECKS_BB	= 0b0111000000000000000000000000000000000000000000000000000000000000
B_KSC_CLEAR_BB	= 0b0110000000000000000000000000000000000000000000000000000000000000
B_QSC_CHECKS_BB	= 0b0001110000000000000000000000000000000000000000000000000000000000
B_QSC_CLEAR_BB	= 0b0000111000000000000000000000000000000000000000000000000000000000



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


'''
Generates a dictionary of all possible moves from each square on an empty board by piece

'''
# Directions
# Rook
N  =  8
E  =  1
S  = -8
W  = -1
ROOK_DIRECTIONS = [N, E, S, W]


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

# Castling
E2 = 2
E3 = 3
W2 = -2


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
	ray_bb = EMPTY_BB
	test_bb = SQUARE_BB[cn]
	
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
	
	jump_bb = shift(SQUARE_BB[cn], direction)
	
	file = ord(cn[0])
	rank = ord(cn[1])

	file, rank = iterate_pos(file, rank, direction)

	# If test_bb still on the board
	if (ord('a')<=file<=ord('h')) and (ord('1')<=rank<=ord('8')):
		# Add it to ray
		return jump_bb
	else:
		return EMPTY_BB


def ray_bbs():
	#Initialise empty dict
	all_rays = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			rays = {}
			# Start with empty bb
			bb = EMPTY_BB
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in QUEEN_DIRECTIONS:
				# Create slide, remove starting square
				rays[direction] = gen_slide(cn, direction) ^ SQUARE_BB[cn]
			all_rays[cn] = rays


	return all_rays


def w_pawn_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY_BB
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in W_PAWN_DIRECTIONS:
				bb |= gen_jump(cn, direction)

			moves[cn] = bb
	return moves

def w_pawn_attacks_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY_BB
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in W_PAWN_ATTACKS:
				bb |= gen_jump(cn, direction)

			moves[cn] = bb
	return moves

def b_pawn_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY_BB
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in B_PAWN_DIRECTIONS:
				bb |= gen_jump(cn, direction)

			moves[cn] = bb
	return moves

def b_pawn_attacks_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY_BB
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in B_PAWN_ATTACKS:
				bb |= gen_jump(cn, direction)

			moves[cn] = bb
	return moves


def rook_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY_BB
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in ROOK_DIRECTIONS:
				bb |= gen_slide(cn, direction)

			moves[cn] = bb


	return moves

def knight_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY_BB
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in KNIGHT_DIRECTIONS:
				bb |= gen_jump(cn, direction)

			moves[cn] = bb
	return moves


def bishop_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY_BB
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in BISHOP_DIRECTIONS:
				bb |= gen_slide(cn, direction)

			moves[cn] = bb
	return moves

def queen_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY_BB
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in QUEEN_DIRECTIONS:
				bb |= gen_slide(cn, direction)

			moves[cn] = bb
	return moves

def king_moves_bbs():
	#Initialise empty dict
	moves = {}
	# For each square
	for file in 'abcdefgh':
		for rank in '12345678':
			# Start with empty bb
			bb = EMPTY_BB
			# Create key
			cn = file + rank
			# For for each possible move, add to bb
			for direction in KING_DIRECTIONS:
				bb |= gen_jump(cn, direction)

			moves[cn] = bb
	return moves



SQUARE_BB = position_bbs()
FILE_BB = file_bbs()
RANK_BB = rank_bbs()
RAY_BBS = ray_bbs()

W_PAWN_MOVES_BB = w_pawn_moves_bbs()
W_PAWN_ATTACKS_BB = w_pawn_attacks_bbs()
B_PAWN_MOVES_BB = b_pawn_moves_bbs()
B_PAWN_ATTACKS_BB = b_pawn_attacks_bbs()
ROOK_MOVES_BB = rook_moves_bbs()
BISHOP_MOVES_BB = bishop_moves_bbs()
KNIGHT_MOVES_BB = knight_moves_bbs()
QUEEN_MOVES_BB = queen_moves_bbs()
KING_MOVES_BB = king_moves_bbs()



