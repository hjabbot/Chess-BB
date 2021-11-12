'''

Chess implemented with bitboards 
Second attempt

'''
#Test

import pygame as pg
from numpy import rot90
import copy

# Custom imports
from constants import *			# Global variables
from board_constants import *	# Global variables
import draw
from chess_pieces import *
import engine



'''
 Import image as pygame image object
-------------------------------------
'''
def import_image(name):
	filename = 'img/{}.png'.format(name)
	img = pg.image.load(filename).convert_alpha()
	img = pg.transform.smoothscale(img, (SQ_SIZE, SQ_SIZE))
	return img

# Generates pieces based on INITIAL_BOARD
def initialise_pieces():
	bb_location = START
	pieces = []

	board = rot90(INITIAL_BOARD, k=3)

	# For each square
	for row in range(len(board)):
		for col in range(len(board[row])):
			# Get piece on square
			square = board[col][row]
			position = Position(bb=bb_location)
			# If not empty
			if square != '--':
				# Add to piece list
				pieces.append(Piece(position, square))
			# Move to next square to test
			bb_location = shift(bb_location, 1)

	return pieces

if __name__ == '__main__':

	# Initialise Pygame
	pg.init()
	screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	clock = pg.time.Clock()

	images = {label: import_image(label) for label in PIECE_LABELS}

	# Initialise chess board
	pieces = initialise_pieces()		# Generate all pieces from initial board in constants
	gs = engine.GameState(pieces)
	gs.update()

	# Initialise variables
	score = 0
	move_piece = None
	move_from = None	# Will store positions that user wants to move piece from/to
	move_to = None
	selected_square = None
	selected_piece = None
	highlight_positions = EMPTY	# All positions highlighted by user
	highlight_moves = EMPTY		# Moves possible by selected piece
	previous_turns =[]

	game_on = True		# Flag to keep game running

	# While in game
	while game_on:
		# Read out events
		for event in pg.event.get():

			#Get current turn's side
			ally_side  = 'w' if gs.white_turn else 'b'
			enemy_side = 'b' if gs.white_turn else 'w'

			# User quits game
			if event.type == pg.QUIT:
				pg.quit()
				game_on = False
			# User clicks
			elif event.type == pg.MOUSEBUTTONDOWN:
				highlight_moves = EMPTY
				x,y = event.pos
				bb = xy2bb(x, y)
				selected_square = Position(bb)
				# .............................................................Left Mouse Button
				if event.button == 1:	# LMB
					# Retrieve ally piece at that square if it exists
					selected_piece = gs.pos2piece(selected_square)

					# If no previously selected piece and ally piece selected
					if not(move_from) and selected_piece in gs.ally_pieces:
						# Remember for movement next click
						move_piece = selected_piece
						move_from = selected_square
						# Get possible moves as bb
						highlight_moves = selected_piece.moves

					# If previously selected piece and not clicking same square 
					# and selected_square in selected_piece.moves
					elif move_from and move_from != selected_square and \
						 selected_square.bb & move_piece.moves:
						move_to = selected_square
						captured_piece = gs.pos2piece(selected_square)

					# If user didn't click on a valid square
					else:
						selected_piece = None
						move_piece = None
						move_from = False
					highlight_positions = EMPTY
				# ...........................................................Middle Mouse Button
				# elif event.button == 2:	# MMB
				# ............................................................Right Mouse Button
				elif event.button == 3:		#RMB
					# Set position to highlight
					# highlight_position = Position(bb=selected_square.bb)
					# XOR the list to select/deselect
					highlight_positions ^= selected_square.bb
			elif event.type == pg.KEYDOWN:
				# .......................................................................'u' key
				if event.key == pg.K_u and previous_turns:
					gs = previous_turns.pop(-1)


	    # Processing
	    # This section will be built out later
	    # If move made
		if move_to:
			# Append old gamestate
			previous_turns.append(copy.deepcopy(gs))
			# Perfom the move
			gs.perform_move(move_from, move_to)

			# Reset turn flags
			move_from = False
			move_to = False

			score = 0
			for piece in gs.active_pieces:
				if piece.side == 'w':
					score += piece.value
				else:
					score -= piece.value
	 
	    # Render elements of the game
		draw.board(screen)
		draw.score(screen, score)
		draw.sidebar(screen)
		draw.highlight(screen, highlight_positions)
		draw.moves(screen, highlight_moves)
		if selected_piece:
			draw.selection(screen, selected_piece.position.bb)
		# if gs.check:
		# 	draw.check(screen, gs.ally_king.position.bb)
		draw.pieces(screen, gs.active_pieces, images)



		pg.display.update()
		clock.tick(FPS)