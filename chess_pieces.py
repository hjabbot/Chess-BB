
from constants import *
from board_constants import *
from numpy import log2


# ................................................................................................Piece

'''
Piece object
-----------------------------------
(Position) position	: 
	 (str) label 	:
	 (str) side 	: 
	 (str) type 	: 
	 [int] attacks 	: 
	 [int] defends 	:
	  
	 [int] moves	:
'''
class Piece:
	def __init__(self, position, label, captured=False):

		self.position 	= position 	# Place on board as bitboard
		self.label		= label 	# e.g. 'wK'
		self.side 		= label[0]	# 'w' or 'b'
		self.type 		= label[1]	# 'p', 'R', 'N', 'B', 'Q', or 'K'
		self.captured 	= captured

		self.moves 		= EMPTY	# All possible moves, same as self.attacks but includes pawn jumps
		self.xrays 		= EMPTY	# All posible moves like above but ignoring first enemy piece along LOS
		self.attacks 	= EMPTY	# All squares this piece is currently attacking (excludes ally squares)
		self.defends 	= EMPTY	# All the squares this piece is defending (includes ally squares)

		# Assigning the move generating function
		if   self.type == 'p': self.value = PAWN_VALUE
		elif self.type == 'R': self.value = ROOK_VALUES
		elif self.type == 'N': self.value = KNIGHT_VALUE
		elif self.type == 'B': self.value = BISHOP_VALUE
		elif self.type == 'Q': self.value = QUEEN_VALUE
		else 				 : self.value = KING_VALUE


	def update(self, ally_positions, 	     enemy_positions, enemy_king=None,
				     attacked_squares=EMPTY, defended_squares=EMPTY,
				     enpassant=EMPTY, 	     castle=EMPTY):
		# No moves possible if captured
		if self.captured:
			self.moves = EMPTY
			self.attacks = EMPTY
			self.defends = EMPTY
		else:

			# Generate bb for all moves, attacks and defenses possible by piece
			if self.type == 'p':
				self.moves, self.attacks, self.defends = self.pawn_moves(ally_positions, enemy_positions, 
																		 enpassant=enpassant)
			elif self.type == 'R':
				self.moves, self.attacks, self.defends = self.rook_moves(ally_positions, enemy_positions)
			elif self.type == 'N':
				self.moves, self.attacks, self.defends = self.knight_moves(ally_positions, enemy_positions)
			elif self.type == 'B':
				self.moves, self.attacks, self.defends = self.bishop_moves(ally_positions, enemy_positions)
			elif self.type == 'Q':
				self.moves, self.attacks, self.defends = self.queen_moves(ally_positions, enemy_positions)
			else:	# self.type == 'K'
				self.moves, self.attacks, self.defends = self.king_moves(ally_positions, enemy_positions, 
				    										attacked_squares=attacked_squares, 
				    										defended_squares=defended_squares, 
															castle=castle)

	def gen_xrays(self, ally_positions, enemy_positions, target=None, magic_attacks = None):
		
		if target:
			pass
		return EMPTY

	def pawn_jumps(self, ally_positions, enemy_positions):
		# Look up single jumps
		moves = W_PAWN_JUMPS[self.position.cn] if self.side == 'w' else B_PAWN_JUMPS[self.position.cn]

		taken_positions = ally_positions | enemy_positions
		# Remove double jump if blocked
		if   self.side == 'w' and (self.position.bb & RANK[2]) and (enemy_positions & RANK[3]): 
			moves &= ~RANK[4]
		elif self.side == 'b' and (self.position.bb & RANK[7]) and (enemy_positions & RANK[6]):
			moves &= ~RANK[5]
		# Remove taken positions
		moves &= ~taken_positions

		return moves


	def pawn_attacks(self, ally_positions, enemy_positions, enpassant):
		# Look up attackable positions
		moves = W_PAWN_ATTACKS[self.position.cn] if self.side == 'w' else B_PAWN_ATTACKS[self.position.cn]
		# Only accept enemy positions and enpassant positions
		moves &= (enemy_positions | enpassant)
		return moves

	def pawn_moves(self, ally_positions, enemy_positions, enpassant=EMPTY):
		# Look up movable positions
		moves   = self.pawn_jumps(ally_positions, enemy_positions) | self.pawn_attacks(ally_positions, enemy_positions, enpassant)  & (FULL^self.position.bb)
		attacks = self.pawn_attacks(ally_positions, enemy_positions, enpassant) & (enemy_positions | enpassant) & (FULL^self.position.bb)
		defends = self.pawn_attacks(ally_positions, enemy_positions, enpassant) & ally_positions & (FULL^self.position.bb)
			
		return moves, attacks, defends

	def rook_moves(self, ally_positions, enemy_positions):
		# Look up attackable positions
		possible_moves  = magic_rook_attacks(self.position.cn, ally_positions | enemy_positions)
		# Remove self
		possible_moves &= FULL ^ self.position.bb

		### TO DO: PINNING

		moves   = possible_moves & ~ally_positions # All possible moves
		attacks	= possible_moves & enemy_positions # Excludes empty squares
		defends	= possible_moves & ally_positions  # Excludes empty squares

		return moves, attacks, defends

	def knight_moves(self, ally_positions, enemy_positions):
		# Look up attackable positions
		possible_moves  =  KNIGHT_MOVES[self.position.cn]
		# Remove self
		possible_moves &= FULL ^ self.position.bb

		moves   = possible_moves & ~ally_positions # All possible moves
		attacks	= possible_moves & enemy_positions # Excludes empty squares
		defends	= possible_moves & ally_positions  # Excludes empty squares
		
		return moves, attacks, defends

	def bishop_moves(self, ally_positions, enemy_positions):
		# Look up attackable positions
		possible_moves  = magic_bishop_attacks(self.position.cn, ally_positions | enemy_positions)
		# Remove self
		possible_moves &= FULL ^ self.position.bb

		### TO DO: PINNING

		moves   = possible_moves & ~ally_positions # All possible moves
		attacks	= possible_moves & enemy_positions # Excludes empty squares
		defends	= possible_moves & ally_positions  # Excludes empty squares

		return moves, attacks, defends

	def queen_moves(self, ally_positions, enemy_positions):
		# Look up attackable positions
		possible_moves  = magic_queen_attacks(self.position.cn, ally_positions | enemy_positions)
		# Remove self
		possible_moves &= FULL ^ self.position.bb

		### TO DO: PINNING

		moves   = possible_moves & ~ally_positions # All possible moves
		attacks	= possible_moves & enemy_positions # Excludes empty squares
		defends	= possible_moves & ally_positions  # Excludes empty squares

		return moves, attacks, defends

	def king_moves(self, ally_positions,     enemy_positions,
				 		 attacked_squares=EMPTY,
				 		 defended_squares=EMPTY,
				 		 castle=EMPTY):

		# Look up attackable positions
		possible_moves = KING_MOVES[self.position.cn] 

		# Remove positions in check
		possible_moves &= ~(attacked_squares)
		# print("<HEYO><HEYO><HEYO><HEYO><HEYO><HEYO><HEYO><HEYO>")
		# print("enemy of {}".format(self.label))
		# bbprint(enemy_attacks | enemy_defends)


		# If castling is available to either side
		if castle:
			# Combine piece positions
			all_positions    = ally_positions | enemy_positions

			# Add castling possible_moves
			possible_moves |= (castle & RANK[1]) if self.side == 'w' else (castle & RANK[8]) 

			# Determine if it's white's turn or not
			if self.side == 'w' and (self.position.bb & ally_positions) or\
			   self.side == 'b' and (self.position.bb & enemy_positions): 
			     white_turn = True 
			else:
				white_turn = False 

			# Remove castling options if blocked or check'ed
			# If looking at ally king
			if (self.position.bb & ally_positions):
				if white_turn:
					if (attacked_squares & W_QSC_CHECKS) or (all_positions & W_QSC_CLEAR): possible_moves &= FULL^c1
					if (attacked_squares & W_KSC_CHECKS) or (all_positions & W_KSC_CLEAR): possible_moves &= FULL^g1
				else:
					if (attacked_squares & B_QSC_CHECKS) or (all_positions & B_QSC_CLEAR): possible_moves &= FULL^c8
					if (attacked_squares & B_KSC_CHECKS) or (all_positions & B_KSC_CLEAR): possible_moves &= FULL^g8	
			else:
				if white_turn:
					if (defended_squares & B_QSC_CHECKS) or (all_positions & B_QSC_CLEAR): possible_moves &= FULL^c1
					if (defended_squares & B_KSC_CHECKS) or (all_positions & B_KSC_CLEAR): possible_moves &= FULL^g1
				else:
					if (defended_squares & W_QSC_CHECKS) or (all_positions & W_QSC_CLEAR): possible_moves &= FULL^c8
					if (defended_squares & W_KSC_CHECKS) or (all_positions & W_KSC_CLEAR): possible_moves &= FULL^g8				


		moves   = possible_moves & ~ally_positions # All possible moves
		attacks	= possible_moves & enemy_positions # Excludes empty squares
		defends	= possible_moves & ally_positions  # Excludes empty squares


		return moves, attacks, defends



