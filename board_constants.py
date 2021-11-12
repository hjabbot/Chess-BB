
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

INITIAL_BOARD = [
			['bR','bN','bB','bQ','--','bR','bK','--'],
			['bp','bp','bp','bp','--','wN','bp','bp'],
			['--','--','bN','--','--','bN','--','--'],
			['--','--','--','--','bp','--','--','--'],
			['--','--','wB','--','wp','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['wp','wp','wp','wp','--','wp','wp','wp'],
			['wR','wN','wB','wQ','wK','--','wN','wR']
			]


# INITIAL_BOARD = [
# 			['bR','--','--','--','bK','--','--','bR'],
# 			['--','--','bp','--','--','--','--','--'],
# 			['--','--','--','--','--','--','--','--'],
# 			['--','--','--','wp','--','--','--','--'],
# 			['--','bp','--','--','--','--','--','--'],
# 			['--','--','--','--','--','--','--','--'],
# 			['wp','--','--','--','--','--','--','--'],
# 			['wB','--','--','--','wK','--','wR','--']
# 			]




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




# ............................................................................ Value
PAWN_VALUE = 1
ROOK_VALUES = 5
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
QUEEN_VALUE = 8
KING_VALUE = 100
