# Reincorment Learning 2020 - Assignment 2: Adaptive Sampling
# Auke Bruinsma (s1594443), Meng Yao (s2308266), Ella (s2384949).
# This file contains part 2 of the assignment: Experiment - 3 points

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
SEARCH_DEPTH = 4
AI = HexBoard.BLUE
PLAYER = HexBoard.RED
EMPTY = HexBoard.EMPTY
inf = float('inf')
INF = 11

# Alphabeta search function.
def alphabeta(board,d,a,b,mx=True):
	best_move = (-1,-1) # # Will always be updated.
	if d <= 0:
		return heuristic_eval(board)
	elif mx == True:
		g = -INF
		for i in range(BOARD_SIZE):
			for j in range(BOARD_SIZE):
				if board.is_empty((i,j)):
					board.virtual_place((i,j),AI)
					#board.print()
					g_optimal = g
					g = max(g,alphabeta(board,d-1,a,b,mx=False))
					a = max(a,g) # Update alpha.

					if g > g_optimal:
						best_move = (i,j)
					board.make_empty((i,j))
					if g >= b:
						break
	elif mx == False:
		g = INF
		for i in range(BOARD_SIZE):
			for j in range(BOARD_SIZE):
				if board.is_empty((i,j)):
					board.virtual_place((i,j),PLAYER)
					#board.print()
					g = min(g,alphabeta(board,d-1,a,b,mx=True))
					b = min(b,g) # Update beta

					board.make_empty((i,j))
					if a >= g:
						break
	if d == SEARCH_DEPTH:
		f = open('movelist.txt','a')
		f.write(f'\n{mcts_hex.d2l_conversion(best_move[0])},{best_move[1]}')
		f.close()
	return g

# Heuristic evaluation function.
def heuristic_eval(board):
	# For now, the evaluation function is just a random number.
	random_number = rd.randint(1,9)

	return random_number

# The AI makes a move.
def ai_make_move(board):
	with open('movelist.txt','r') as f:
		x = ''; y = ''
		find_x = True
		lines = f.read().splitlines()
		for char in lines[-1]: # Should work for numbers with digits > 1.
			if char == ',':
				find_x = False
			elif find_x == True:
				x += char
			elif find_x == False:				
				y += char
			
		move_to_make = (mcts_hex.l2d_conversion(x),int(y))
		board.place(move_to_make,PLAYER)

# Play the game.
def play_game(board):
	# Make a copy for the search algorithm.
	virtual_board = board

	# Make a text file for the moves.
	f = open('movelist.txt','w')
	f.write('Movelist alphabeta')
	f.close()

	while not board.game_over:
		# Alphabeta part.
		eval_val = alphabeta(virtual_board,d=SEARCH_DEPTH,a=-INF,b=INF)
		ai_make_move(board)
		board.print()
		if board.check_win(PLAYER):
			print('Alphabeta has won.')
			break

		# MCTS part.
		board.place((mcts_hex.MCTS(board,mcts_hex.itermax,mcts_hex.C_p)),AI)
		board.print()
		if board.check_win(AI):
			print('MCTS has won.')

if __name__ == '__main__':
	board = HexBoard(BOARD_SIZE)

	# Play the game.
	play_game(board)