from constants import *

# ................................................................................................GameState
'''
Game State object
'''
class GameState:
	def __init__(self, pieces, white_turn=True):


		ally_positions  = EMPTY
		enemy_positions = EMPTY
		# On initialise, find where every piece is on the board
		for piece in pieces:
			ally_positions  |= piece.position.bb if piece.side == 'w' else EMPTY
			enemy_positions |= piece.position.bb if piece.side == 'b' else EMPTY

		# Update pieces with board
		for piece in pieces:
			if piece.side == 'w': piece.update(ally_positions, enemy_positions, enpassant=EMPTY, castle=CASTLE_MOVES)
			if piece.side == 'b': piece.update(enemy_positions, ally_positions, enpassant=EMPTY, castle=CASTLE_MOVES)

		self.pieces 	= pieces
		self.move_list 	= []

		self.white_turn 	 = white_turn
		self.enpassantable 	 = EMPTY
		self.castle_moves	 = CASTLE_MOVES

		self.active_pieces 	 = self.pieces
		self.captured_pieces = []
		self.ally_pieces 	 = [p for p in self.pieces if p.side == 'w']
		self.ally_king	 	 = [p for p in self.ally_pieces if p.type == 'K'][0]
		self.ally_positions  = bblist2bb([p.position for p in self.ally_pieces])
		self.ally_attacks 	 = bblist2bb([p.attacks for p in self.ally_pieces])
		self.ally_defends	 = bblist2bb([p.defends for p in self.ally_pieces])
		
		self.enemy_pieces 	 = [p for p in self.pieces if p.side == 'b']
		self.enemy_king	 	 = [p for p in self.enemy_pieces if p.type == 'K'][0]
		self.enemy_positions = bblist2bb([p.position for p in self.enemy_pieces])
		self.enemy_attacks 	 = bblist2bb([p.attacks  for p in self.enemy_pieces])
		self.enemy_defends	 = bblist2bb([p.defends  for p in self.enemy_pieces])	
		
		# Get all ally rooks and OR their bitboards to form mask
		rook_positions		 = bblist2bb([p.position.bb for p in self.pieces if p.type == 'R'])
		# If corner square not occupied by rook positions, remove that side of castle move
		if not(rook_positions & a1): 	self.castle_moves &= (FULL ^ c1)
		if not(rook_positions & h1): 	self.castle_moves &= (FULL ^ g1)
		if not(rook_positions & a8): 	self.castle_moves &= (FULL ^ c8)
		if not(rook_positions & h8): 	self.castle_moves &= (FULL ^ g8)

	'''
	Recalculates the ally/enemy pieces and their possible moves
	-----------------------------------------------------------
	active_pieces 	[Piece]
	captured_pieces [Piece]
	ally_pieces		[int]
	ally_king		Piece
	ally_attacks	int (bb)
	ally_defends	int (bb)
	enemy_pieces	[int]
	enemy_king		Piece
	enemy_attacks	int (bb)
	enemy_defends	int (bb)
	'''
	def update(self):
		# Recalculate what is and isn't captured
		self.active_pieces 	 = [p for p in self.pieces if not(p.captured)]
		self.captured_pieces = [p for p in self.pieces if p.captured]

		# Set ally and enemy pieces in gamestate
		if self.white_turn:
			self.ally_pieces 	 = [p for p in self.active_pieces if p.side == 'w']
			self.ally_king	 	 = [p for p in self.ally_pieces if p.type == 'K'][0]
			
			self.enemy_pieces 	 = [p for p in self.active_pieces if p.side == 'b']
			self.enemy_king	 	 = [p for p in self.enemy_pieces if p.type == 'K'][0]
		else:
			self.ally_pieces 	 = [p for p in self.active_pieces if p.side == 'b']
			self.ally_king	 	 = [p for p in self.ally_pieces if p.type == 'K'][0]
			
			self.enemy_pieces 	 = [p for p in self.active_pieces if p.side == 'w']
			self.enemy_king	 	 = [p for p in self.enemy_pieces if p.type == 'K'][0]

		# Set ally and enemy positions in gamestate
		self.ally_positions  = bblist2bb([p.position for p in self.ally_pieces])
		self.enemy_positions = bblist2bb([p.position for p in self.enemy_pieces])

		# Update pieces with board
		for piece in self.pieces:
			if piece.type == 'p':
				if self.white_turn:
					if piece.side == 'w': piece.update(self.ally_positions, self.enemy_positions, enpassant=self.enpassantable)
					else 				: piece.update(self.enemy_positions, self.ally_positions, enpassant=self.enpassantable)
				else:
					if piece.side == 'b': piece.update(self.ally_positions, self.enemy_positions, enpassant=self.enpassantable)
					else 				: piece.update(self.enemy_positions, self.ally_positions, enpassant=self.enpassantable)

			# King special case, its moves depend on where other attacks are
			elif piece.type != 'K':
				if self.white_turn:
					if piece.side == 'w': piece.update(self.ally_positions, self.enemy_positions)
					else 				: piece.update(self.enemy_positions, self.ally_positions)
				else:
					if piece.side == 'b': piece.update(self.ally_positions, self.enemy_positions)
					else 				: piece.update(self.enemy_positions, self.ally_positions)



		# With updated positions, set attacks/defences in gamestate
		self.ally_moves      = bblist2bb([p.moves    for p in self.ally_pieces])
		self.ally_attacks 	 = bblist2bb([p.attacks  for p in self.ally_pieces])
		self.ally_defends	 = bblist2bb([p.defends  for p in self.ally_pieces])
		self.enemy_moves     = bblist2bb([p.moves    for p in self.enemy_pieces])
		self.enemy_attacks 	 = bblist2bb([p.attacks  for p in self.enemy_pieces])
		self.enemy_defends	 = bblist2bb([p.defends  for p in self.enemy_pieces])	



		# Fix pawn attacks to include empty squares, not just enemy squares
		ally_attack_dict 	 = W_PAWN_ATTACKS if self.white_turn else B_PAWN_ATTACKS
		enemy_attack_dict 	 = B_PAWN_ATTACKS if self.white_turn else W_PAWN_ATTACKS



		# Define attacked and defended squares. 
		# An attacked square is a square that the enemy can move to, or is defending
		# A  defended square is a square that the ally  can move to, or is defending
		squares_defended 	 = EMPTY
		squares_attacked 	 = EMPTY

		for piece in self.ally_pieces:
			if piece.type == 'p': squares_defended |= ally_attack_dict[piece.position.cn]
			else 				: squares_defended |= piece.moves | piece.defends
		for piece in self.enemy_pieces:
			if piece.type == 'p': squares_attacked |= enemy_attack_dict[piece.position.cn]
			else 				: squares_attacked |= piece.moves | piece.defends


		# self.ally_pawns  	 = [p for p in self.ally_pieces  if p.type == 'p']
		# self.enemy_pawns 	 = [p for p in self.enemy_pieces if p.type == 'p']
		# ally_pawn_attacks 	 = bblist2bb([ally_attack_dict[p.position.cn]  for p in self.enemy_pawns])
		# enemy_pawn_attacks 	 = bblist2bb([enemy_attack_dict[p.position.cn] for p in self.enemy_pawns])
		bbprint(squares_attacked)
		# self.enemy_attacks = squares_attacked
		# self.ally_attacks = squares_defended
		# self.ally_attacks 	|= ally_pawn_attacks
		# self.enemy_attacks 	|= enemy_pawn_attacks

		# Get all ally rooks and OR their bitboards to form mask
		rook_positions		 = bblist2bb([p.position.bb for p in self.pieces if p.type == 'R'])
		# If corner square not occupied by rook positions, remove that side of castle move
		if not(rook_positions & a1): 	self.castle_moves &= (FULL ^ c1)
		if not(rook_positions & h1): 	self.castle_moves &= (FULL ^ g1)
		if not(rook_positions & a8): 	self.castle_moves &= (FULL ^ c8)
		if not(rook_positions & h8): 	self.castle_moves &= (FULL ^ g8)


		

		# Update king last because it requires enemy attacks to avoid check
		self.enemy_king.update(self.enemy_positions, self.ally_positions, 
							   attacked_squares=squares_defended, defended_squares=squares_attacked,
							   castle=self.castle_moves)
		self.enemy_attacks 	|= self.enemy_king.attacks
		self.enemy_defends  |= self.enemy_king.defends
		
		self.ally_king.update(self.ally_positions, self.enemy_positions, 
							   attacked_squares=squares_attacked, defended_squares=squares_defended,
							   castle=self.castle_moves)

		self.ally_attacks 	|= self.ally_king.attacks
		self.ally_defends   |= self.ally_king.defends


	@property
	def check(self):
		return True if self.ally_king.position.bb & self.enemy_attacks else False
	@property
	def mate(self):
		return True if (self.ally_king.position.bb & self.enemy_attacks) and (self.ally_king.moves != 0) else False

	def pos2piece(self, position):
		# Iterate through all pieces to find one that matches position
		for piece in self.pieces:
			if piece.position == position:
				return piece
		# If none match, then return nothing
		else:
			return None

	def perform_move(self, start, end):
		# Determine basics about move
		moving_piece = self.pos2piece(start)
		captured_piece = self.pos2piece(end)

		castling = False
		pawn_promotion = False
		performing_enpassant = False
		enpassantable = EMPTY


		# Process special cases
		# If king
		if moving_piece.type == 'K':
			# If castling as a move (If king moves 2 squares)
			if (shift(start.bb, E2) == end or shift(start.bb, W2) == end): 	
				castling = True

				# Move rook if castled
				if end.bb & c1:
					castling_rook 				= self.pos2piece(a1)
					assert(castling_rook.type == 'R')
					castling_rook.position.bb 	= d1
				elif end.bb & c8:
					castling_rook 				= self.pos2piece(a8)
					assert(castling_rook.type == 'R')
					castling_rook.position.bb 	= d8
				elif end.bb & g1:
					castling_rook 				= self.pos2piece(h1)
					assert(castling_rook.type == 'R')
					castling_rook.position.bb 	= f1
				elif end.bb & g8:
					castling_rook 				= self.pos2piece(h8)
					assert(castling_rook.type == 'R')
					castling_rook.position.bb 	= f8 



			# Remove white start rank if white king moves. Does this by only 'and'ing black start rank
			# Same for black
			if moving_piece.side == 'w': 	self.castle_moves &= RANK[8] 
			else 					   : 	self.castle_moves &= RANK[1] 

		# If pawn
		if moving_piece.type == 'p':
			# If pawn promotion (If pawn moving to one of end ranks)
			if end.bb & (RANK[1] & RANK[8]):
				pawn_promotion = True

			# If performing en passant
			if moving_piece.attacks & self.enpassantable & end.bb:
				performing_enpassant = True
				# Get position of square behind end capture to set captured_piece

				captured_position = shift(end.bb, S) if self.white_turn else shift(end.bb, N)
				captured_piece = self.pos2piece(captured_position)


			# If double jump, allow enpassant
			if start.bb & RANK[2] and end.bb & RANK[4]:
				enpassantable = shift(start.bb, N)
			elif start.bb & RANK[7] and end.bb & RANK[5]:
				enpassantable = shift(start.bb, S)

			self.enpassantable = enpassantable

		# Generate a move object
		move = Move(start, end, 
					moving_piece=moving_piece, captured_piece=captured_piece, 
					check=self.check, mate=self.mate,
					castle=castling, enpassant=performing_enpassant, pawn_promotion=pawn_promotion)
 
		# Add to list of moves made
		self.move_list.append(move)

		# Place piece in end position
		moving_piece.position = end
		# Remove captured piece if there is one
		if captured_piece: captured_piece.captured = True

		# Finally, update to next game state
		self.white_turn = not(self.white_turn)
		self.update()

