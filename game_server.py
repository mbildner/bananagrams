from tornado import websocket, web, ioloop
import json
from Bananagrams import GameModel, GamePlayer, WordDictionary
from random import choice

def random_string(length):
	return "".join([choice("0123456789abcdefghijklmnopqrstuvwxyz") for n in range(length)])


players_online = {}

server_id = random_string(10)

def request_game_state():
	return {
		'description': 'boardState',
		'payload':"A B C D E\nF G H I J\nK L M N O"  
	}


class IndexHandler(web.RequestHandler):
	def get(self):
		if not self.get_cookie("user_id"):
			self.set_cookie("user_id", random_string(10))

		self.render('index.html')


class WebSocketHandler(websocket.WebSocketHandler):
	def open(self):
		print self.get_cookie("user_id")
		self.write_message("HI FRIEND")

	def on_close(self):
		print "websocket closed"

	def on_message(self, message):
		if message == "request_game_state":
			self.write_message(json.dumps(request_game_state()))

app = web.Application([
	(r'/', IndexHandler),
	(r'/ws', WebSocketHandler)
	])

if __name__ == '__main__':
	app.listen(8000)
	ioloop.IOLoop.instance().start()