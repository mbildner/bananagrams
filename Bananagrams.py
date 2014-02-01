from random import shuffle

class GameModel(object):
	"""Holds all game state and manages state transitions for the bananagrams game"""

	letter_distributions = {
	"a": 13, "b": 3, "c": 3, "d": 6, "e": 18,
	"f": 3,	"g": 4,	"h": 3,	"i": 12, "j": 2,
	"k": 2,	"l": 5,	"m": 3,	"n": 8,	"o": 11,
	"p": 3,	"q": 2,	"r": 9,	"s": 6,	"t": 9,
	"u": 6,	"v": 3,	"w": 3,	"x": 2,	"y": 3,
	"z": 2}

	def __init__(self, players):
		self.tiles = self.create_tile_bucket(self)
		self.players = players

		self.number_of_players = len(self.players)

	def create_tile_bucket(self, number_of_tiles):
		nested_tile_lists = [letter * distribution for letter, distribution in self.letter_distributions.items()]
		tiles = [tile for sublist in nested_tile_lists for tile in sublist]
		shuffle(tiles)
		return tiles
		
	def give_player_tile(self, tiles, player):
		pass
		
	def distribute_tiles(self, tiles, players):
		if self.number_of_players < 5:
			tiles_per_person = 21
		else if self.number_of_players < 7:
			tiles_per_person = 15
		else if self.number_of_players > 6:
			tiles_per_person = 11

		for player in players:
			self.give_player_tile(tiles, player)
			






class GamePlayer(object):
	"""Holds game state for individual players and manages their state transitions"""
	def __init__(self, name, tiles):
		self.name = name
		self.tiles = tiles