# ................................................................................................Moves


def line_of_attack(position, gs, direction):
	# Create the ray as per empty board
	ray_bb = RAYS[position.cn][direction]
	# Get location of all pieces on board
	occupancy = gs.active_bb
	# Find overlap
	overlap = ray_bb & occupancy
	# If there's any overlap
	if overlap:
		# Find the first square in array that's occupied
		if direction > 0:
			blocking_piece = START << (find_LS1B(overlap))
		else:
			blocking_piece = START << (find_MS1B(overlap))
		blocking_piece_cn = bb2cn(blocking_piece)
		# XOR these rays to get blocked ray
		ray_bb ^= RAYS[blocking_piece_cn][direction]

	return ray_bb

def limit_absolute_pins(position, gs):
	xray_bb = FULL
	# For each xray on king
	for xray in gs.xrays_on_king:
		# If this piece is the xrayed piece
		if position.bb & xray:
			# Limit to moving along xray axis
			xray_bb &= xray
	return xray_bb

def limit_check_escapes(position, gs):
	defend_bb = FULL
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
Move Object
-------------------------------
		   (int) start :
		   (int)   end :

(Piece)   moving_piece :
(Piece) captured_piece :
'''
class Move:
	def __init__(self, start, end, 
					   moving_piece=None, 	captured_piece=None,
					   check=False,           mate=False, 
					   castle=False, enpassant=False, pawn_promotion=None):
		# Positions of move
		self.start = start
		self.end = end
		
		# Pieces involved in move
		self.moving_piece = moving_piece
		self.captured_piece = captured_piece

		# Flags for move special cases
		self.castle = castle
		self.check = check
		self.enpassant = enpassant

	def __str__(self):
		# Castling has unique notation
		if castle:
			if start > end:
				return '  O-O-O'
			else:
				return '    O-O'

		# String to print out in chess notation
		pgn = ''

		# If not a pawn, add label
		if self.moving_piece.type == 'p':
			pgn += ' '
		else:
			pgn += self.moving_piece.type

		# Add starting square
		pgn += self.start.cn

		# If piece is captured, denote it
		if self.captured_piece:
			pgn += 'x'
		else:
			pgn += '-'

		# Add landing square
		pgn += self.end.cn

		# Add check if relevant
		if self.mate:
			pgn += '# '
		elif self.check:
			pgn += '+ '
		elif pawn_promotion:
			pgn += '={p}'.format(p = pawn_promotion)
		else:
			pgn += '  '


		return pgn