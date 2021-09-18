'''

Chess implemented with bitboards 
Second attempt

'''
#Test

import pygame as pg
import copy

# Custom imports
from constants import *		# Global variables
from helper import *		# Global variables
import draw
import chess_pieces as cp
import engine



if __name__ == '__main__':

	# Initialise Pygame
	pg.init()
	screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	clock = pg.time.Clock()

	images = {label: import_image(label) for label in PIECE_LABELS}

	# Initialise chess board
	pieces = cp.initialise_pieces()		# Generate all pieces from initial board in constants
	gs = engine.Gamestate(pieces)


	# Initialise variables
	score = 0
	move_piece = None
	move_from = None	# Will store positions that user wants to move piece from/to
	move_to = None
	selected_square = None
	selected_piece = None
	highlight_positions = EMPTY_BB	# All positions highlighted by user
	highlight_moves = EMPTY_BB		# Moves possible by selected piece
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
				highlight_moves = EMPTY_BB
				x,y = event.pos
				selected_square = Position(xy=event.pos)
				# .............................................................Left Mouse Button
				if event.button == 1:	# LMB
					# Retrieve ally piece at that square if it exists
					selected_piece = gs.get_piece_at_pos(selected_square, side=ally_side)

					# If no previously selected piece and ally piece selected
					if not(move_from) and selected_piece:
						# Remember for movement next click
						move_piece = selected_piece
						move_from = selected_square
						# Get possible moves as bb
						highlight_moves = selected_piece.get_moves(selected_piece, gs)
						# highlight_moves = selected_piece.get_moves(selected_piece, gs)

					# If previously selected piece and not clicking same square 
					# and selected_square in selected_piece.moves
					elif move_from and move_from != selected_square and \
						 selected_square.bb & move_piece.moves:
						move_to = selected_square
						captured_piece = gs.get_piece_at_pos(selected_square, side=enemy_side)

					# If user didn't click on a valid square
					else:
						move_piece = None
						move_from = False
					highlight_positions = EMPTY_BB
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
		if gs.check:
			draw.check(screen, gs.ally_king.position.bb)

		draw.pieces(screen, gs.active_pieces, images)
		pg.display.update()
		clock.tick(FPS)