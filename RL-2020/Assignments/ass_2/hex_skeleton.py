import numpy as np

# The class that represents the board game.
class HexBoard:

	# Definitions.
	BLUE = 1
	RED = 2
	EMPTY = 3

	# Constructor.
	def __init__(self, board_size):
		self.board = {} # Board.
		self.size = board_size # Size of the board.
		self.game_over = False # Continue or stop the game.

		# Loop through all the tiles of the board.
		for x in range(board_size):
			for y in range (board_size):
				self.board[x,y] = HexBoard.EMPTY # Set them all empty.

	# Function that determines of the game is over.
	def is_game_over():
		return self.game_over

	# If a cell is empty, return coordinates.
	def is_empty(self, coordinates):
		return self.board[coordinates] == HexBoard.EMPTY

	# If a cell has a color, return coordinates.
	def is_color(self, coordinates, color):
		return self.board[coordinates] == color

	# Return coordinates of a cell. If coordinates are invalid (-1,-1), return EMPTY.
	def get_color(self, coordinates):
		if coordinates == (-1,-1):
			return HexBoard.EMPTY
		return self.board[coordinates]

	# Give a cell a color and stop the game if someone has won.
	def place(self, coordinates, color):
		if not self.game_over and self.board[coordinates] == HexBoard.EMPTY:
			self.board[coordinates] = color
			if self.check_win(HexBoard.RED) or self.check_win(HexBoard.BLUE):
				self.game_over = True

	# Returns the opposite of the given color.
	def get_opposite_color(self, current_color):
		if current_color == HexBoard.BLUE:
			return HexBoard.RED
		return HexBoard.BLUE

	# Returns the coordinates of the neighbour tiles.
	def get_neighbors(self, coordinates):
		(cx,cy) = coordinates
		neighbors = []
		if cx-1>=0:   neighbors.append((cx-1,cy))
		if cx+1<self.size: neighbors.append((cx+1,cy))
		if cx-1>=0    and cy+1<=self.size-1: neighbors.append((cx-1,cy+1))
		if cx+1<self.size  and cy-1>=0: neighbors.append((cx+1,cy-1))
		if cy+1<self.size: neighbors.append((cx,cy+1))
		if cy-1>=0:   neighbors.append((cx,cy-1))
		return neighbors

	# 
	def border(self, color, move):
		(nx, ny) = move
		return (color == HexBoard.BLUE and nx == self.size-1) or (color == HexBoard.RED and ny == self.size-1)

	# 
	def traverse(self, color, move, visited):
		if not self.is_color(move, color) or (move in visited and visited[move]): return False
		if self.border(color, move): return True
		visited[move] = True
		for n in self.get_neighbors(move):
			if self.traverse(color, n, visited): return True
		return False

	# Returns true if someone has won the game.
	def check_win(self, color):
		for i in range(self.size):
			if color == HexBoard.BLUE: move = (0,i)
			else: move = (i,0)
			if self.traverse(color, move, {}):
				return True
		return False

	# Print the current state of the board.
	def print(self):
		#print(f'\033c') # Clears terminal screen.
		print("   ",end="")
		for y in range(self.size):
			print(chr(y+ord('a')),"",end="")
		print("")
		print(" -----------------------")
		for y in range(self.size):
			print(y, "|",end="")
			for z in range(y):
				print(" ", end="")
			for x in range(self.size):
				piece = self.board[x,y]
				if piece == HexBoard.BLUE: print("\033[44mb\033[49m ",end="")
				elif piece == HexBoard.RED: print(f"\033[41mr\033[49m ",end="")
				else:
					if x==self.size:
						print("-",end="")
					else:
						print("- ",end="")
			print("|")
		print("   -----------------------")


# --- SELF WRITTEN FUNCTIONS ---

	# Make a cell empty.
	def make_empty(self,coordinates):
		self.board[coordinates] = HexBoard.EMPTY

	# Same as the place function but without the boolean variable game_over.
	def virtual_place(self,coordinates,color): 
		if self.board[coordinates] == HexBoard.EMPTY:
			self.board[coordinates] = color

	def random_move(self,board,BOARD_SIZE):
		available_moves = []
		for i in range(BOARD_SIZE):
			for j in range(BOARD_SIZE):
				if board.is_empty((i,j)):
					available_moves.append((i,j))
		if available_moves == []:
			return available_moves
		else:
		#print(available_moves)
			return available_moves[int(np.random.choice(np.linspace(0,len(available_moves)-1,len(available_moves))))]

	def move_check_win(self,board,BOARD_SIZE,last_move=BLUE):
		move = self.random_move(board,BOARD_SIZE)

		if move == []:
			return 0
		else:
			if not self.game_over and self.board[move] == HexBoard.EMPTY:
				if last_move == HexBoard.BLUE:
					self.board[move] = HexBoard.RED
				if last_move == HexBoard.RED:
					self.board[move] = HexBoard.BLUE

				if self.check_win(HexBoard.RED):
					return -1
					self.game_over = True
				if self.check_win(HexBoard.BLUE):
					return 1
					self.game_over = True

				if last_move == HexBoard.BLUE:
					return self.move_check_win(board,BOARD_SIZE,HexBoard.RED)
				if last_move == HexBoard.RED:
					return self.move_check_win(board,BOARD_SIZE,HexBoard.BLUE)