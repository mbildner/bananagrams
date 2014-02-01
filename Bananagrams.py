from random import shuffle


class GamePlayer(object):
	"""Holds game state for individual players and manages their state transitions"""
	def __init__(self, name):
		self.name = name
		self.tiles = []


class GameModel(object):
	"""Holds all game state and manages state transitions for the bananagrams game"""

	letter_distributions = {
	"a": 13, "b": 3, "c": 3, "d": 6, "e": 18,
	"f": 3,	"g": 4,	"h": 3,	"i": 12, "j": 2,
	"k": 2,	"l": 5,	"m": 3,	"n": 8,	"o": 11,
	"p": 3,	"q": 2,	"r": 9,	"s": 6,	"t": 9,
	"u": 6,	"v": 3,	"w": 3,	"x": 2,	"y": 3,
	"z": 2
	}

	def __init__(self, players):
		self.game_running = False

		self.tiles = self.create_tile_bucket()
		self.players = players
		self.number_of_players = len(self.players)
		self.tiles_per_person = self.calculate_tiles_per_person(self.number_of_players)


	def start_game(self):
		self.distribute_tiles(self.players)
		self.game_running = True


	# def end_game(self, player):
	# 	self.game_running = False


	def return_tiles(self, tiles, player):
		for tile in tiles:
			tile_index = player.tiles.index(tile)
			self.tiles += player.tiles.pop(tile_index)


	def dump(self, tile, player):
		if self.enough_tiles_for_dump():
			self.return_tiles([tile], player)
			self.give_player_tiles(3, player)
			return True

		else:
			return False



	def create_tile_bucket(self):
		nested_tile_lists = [letter * distribution for letter, distribution in self.letter_distributions.items()]
		tiles = [tile for sublist in nested_tile_lists for tile in sublist]
		shuffle(tiles)
		return tiles

	def get_number_of_tiles(self):
		return len(self.tiles)


	def enough_tiles_for_dump(self):
		# is player allowed to put their tile in and retrieve 3 remaining?
		return self.get_number_of_tiles() >= 2


	def enough_tiles_for_peel(self):
		return self.get_number_of_tiles() >= self.number_of_players


	def give_player_tiles(self, number_of_tiles, player):
		player.tiles += [self.tiles.pop() for tile in range(number_of_tiles)]


	def give_player_one_tile(self, player):
		self.give_player_tiles(1, player)


	
	def calculate_tiles_per_person(self, number_of_players):
		if number_of_players < 5:
			return 21
		elif number_of_players < 7:
			return 15
		elif number_of_players > 6:
			return 11


	def distribute_tiles(self, players):
		tiles_per_person = self.tiles_per_person
		for player in players:
			self.give_player_tiles(tiles_per_person, player)
			












