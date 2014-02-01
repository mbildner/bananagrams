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

		player1_tile_count = self.player1.get_tile_count()
		player2_tile_count = len(player2.tiles)

		extra_tiles = random.randint(1, len(self.game_model.tiles))

		self.game_model.give_player_tiles(extra_tiles, self.player1)
		self.assertEqual(extra_tiles, (self.player1.get_tile_count() - player1_tile_count))


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
		self.player2 = self.game_model.players[1]
		self.number_of_players = len(self.game_model.players)

		self.game_model.start_game()

		self.init_player1_tile_count = self.player1.get_tile_count()
		self.init_player2_tile_count = self.player2.get_tile_count()
		self.init_game_tile_count = self.game_model.get_tile_count()



	def test_return_tiles(self):
		# randomize this?
		tiles_to_return = self.player1.tiles[0:4]

		self.game_model.return_tiles(tiles_to_return, self.player1)
		
		self.assertEquals(self.init_game_tile_count + len(tiles_to_return), self.game_model.get_tile_count())
		self.assertEquals(self.init_player1_tile_count - self.player1.get_tile_count(), len(tiles_to_return))


	def test_dump_success(self):
		dump_succeeded = self.game_model.dump(self.player1.tiles[0], self.player1)
		
		self.assertEquals(self.init_game_tile_count - 2, self.game_model.get_tile_count())
		self.assertEquals(self.player1.get_tile_count() - self.init_player1_tile_count, 2)
		self.assertTrue(dump_succeeded)


	def test_dump_failure(self):
		self.game_model.give_player_tiles(self.game_model.get_tile_count() - 1, self.player1)
		player1_tile_count = self.player1.get_tile_count()
		game_tile_count = self.game_model.get_tile_count()

		dump_succeeded = self.game_model.dump(self.player1.tiles[0], self.player1)

		self.assertEquals(game_tile_count, self.game_model.get_tile_count())
		self.assertEquals(self.player1.get_tile_count(), player1_tile_count)
		self.assertFalse(dump_succeeded)

	# def test_peel_midgame(self):
	# 	self.game_model.peel(self.player1)

	# 	self.assertEquals( self.player1.get_tile_count() - self.init_player1_tile_count, 1)
	# 	self.assertEquals( self.player2.get_tile_count() - self.init_player2_tile_count, 1)
	# 	self.assertEquals( self.init_game_tile_count - self.game_model.get_tile_count(), self.number_of_players )

	# def test_peel_endgame(self):
	# 	self.game_model.peel(self.player1)
	# 	while self.game_model.enough_tiles_for_peel():
	# 		self.game_model.peel(self.player1)
	# 	self.game_model.peel(self.player1)








if __name__ == '__main__':
	unittest.main()



