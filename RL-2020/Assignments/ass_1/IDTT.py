# Reincorment Learning 2020 - Assignment 1: Heuristic Planning
# Auke Bruinsma (s1594443), Meng Yao (s2308266), Ella (s2384949).
# This file contains part 6 of the assignment: Iterative Deepening and Transposition Tables.

# Imports.
import numpy as np
from hex_skeleton import HexBoard
import random as rd
from trueskill import Rating, quality_1vs1, rate_1vs1
import search
import evaluation 
import sys 
from datetime import datetime, timedelta

# Global variables
BOARD_SIZE = search.BOARD_SIZE
AI = HexBoard.BLUE
PLAYER = HexBoard.RED
EMPTY = HexBoard.EMPTY
INF = 11

def lookup(board, d):
    with open('transposition_table.txt','r') as f:
        lines = f.read().splitlines()
        for line in lines:
            if line.split(', ')[0] == board:
                shallow = 0
                if line.split(', ')[2] == d:
                    return True, line.split(', ')[1], line.split(', ')[3]
                # Should we find the bm for the second deepest search??
                # if not hit at this depth , still use tt−bestmove
                else:
                    if line.split(', ')[2] > shallow:
                        shallow = line.split(', ')[2]
                        second_deepest = [False, line.split(', ')[1], line.split(', ')[3]]
    return second_deepest[0], second_deepest[1], second_deepest[2]

def store(board,g,d,bm):
	f = open('transposition_table.txt','a')
	f.write(f'{board},{g},{d},{bm}\n')
	f.close()

def ttalphabeta(board,a,b,d,mx=True):
	bm = ()
	if d <= 0:
		g = evaluation.heuristic_eval(board)
		#bm = ()
	elif mx == True:
		g = -INF
		for i in range(BOARD_SIZE):
			for j in range(BOARD_SIZE):
				if board.is_empty((i,j)):
					board.virtual_place((i,j),AI)
					gc = ttalphabeta(board,a,b,d-1,mx=False)
					if gc > g:
						bm = (i,j)
						g = gc
					a = max(a,g)
					if a >= b:
						break
	elif mx == False:
		g = INF
		for i in range(BOARD_SIZE):
			for j in range(BOARD_SIZE):
				if board.is_empty((i,j)):
					gc = ttalphabeta(board,a,b,d-1,mx=True)
					if gc < g:
						bm = (i,j)
						g = gc
					b = min(b,g)
					if a >= b:
						break

	if board.board in board_states:
		board_states.append(board.board)
		store(board.board,g,d,bm)
	
	return g

def iterative_deepening(board,runtime):
	d = 1
	end_time = datetime.now() + timedelta(seconds=runtime)
	while datetime.now() < end_time:
		f = minimax(board,d)
		d = d + 1
	return f

if __name__ == '__main__':
	# Initialise the board.
	board = HexBoard(BOARD_SIZE)

	# Make a copy for the search algorithm.
	virtual_board = board

	f = open('transposition_table.txt','w')
	#f.write(f'{board},{g},{d},{bm}\n')
	f.close()

	board_states = []
	ttalphabeta(virtual_board,-INF,INF,d=3)
	#print(board_states)