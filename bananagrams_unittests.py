import unittest
from Bananagrams import GameModel, GamePlayer

from copy import deepcopy


import random

class TestInitializeGameFunction(unittest.TestCase):
	def setUp(self):
	 	player1 = GamePlayer('player1')
	 	player2 = GamePlayer('player2')

	 	players = [player1, player2]
		self.game_model = GameModel(players)
		self.player1 = self.game_model.players[0]

	def test_letter_bucket_creation(self):
		tiles = self.game_model.tiles

		self.assertEqual(len(tiles), 144)

		cloned_tiles = deepcopy(tiles)
		cloned_tiles.sort()
		self.assertNotEqual(cloned_tiles, tiles)

	
	def test_player_setups(self):
		self.game_model.start_game()

		for player in self.game_model.players:
			self.assertEqual(len(player.tiles), self.game_model.tiles_per_person)


	def test_give_player_tiles(self):
		player2 = self.game_model.players[1]

		player1_tile_count = len(self.player1.tiles)
		player2_tile_count = len(player2.tiles)

		extra_tiles = random.randint(1, len(self.game_model.tiles))

		self.game_model.give_player_tiles(extra_tiles, self.player1)
		self.assertEqual(extra_tiles, (len(self.player1.tiles) - player1_tile_count))


	def test_start_game(self):
		self.assertFalse(self.game_model.game_running)
		self.game_model.start_game()
		self.assertTrue(self.game_model.game_running)


class TestGamePlayFunction(unittest.TestCase):
	def setUp(self):
	 	player1 = GamePlayer('player1')
	 	player2 = GamePlayer('player2')

	 	players = [player1, player2]
		self.game_model = GameModel(players)
		self.player1 = self.game_model.players[0]

		self.game_model.start_game()

	def test_return_tiles(self):
		


		player1_tile_count = len(self.player1.tiles)

		game_tile_count = self.game_model.get_number_of_tiles()

		# randomize this?
		tiles_to_return = self.player1.tiles[0:4]

		self.game_model.return_tiles(tiles_to_return, self.player1)
		
		self.assertEquals(game_tile_count + len(tiles_to_return), self.game_model.get_number_of_tiles())
		self.assertEquals(player1_tile_count - len(self.player1.tiles), len(tiles_to_return))


	def test_dump_success(self):
		self.game_model.start_game()
		player1_tile_count = len(self.player1.tiles)
		game_tile_count = self.game_model.get_number_of_tiles()

		dump_succeeded = self.game_model.dump(self.player1.tiles[0], self.player1)
		
		self.assertEquals(game_tile_count - 2, self.game_model.get_number_of_tiles())
		self.assertEquals(len(self.player1.tiles) - player1_tile_count, 2)
		self.assertTrue(dump_succeeded)


	def test_dump_failure(self):
		self.game_model.start_game()
		self.game_model.give_player_tiles(self.game_model.get_number_of_tiles() - 1, self.player1)
		player1_tile_count = len(self.player1.tiles)
		game_tile_count = self.game_model.get_number_of_tiles()

		dump_succeeded = self.game_model.dump(self.player1.tiles[0], self.player1)

		self.assertEquals(game_tile_count, self.game_model.get_number_of_tiles())
		self.assertEquals(len(self.player1.tiles), player1_tile_count)
		self.assertFalse(dump_succeeded)

	# def test_peel_midgame(self):
	# 	self.game_model.start_game()
	# 	player1_tile_count = len(self.player1.tiles)
	# 	game_tile_count = self.game_model.get_number_of_tiles()


	# 	self.game_model.peel(self.player1)









if __name__ == '__main__':
	unittest.main()



