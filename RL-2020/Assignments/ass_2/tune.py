# Reincorment Learning 2020 - Assignment 2: Adaptive Sampling
# Auke Bruinsma (s1594443), Meng Yao (s2308266), Ella (s2384949).
# This file contains part 3 of the assignment: Tune - 3 points

# Imports.
import numpy as np
import random as rd
import copy
import sys

from hex_skeleton import HexBoard
from node import Node

import mcts_hex

# Global variables
BOARD_SIZE = mcts_hex.BOARD_SIZE
AI = HexBoard.BLUE
PLAYER = HexBoard.RED
EMPTY = HexBoard.EMPTY
inf = float('inf')
INF = 11

# Play the game.
def play_game(board):
	# Make a copy for the search algorithm.
	virtual_board = board

	itermax_1 = 100
	itermax_2 = 100
	C_p_1 = 10
	C_p_2 = 1

	while not board.game_over:
		# MCTS 1.
		board.place((mcts_hex.MCTS(board,itermax_1,C_p_1)),PLAYER)
		board.print()
		if board.check_win(PLAYER):
			print('MCTS 1 has won.')
			break

		# MCTS 2.
		board.place((mcts_hex.MCTS(board,itermax_2,C_p_2)),AI)
		board.print()
		if board.check_win(AI):
			print('MCTS 2 has won.')




if __name__ == '__main__':
	board = HexBoard(BOARD_SIZE)

	# Play the game.
	play_game(board)