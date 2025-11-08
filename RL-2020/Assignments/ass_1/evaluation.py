# Reincorment Learning 2020 - Assignment 1: Heuristic Planning
# Auke Bruinsma (s1594443), Meng Yao (s2308266), Ella (s2384949).
# This file contains part 4 of the assignment: Evaluation.

# Imports.
import numpy as np
from hex_skeleton import HexBoard
import random as rd
import search
import sys 

# Global variables
BOARD_SIZE = search.BOARD_SIZE
SEARCH_DEPTH = 3
AI = HexBoard.BLUE
PLAYER = HexBoard.RED
EMPTY = HexBoard.EMPTY
INF = 11

'''
To test Dijkstra's shortest path algorithm, we are not going to play
the game yet, but first populate the board in a certain way and then
run Dijkstra's algorithm on that certain board state. If we have succeeded
in that, we can implement in playing the game.
'''

def populate_board(board):
	# Place player pieces.
	board.place((4,3),PLAYER)
	#board.place((1,5),PLAYER)
	board.place((5,3),PLAYER)
	board.place((5,4),PLAYER)

	# Play AI pieces.
	board.place((3,2),AI)
	board.place((4,2),AI)
	board.place((5,2),AI)
	board.place((3,3),AI)
	#board.place((3,4),AI)
	#board.place((2,4),AI)

	board.print()

def shortest_path(board,player):
	# Create list of possible starting positions.
	starting_point = []

	if player == AI:
		for i in range(BOARD_SIZE):
			starting_point.append((0,i))
	if player == PLAYER:
		for i in range(BOARD_SIZE):
			starting_point.append((i,0))

	# Make a distance graph.
	distance_graph = np.zeros((BOARD_SIZE,BOARD_SIZE))
	distance_graph.fill(INF)

	for i in range(len(starting_point)):
		current_point = starting_point[i]
		visited = []
		distance_graph[current_point[1],current_point[0]] = 0

		if player == AI:
			AI_update_distances(board,current_point,distance_graph,visited)
		if player == PLAYER:
			PLAYER_update_distances(board,current_point,distance_graph,visited)

	if player == AI:
		return min(distance_graph[:,-1])
	if player == PLAYER:
		return min(distance_graph[-1])


def AI_update_distances(board,current_point,distance_graph,visited):
	border_reached = False

	if board.border(AI,current_point) == True:
		border_reached = True

	cur_distance = distance_graph[current_point[1],current_point[0]]
	shortest = INF
	next_point = []

	neighbors = board.get_neighbors(current_point)

	for i in range(len(neighbors)):
		if neighbors[i] not in visited and board.is_color(neighbors[i],PLAYER) == False:
			next_distance = cur_distance + 1

			if board.is_color(neighbors[i],AI) == True and cur_distance < distance_graph[neighbors[i][1],neighbors[i][0]]:
				distance_graph[neighbors[i][1],neighbors[i][0]] = cur_distance
				next_point = neighbors[i]
				shortest = cur_distance
			elif next_distance < distance_graph[neighbors[i][1],neighbors[i][0]]:
				distance_graph[neighbors[i][1],neighbors[i][0]] = next_distance

			if next_distance < shortest:
				next_point = neighbors[i]
				shortest = next_distance

	visited.append(current_point)

	if (current_point[0]+1,current_point[1]) in neighbors:
		for i in range(len(neighbors)):
			if board.is_color(neighbors[i],AI) == True:
				break
			else:
				next_point = (current_point[0]+1,current_point[1])

	if len(next_point) != 0 and border_reached == False:
		AI_update_distances(board,next_point,distance_graph,visited)

def PLAYER_update_distances(board,current_point,distance_graph,visited):
	border_reached = False

	if board.border(PLAYER,current_point) == True:
		border_reached = True

	cur_distance = distance_graph[current_point[1],current_point[0]]
	shortest = INF
	next_point = []

	neighbors = board.get_neighbors(current_point)

	for i in range(len(neighbors)):
		if neighbors[i] not in visited and board.is_color(neighbors[i],AI) == False:
			next_distance = cur_distance + 1

			if board.is_color(neighbors[i],PLAYER) == True and cur_distance < distance_graph[neighbors[i][1],neighbors[i][0]]:
				distance_graph[neighbors[i][1],neighbors[i][0]] = cur_distance
				next_point = neighbors[i]
				shortest = cur_distance
			elif next_distance < distance_graph[neighbors[i][1],neighbors[i][0]]:
				distance_graph[neighbors[i][1],neighbors[i][0]] = next_distance

			if next_distance < shortest:
				next_point = neighbors[i]
				shortest = next_distance

	visited.append(current_point)

	if (current_point[0],current_point[1]+1) in neighbors:
		for i in range(len(neighbors)):
			if board.is_color(neighbors[i],PLAYER) == True:
				break
			else:
				next_point = (current_point[0],current_point[1]+1)

	if len(next_point) != 0 and border_reached == False:
		PLAYER_update_distances(board,next_point,distance_graph,visited)

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
					board.virtual_place((i,j),PLAYER)
					#board.print()
					g = min(g,alphabeta(board,d-1,a,b,mx=True))
					b = min(b,g) # Update beta

					f = open('alphabeta.txt','a')
					f.write(f'd = {d} g = {g} a = {a} b = {b}\n')
					f.close()

					board.make_empty((i,j))
					#virtual_board.print()
					if a >= g:
						break
	if d == SEARCH_DEPTH:
		f = open('movelist.txt','a')
		f.write(f'\n{search.d2l_conversion(best_move[0])},{best_move[1]}')
		f.close()
	return g

def heuristic_eval(board):
	AI_heur_val = shortest_path(board,player=AI)
	PLAYER_heur_val = shortest_path(board,player=PLAYER)

	return PLAYER_heur_val - AI_heur_val

# Play the game.
def play_game(board):
	# Make a copy for the search algorithm.
	virtual_board = board

	# Make a text file for the moves.
	f = open('movelist.txt','w')
	f.write('Movelist')
	f.close()

	# Make a text file for the alphabeta algorithm.
	f = open('alphabeta.txt','w')
	f.write('Alphabeta search.')
	f.write(f'\n Board size:   {BOARD_SIZE}')
	f.write(f'\n Search depth: {SEARCH_DEPTH}\n\n')
	f.close()

	while not board.game_over:
		eval_val = alphabeta(virtual_board,d=SEARCH_DEPTH,a=-INF,b=INF)
		search.ai_make_move(board)
		search.player_make_move(board)

if __name__ == '__main__':
	# Initialise the board.
	board = HexBoard(BOARD_SIZE)

	# Populate board and print it.
	#populate_board(board)

	# Play the game.
	play_game(board)









