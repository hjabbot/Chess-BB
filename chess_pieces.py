# Generates pieces based on INITIAL_BOARD
def initialise_pieces():
	bb_location = START_BB
	pieces = []

	board = np.rot90(INITIAL_BOARD, k=3)

	# For each square
	for row in range(len(board)):
		for col in range(len(board[row])):
			# Get piece on square
			square = board[col][row]
			position = Position(bb=bb_location)
			# If not empty
			if square != '--':
				# Add to piece list
				pieces.append(Piece(square, position))
			# Move to next square to test
			bb_location = shift(bb_location, 1)

	return pieces
