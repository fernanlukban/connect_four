class Player():
	def __init__(self, piece, isTurn = True):
		self.piece = piece
		self.isTurn = True
		self.hasWon = False

class Node():
	def __init__(self, compass = {}, value = 0):
		self.compass = compass
		self.value = value

class Grid():
	def __init__(self, rows = 6, columns = 7):
		self.rows = rows
		self.columns = columns
		self.grid = self.setup_grid()

	def setup_grid(self):

		def create_row(columns):
			return [Node() for x in range(columns)]

		def create_grid(columns, rows):
			return [create_row(columns) for x in range(rows)]

		grid = create_grid(self.columns, self.rows)

		'''compass = {N, NE, E, SE, S, SW, W, NW}'''

		first_row = 0
		last_row = self.rows - 1
		first_column = 0
		last_column = self.columns - 1

		for i in range(self.columns):
			for j in range(self.rows):
				compass = {}
				if i != last_column:
					compass['E'] = grid[j][i+1]
				if i != first_column:
					compass['W'] = grid[j][i-1]
				if j != first_row:
					compass['N'] = grid[j-1][i]
					if i != last_column:
						compass['NE'] = grid[j-1][i+1]
					if i != first_column:
						compass['NW'] = grid[j-1][i-1]
				if j != last_row:
					compass['S'] = grid[j+1][i]
					if i != first_column:
						compass['SW'] = grid[j+1][i-1]
					if i != last_column:
						compass['SE'] = grid[j+1][i+1]
				grid[j][i].compass = compass

		return grid


class Game():
	def __init__(self, player1, player2):
		self.grid = Grid()
		self.grid.setup_grid()
		self.player1 = player1
		self.player2 = player2

	def print_grid(self):
		for x in range(1, self.grid.columns+1):
			print(x, end='')
		print()
		for row in self.grid.grid:
			for node in row:
				print(node.value, end='')
			print()

	def make_move(self, player, column):
		grid = self.grid.grid
		def next_spot(row, column):
			current_node = grid[row][column]
			if row == self.grid.rows-1:
				self.grid.grid[self.grid.rows-1][column].value = player.piece
			elif current_node.compass['S'].value != 0:
				self.grid.grid[row][column].value = player.piece
			else:
				return next_spot(row+1, column)
		next_spot(0, column-1)

	def get_input(self):
		while(True):
			try:
				move = int(input("What is your move? Column #"))
			except ValueError:
				print('That is not a valid input, try again\n')
				continue
			if move not in range(1, self.grid.columns+1):
				print("Not a valid column, try again\n")
				continue
			if self.grid.grid[0][move-1].value != 0:
				print("Spot already taken, try again\n")
				continue
			else:
				return move

	def turn(self, player1, player2):
		self.print_grid()
		if player1.isTurn:
			print("Player 1's Turn")
			move = self.get_input()
			self.make_move(player1, move)
			player1.isTurn = False
			player2.isTurn = True
		else:
			print("Player 2's Turn")
			move = self.get_input()
			self.make_move(player2, move)
			player2.isTurn = False
			player1.isTurn = True
		print()

	def game_over(self, player):
		def connected(node, direction):
			if direction not in node.compass:
				return 0
			if node.value != player.piece or node.compass[direction].value != player.piece:
				return 0
			else:
				return 1 + connected(node.compass[direction], direction)

		for row in self.grid.grid:
			for node in row:
				for direction in node.compass:
					if connected(node, direction) == 3:
						return True
						
		return False


	def start_game(self):
		while(True):
			self.turn(self.player1, self.player2)
			#print(self.game_over(self.player1))
			#print(self.game_over(self.player2))
			if self.game_over(self.player1):
				self.print_grid()
				self.player1.hasWon = True
				print('Game Over\nPlayer One Won')
				break;
			elif self.game_over(self.player2):
				self.print_grid()
				self.player2.hasWon = True
				print('Game Over\nPlayer Two Won')
				break;

player1 = Player('A')
player2 = Player('B', False)
connect_four = Game(player1, player2)
connect_four.start_game()