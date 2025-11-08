# Reincorment Learning 2020 - Assignment 2: Adaptive Sampling
# Auke Bruinsma (s1594443), Meng Yao (s2308266), Ella (s2384949).
# This file contains part 1 of the assignment: MCTS Hex - 3 points

# Imports.
import numpy as np
import copy
from hex_skeleton import HexBoard
from node import Node
import random as rd
import sys 

# Global variables
BOARD_SIZE = 4
AI = HexBoard.BLUE
PLAYER = HexBoard.RED
EMPTY = HexBoard.EMPTY
inf = float('inf')
C_p = 1
itermax = 10

# Digit to letter conversion.
def d2l_conversion(x_coor):
	letter_arr = np.array(['a','b','c','d','e','f','g','h','i','j']) # Max a playfield of 10 by 10.
	return letter_arr[x_coor]

# Letter to digit conversion.
def l2d_conversion(letter):
	letter_arr = np.array(['a','b','c','d','e','f','g','h','i','j'])
	for i in range(len(letter_arr)):
		if letter == letter_arr[i]:
			return i

def MCTS(rootstate,itermax,C_p):
	# Initialise rootnote.
	rootnode = Node(state = rootstate)
	node = rootnode

	# Loop until the max number of iterations is reached.
	for i in range(itermax):
		board = copy.deepcopy(rootstate)

		action = node.check_visits(node)

		counter = 0 # This counter solves a bug.

		# Selection
		while action != True:
			counter += 1
			action = node.check_visits(node)
			if action == False:
				node.collapse(node,board,BOARD_SIZE)
			elif action == 2:
				node,move = node.UCTSelectChild(C_p,inf)
				board.virtual_place(move,AI)
				action = node.check_visits(node)
				if action == False:
					node.collapse(node,board,BOARD_SIZE)
			if counter == 10:
				action = True

		# Expansion
		while node.childNodes != []: # If there are children ...
			node,move = node.UCTSelectChild(C_p,inf)
			board.virtual_place(move,AI)

		# Play-out.
		# Check if the node has been visited.
		if node.V == 0:
			result = board.move_check_win(board,BOARD_SIZE)

		# Backpropagate:
		while node != None:
			node.update(result)
			if node.parent == None:
				break;
			node = node.parent

		#node.tree_info(rootnode,C_p,inf)

	return node.UCTSelectChild(C_p,inf)[1]

# Player makes a move.
def player_make_move(board):
	print('Next move.')
	x = l2d_conversion(input(' x: '))
	y = int(input(' y: '))
	
	board.place((x,y),PLAYER)
	
if __name__ == '__main__':
	# Initialise a board.
	board = HexBoard(BOARD_SIZE)
	board.print()

	while not board.game_over:
		board.place((MCTS(board,itermax,C_p=C_p)),AI)
		board.print()
		if board.check_win(AI):
			print('AI has won.')
			break
		player_make_move(board)
		board.print()
		if board.check_win(PLAYER):
			print('PLAYER has won.')

