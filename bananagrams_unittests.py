import unittest
from Bananagrams import GameModel, GamePlayer, WordDictionary

from copy import deepcopy
import random


class TestWordDictionaryClass(unittest.TestCase):
	def setUp(self):
		self.word_dict = WordDictionary("/usr/share/dict/words")

	def test_multiple_word_validation(self):
		test_word_list = ["clean", "dirty", "test", "self", "python"]
		test_return_boolean = self.word_dict.are_valid_words(test_word_list)
		self.assertTrue(test_return_boolean)

		test_word_list = ["California", "dirty", "test", "self", "python"]
		test_return_boolean = self.word_dict.are_valid_words(test_word_list)
		self.assertFalse(test_return_boolean)

		test_word_list = ["fasdf", "efauwfads", "test", "self", "python"]
		test_return_boolean = self.word_dict.are_valid_words(test_word_list)
		self.assertFalse(test_return_boolean)

		test_word_list = ["hello", "world", "sound", "good"]
		test_return_boolean = self.word_dict.are_valid_words(test_word_list)
		self.assertTrue(test_return_boolean)

	def test_single_word_validation(self):
		self.assertTrue(self.word_dict.is_valid_word("table"), True)
		self.assertTrue(self.word_dict.is_valid_word("chair"), True)
		self.assertTrue(self.word_dict.is_valid_word("eat"), True)

		self.assertFalse(self.word_dict.is_valid_word("fdsafds"), False)
		self.assertFalse(self.word_dict.is_valid_word("Gregory"), False)
		self.assertFalse(self.word_dict.is_valid_word("good idea"), False)
		self.assertFalse(self.word_dict.is_valid_word(23), False)
		self.assertFalse(self.word_dict.is_valid_word(""), False)


class TestInitializeGameFunction(unittest.TestCase):
	def setUp(self):
	 	player1 = GamePlayer('player1')
	 	player2 = GamePlayer('player2')
	 	players = [player1, player2]
		word_dict = WordDictionary("/usr/share/dict/words")
		self.game_model = GameModel(players, word_dict)
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


class TestGameEndFunction(unittest.TestCase):
	def setUp(self):
	 	player1 = GamePlayer('player1')
	 	player2 = GamePlayer('player2')

	 	players = [player1, player2]

	 	word_dict = WordDictionary("/usr/share/dict/words")
	 	self.game_model = GameModel(players, word_dict)

		self.player1 = self.game_model.players[0]
		self.player2 = self.game_model.players[1]
		self.number_of_players = len(self.game_model.players)

		self.game_model.start_game()

		self.init_player1_tile_count = self.player1.get_tile_count()
		self.init_player2_tile_count = self.player2.get_tile_count()
		self.init_game_tile_count = self.game_model.get_tile_count()

		while self.game_model.enough_tiles_for_peel():
			self.game_model.peel(random.choice(players))


	def test_winning_peel(self):
		players = self.game_model.players
		players[0].words = ["hello", "good", "sound", "interest", "thing"]
		players[1].words = ["friend", "sound", "interest", "thing"]
		ending_game_player = random.choice(players)
		self.game_model.peel(ending_game_player)
		self.assertEqual(ending_game_player, self.game_model.winning_player)


	def test_losing_peel(self):
		players = self.game_model.players
		players[0].words = ["hello", "good", "sound", "interest", "thing"]
		players[1].words = ["Moshe", "FDFS", 12]
		
		while self.game_model.enough_tiles_for_peel():
			self.game_model.peel(random.choice(players))

		self.game_model.peel(players[1])
		self.assertEquals(self.game_model.winning_player, players[0])


	# a single losing player is likely to make the other player win, be careful with this function


class TestGamePlayFunction(unittest.TestCase):
	def setUp(self):
	 	player1 = GamePlayer('player1')
	 	player2 = GamePlayer('player2')

	 	players = [player1, player2]

	 	word_dict = WordDictionary("/usr/share/dict/words")
	 	self.game_model = GameModel(players, word_dict)

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

	def test_peel_midgame(self):
		self.game_model.peel(self.player1)
		self.assertEquals( self.player1.get_tile_count() - self.init_player1_tile_count, 1)
		self.assertEquals( self.player2.get_tile_count() - self.init_player2_tile_count, 1)
		self.assertEquals( self.init_game_tile_count - self.game_model.get_tile_count(), self.number_of_players )

	# def test_peel_win(self):
	# 	while self.game_model.enough_tiles_for_peel():
	# 		self.game_model.peel(self.player1)
	# 	self.game_model.peel(self.player1)
	# 	self.assertFalse(self.game_model.game_running)
		

if __name__ == '__main__':
	unittest.main()
