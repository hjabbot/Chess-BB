from board_constants import *

'''
All the pygame drawing wrapped up 


'''

import pygame as pg
# Custom imports
from constants import *		# Global variables


# Draws the checkerboard pattern
def board(screen):

	board_colours = [LIGHT_SQUARE_COLOUR, DARK_SQUARE_COLOUR]

	x,y = (0,0)
	i = False

	# For each column 
	for col in range(8):
		# For each row
		for row in range(8):
			# Colour flip flops between board_colours
			colour = board_colours[int(i)]
			i = not(i)

			# Draw the square there
			pg.draw.rect(screen, colour, (x,y,SQ_SIZE,SQ_SIZE))
			
			# Iterate row being drawn
			y = (y + SQ_SIZE) % (BOARD_HEIGHT)

		# Iterate col being drawn
		x += SQ_SIZE
		i = not(i)


# ...............................NEEDS WORK.........................................
# Draws the scorebar showing calculated advantage ratio
def score(screen, score):

	max_score = 32

	white_height = ((1/2 + score/max_score)*SCOREBAR_HEIGHT) // 1
	black_height = ((1/2 - score/max_score)*SCOREBAR_HEIGHT) // 1



	pg.draw.rect(screen, SCOREBAR_BORDER_COLOUR, (BOARD_WIDTH, 		0, 
												  SCOREBAR_WIDTH, 	SCOREBAR_HEIGHT))

	pg.draw.rect(screen, BLACK, (BOARD_WIDTH+SCOREBAR_BORDER, 		0, 
								 SCOREBAR_WIDTH-2*SCOREBAR_BORDER, 	black_height))

	pg.draw.rect(screen, WHITE, (BOARD_WIDTH+SCOREBAR_BORDER, 		black_height, 
								 SCOREBAR_WIDTH-2*SCOREBAR_BORDER, 	white_height))

# ...............................NEEDS WORK.........................................
# Draws the sidebar 
def sidebar(screen):
	pg.draw.rect(screen, SIDEBAR_BACKGROUND_COLOUR, (BOARD_WIDTH + SCOREBAR_WIDTH	, 0,
													 SIDEBAR_WIDTH					, SIDEBAR_HEIGHT))


def pieces(screen, pieces, images):
	# For each piece, draw at piece's position
	for piece in pieces:
		screen.blit(images[piece.label], (piece.position.pix_x, piece.position.pix_y))


def highlight(screen, positions):
	#Create the square to draw
	square = pg.Surface((SQ_SIZE, SQ_SIZE))
	square.fill(HIGHLIGHT_COLOUR)
	square.set_alpha(HIGHLIGHT_ALPHA)
	# For each square
	for cn, bb in SQUARE.items():
		# If square in positions
		if bb & positions:
			# Draw it
			x, y = bb2xy(bb)
			screen.blit(square, (x, y))

def moves(screen, positions):
	#Create the square to draw
	square = pg.Surface((SQ_SIZE, SQ_SIZE))
	square.fill(MOVES_COLOUR)
	square.set_alpha(MOVES_ALPHA)
	# For each square
	for cn, bb in SQUARE.items():
		# If square in positions
		if bb & positions:
			# Draw it
			x, y = bb2xy(bb)
			screen.blit(square, (x, y))

def selection(screen, position):
	# Get x,y coords of position
	x, y = bb2xy(position)

	# Border
	outer_square = pg.Surface((SQ_SIZE, SQ_SIZE))
	outer_square.fill(pg.Color(SELECTION_COLOUR))
	# outer_square.set_alpha(SELECTION_ALPHA)

	# Underlying square replication
	# Determine colour of underlying square
	sq_c = [LIGHT_SQUARE_COLOUR, DARK_SQUARE_COLOUR][(x//SQ_SIZE + y//SQ_SIZE) % 2]
	inner_square = pg.Surface((SQ_SIZE-2*SELECTION_BORDER_THICKNESS, 
							   SQ_SIZE-2*SELECTION_BORDER_THICKNESS))
	inner_square.fill(pg.Color(sq_c))

	# Draw on screen
	screen.blit(outer_square, (x, y))
	screen.blit(inner_square, (x+SELECTION_BORDER_THICKNESS, 
							   y+SELECTION_BORDER_THICKNESS))


def check(screen, check_square):
	# Get x,y coords of position
	x, y = bb2xy(check_square)

	# Border
	outer_square = pg.Surface((SQ_SIZE, SQ_SIZE))
	outer_square.fill(pg.Color(CHECK_COLOUR))
	# outer_square.set_alpha(SELECTION_ALPHA)

	# Underlying square replication
	# Determine colour of underlying square
	sq_c = [LIGHT_SQUARE_COLOUR, DARK_SQUARE_COLOUR][(x//SQ_SIZE + y//SQ_SIZE) % 2]
	inner_square = pg.Surface((SQ_SIZE-2*SELECTION_BORDER_THICKNESS, 
							   SQ_SIZE-2*SELECTION_BORDER_THICKNESS))
	inner_square.fill(pg.Color(sq_c))

	# Draw on screen
	screen.blit(outer_square, (x, y))
	screen.blit(inner_square, (x+SELECTION_BORDER_THICKNESS, 
							   y+SELECTION_BORDER_THICKNESS))