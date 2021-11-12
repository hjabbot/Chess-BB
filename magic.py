from constants import *
from functions import *
from multiprocessing import Pool
import random

def gen_sparse_random(bits=64):
	return random.getrandbits(bits) & random.getrandbits(bits) & random.getrandbits(bits)


def find_magic_number(square, num_relevant_bits, piece_type):
	# Initialise as per piece type
	if piece_type == 'R':
		attack_mask = masked_rook_attacks()[square]
		directions = ROOK_DIRECTIONS
	elif piece_type == 'B':
		attack_mask = masked_bishop_attacks()[square]
		directions = BISHOP_DIRECTIONS
	elif piece_type == 'Q':
		attack_mask = mask_queen_attacks()[square]
		directions = QUEEN_DIRECTIONS
	
	occupancy_indicies = 1 << num_relevant_bits

	# Initialise arrays 
	occupancies 	= [EMPTY] * 4096 	# Combinations of blocking pieces and empty spaces
	attacks 		= [EMPTY] * 4096	# Moves that these combinations allow
	used_attacks 	= [EMPTY] * 4096	# Ensures no overlap in hashing function

	# For each possible combination of spaces/pieces along attack axis
	for index in range(occupancy_indicies):
		# Generate combination
		occupancies[index] = set_occupancy(index, num_relevant_bits, attack_mask)
		# Get attacks accounting for blocked squares
		attacks[index] = gen_slide_attacks(square, occupancies[index], directions)

	# Brute force finding magic numbers
	for r in range(10000000):
		magic_number = gen_sparse_random(bits=64)

		# Skip inappropriate numbers
		if count_bits((attack_mask * magic_number) & 0xFF00000000000000) < 6: continue

		# For each combination defined above
		for index in range(occupancy_indicies):
			# Generate a magic key
			magic_index = ((occupancies[index] * magic_number) & FULL) >> (64 - num_relevant_bits)

			# Check if hash is unique
			if used_attacks[magic_index] == EMPTY:
				used_attacks[magic_index] = attacks[index]
			elif used_attacks[magic_index] != attacks[index]:
				break
		else:
			return EMPTY

	return magic_number


def init_magic_numbers(cn):
	# return ("'{cn}': {mn}".format(cn=cn, mn=find_magic_number(cn, NUM_RELEVANT_BITS_ROOK[cn], piece_type = 'R')))
	return ("'{cn}': {mn}".format(cn=cn, mn=find_magic_number(cn, NUM_RELEVANT_BITS_BISHOP[cn], piece_type = 'B')))
	# return ("'{cn}': {mn}".format(cn=cn, mn=find_magic_number(cn, NUM_RELEVANT_BITS_QUEEN[cn], piece_type = 'Q')))


if __name__ == '__main__':
	cns = [cn for cn, bb in CN2BB.items()]
	with Pool(12) as p:
		print(p.map(init_magic_numbers, cns))

	# occupancy = EMPTY | d7 | c4 | d1 | f4

	# bbprint(magic_rook_attacks('d4', occupancy))