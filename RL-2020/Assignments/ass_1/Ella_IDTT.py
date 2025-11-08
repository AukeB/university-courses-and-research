# This file contains part 6 of the assignment: Iterative Deepening and Transposition Tables

# Imports.
import search 
from hex_skeleton import HexBoard 

# Global variables
BOARD_SIZE = 4
AI = HexBoard.BLUE
PLAYER = HexBoard.RED
EMPTY = HexBoard.EMPTY
INF = 11

# use tt results to transform a tree search algorithms into graph search algorithms
def ttalphabeta(board,d,a,b,mx):
    # d: depth, ttbm: tt-bestmove, g: search value
    (hit, g, ttbm) = lookup(board, d)
    if hit:
        return g
    
    if d <= 0:
        g = heuristic_eval(board)
        bm = (-1,-1) 
    
    elif mx == True:
        g = -INF
        board.virtual_place(ttbm, AI)
        # search for tt-bestmove's children
        # now it's player's turn
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
                        break # alpha cutoff

    elif mx == False:
        g = INF
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board.is_empty((i,j)):
                    board.virtual_place((i,j),AI)
                    #board.print()
                    g_optimal = g
                    g = max(g, alphabeta(board,d-1,a,b,mx=False))
                    a = max(a, g) # Update alpha.

                    f = open('alphabeta.txt','a')
                    f.write(f'd = {d} g = {g} a = {a} b = {b}\n')
                    f.close()
                    # only store bestmove when it's AI's turn
                    if g > g_optimal:
                        bm = (i,j)
                    board.make_empty((i,j))
                    if g >= b:
                        break # beta cutoff
    store(board, g, d, bm)
    return g

def iterativedeepening(board,d,a,b,mx=True):
    d = 1
    while not keypressed() and not time_is_up():
        f = ttalphabeta(board,d,a,b,mx=True)
        d = d + 1
    f = open('movelist.txt','a')
    f.write(f'\n{d2l_conversion(bm[0])},{bm[1]}')
    f.close()
    return f
   
    
def lookup(board, d):
    with open('TranspositionTable.txt','r') as f:
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
                        
def store(board, g, d, bm):
    f = open('TranspositionTable.txt', 'a')
    f.write(f'\n{board}, {g}, {d}, {bm}')
    f.close()

