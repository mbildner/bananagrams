import unittest
from Bananagrams import GameModel, GamePlayer

from copy import deepcopy



class TestInitializeGameFunction(unittest.TestCase):
	def setUp(self):
	 	player1 = GamePlayer('player1')
	 	player2 = GamePlayer('player2')

	 	players = [player1, player2]

		self.game_model = GameModel(players)

	def test_letter_bucket_creation(self):
		tiles = self.game_model.tiles
		self.assertEqual(len(tiles), 144)
		cloned_tiles = deepcopy(tiles)
		cloned_tiles.sort()
		self.assertNotEqual(cloned_tiles, tiles)

	
	def test_player_setups(self):
		players = self.game_model.players
		number_of_players = len(players)

		if number_of_players < 5:
			tiles_per_person = 21

		elif number_of_players < 7:
			tiles_per_person = 15

		elif number_of_players > 6:
			tiles_per_person = 11

		for player in self.game_model.players:
			self.assertEqual(len(player.tiles), tiles_per_person)




if __name__ == '__main__':
	unittest.main()



