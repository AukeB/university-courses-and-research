# Reincorment Learning 2020 - Assignment 1: Heuristic Planning
# Auke Bruinsma (s1594443), Meng Yao (s2308266), Ella (s2384949).
# This file contains part 5 of the assignment: Experiment.

# Imports.
import numpy as np
from hex_skeleton import HexBoard
import random as rd
from trueskill import Rating, quality_1vs1, rate_1vs1
import search
import evaluation 
import sys 

# Global variables
BOARD_SIZE = search.BOARD_SIZE
AI = HexBoard.BLUE
AI2 = HexBoard.RED
EMPTY = HexBoard.EMPTY
INF = 11

# The second AI makes a move.
def ai2_make_move(board):
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
		
		move_to_make = (search.l2d_conversion(x),int(y))
		board.place(move_to_make,AI2)
		board.print()

# Alphabeta search function.
def alphabeta(board,d,a,b,p1,p2,ev,mx=True):
	best_move = (-1,-1) # # Will always be updated.
	if d <= 0:
		if ev == 'dijkstra':
			return evaluation.heuristic_eval(board)
		if ev == 'random':
			return search.heuristic_eval(board)
	elif mx == True:
		g = -INF
		for i in range(BOARD_SIZE):
			for j in range(BOARD_SIZE):
				if board.is_empty((i,j)):
					board.virtual_place((i,j),AI)
					#board.print()
					g_optimal = g
					g = max(g,alphabeta(board,d-1,a,b,p1,p2,ev,mx=False))
					a = max(a,g) # Update alpha.

					f = open('alphabeta.txt','a')
					f.write(f'd = {d} g = {g} a = {a} b = {b}\n')
					f.close()

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
					board.virtual_place((i,j),AI2)
					#board.print()
					g = min(g,alphabeta(board,d-1,a,b,p1,p2,ev,mx=True))
					b = min(b,g) # Update beta

					f = open('alphabeta.txt','a')
					f.write(f'd = {d} g = {g} a = {a} b = {b}\n')
					f.close()

					board.make_empty((i,j))
					#virtual_board.print()
					if a >= g:
						break
	if d == search_depth:
		f = open('movelist.txt','a')
		f.write(f'\n{search.d2l_conversion(best_move[0])},{best_move[1]}')
		f.close()
	return g

# Initialise the board.
board = HexBoard(BOARD_SIZE)

# Create a virtual board for the alphabeta algorithm.
virtual_board = board

# Make a text file for the moves.
f = open('movelist.txt','w')
f.write('Movelist')
f.close()


while not board.game_over:
	search_depth = 3
	eval_val = alphabeta(virtual_board,d=search_depth,a=-INF,b=INF,p1=AI,p2=AI2,ev='random',mx=True)
	search.ai_make_move(board)

	search_depth = 3
	eval_val = alphabeta(virtual_board,d=search_depth,a=-INF,b=INF,p1=AI2,p2=AI,ev='dijkstra',mx=True)
	ai2_make_move(board)


r1,r2 = Rating(),Rating()
r1,r2 = rate_1vs1(r1,r2)
r1,r2 = rate_1vs1(r1,r2)
r1,r2 = rate_1vs1(r1,r2)
r1,r2 = rate_1vs1(r1,r2)
r1,r2 = rate_1vs1(r1,r2)
r1,r2 = rate_1vs1(r1,r2)

r1,r2 = rate_1vs1(r1,r2)
r1,r2 = rate_1vs1(r1,r2)
r1,r2 = rate_1vs1(r1,r2)
r1,r2 = rate_1vs1(r1,r2)
r1,r2 = rate_1vs1(r2,r1)
r1,r2 = rate_1vs1(r1,r2)

print(r1,r2)

