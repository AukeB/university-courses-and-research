# Imports
import numpy as np
from hex_skeleton import HexBoard

# The class that governs nodes.
class Node:
	# Making a new node.
	def __init__(self,move = None,state = None,parent = None):
		self.state = state
		self.parent = parent
		self.V = 0 # Visit count.
		self.W = 0 # Win count.
		self.childNodes = [] # For the children that will be added.
		self.moves = []
		self.untriedMoves = [] # For the moves that hasn't been tried yet.

	def add_children(self,node,children):
		children = Node() # Initialise children.
		node.childNodes.append(children) # Make children.
		node.childNodes[-1].parent = node # Define parent for children.
		node.childNodes[-1].V = 0
		node.childNodes[-1].W = 0

	def add_moves(self,node,move):
		self.moves.append(move)

	def UCT(self,node,C_p,inf):
		inf = 10e10 # Probably high enough.
		if node.W == 0:
			if C_p == 0:
				return 0
			else:
				return inf
		else:
			return node.W/node.V+C_p*np.sqrt(np.log(node.parent.V)/node.V)

	def UCTSelectChild(self,C_p,inf):
		values = []
		for i in range(len(self.childNodes)):
			values.append(self.UCT(self.childNodes[i],C_p,inf))
		return self.childNodes[np.argmax(values)],self.moves[np.argmax(values)]

	def update(self,result):
		self.V += 1
		self.W += result

	def tree_info(self,node,C_p,inf): # Up to 3 generations.
		print(f'Root: {node.V,node.W}')

		if node.childNodes != []:
			for i in range(len(node.childNodes)):
				print(f'Child {i}: {node.childNodes[i].V,node.childNodes[i].W} UCT: {self.UCT(self.childNodes[i],C_p,inf)}')
				if node.childNodes[i].childNodes != []:
					for j in range(len(node.childNodes[i].childNodes)):
						print(f'Grandchild {i,j}: {node.childNodes[i].childNodes[j].V,node.childNodes[i].childNodes[j].W} UCT: {self.UCT(self.childNodes[i].childNodes[j],C_p,inf)}')

	def collapse(self,node,board,BOARD_SIZE):
		#print('Collapsing')
		for i in range(BOARD_SIZE):
			for j in range(BOARD_SIZE):
				if board.is_empty((i,j)):
					board.virtual_place((i,j),HexBoard.BLUE)
					node.add_children(node,board)
					node.add_moves(node,(i,j))
					#print(node.childNodes)
					#print(node.childNodes[-1].V)
					#print(node.V)
					#board.print()
					board.make_empty((i,j))

	def check_visits(self,node):
		#print(node.childNodes)
		if node.childNodes != []: # If there are children ...
			for i in range(len(node.childNodes)):
				#print(node.childNodes[i].V)
				if node.childNodes[i].V == 0:
					return True
			return 2
		return False