# .............................................................................................Position
'''
Position object
-----------------------------------
(Position) position	: 
		   (int) bb	: Bitboard representation of position
		   			  Only takes in a value that's a power of 2

		   (int)  x	: x coord of square
		   (int)  y	: y coord of square
		 (str) file : column of square
		 (str) rank : row of square
		   (str) cn : chess notation of square
'''
class Position:	
	
	def __init__(self, bb):
		assert (bb & (bb-1) == 0) and bb != 0, "Error: Bitboard is not a position! (i.e. not a power of 2)"
		self.bb = bb

	def __eq__(self, other):
		# Return true if 'other' is a position object, with same bitboard
		if isinstance(other, Position):
			return (self.bb == other.bb)
		# Return true if 'other' is bitboard equivalent to position bitboard
		elif isinstance(other, int):
			return (self.bb == other)
		# Otherwise '==' doesn't exist
		else:
			raise TypeError("Comparing Position to {}".format())

	def __repr__(self):
		return BB2CN[self.bb]

	# Overriding int values as bb is an int
	def __int__(self):
		return self.bb
	def __index__(self):
		return self.bb


	@property
	def file(self):
		return chr(ord('a') + self.x)
	@property
	def rank(self):
		return int(chr(ord('1') + self.y))
	@property
	def cn(self):
		return self.file + str(self.rank)

	@property
	def x(self):
		return int(log2(self.bb & -self.bb)) % 8
	@property
	def y(self):
		return int(log2(self.bb & -self.bb)) // 8
	@property
	def pix_x(self):
		return self.x * SQ_SIZE
	@property
	def pix_y(self):
		return (7-self.y) * SQ_SIZE





