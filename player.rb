require 'set'
require './board'


class Player
  class NoPeelUnlessUserBagEmpty < Exception; end
  class NoBananasUnlessFinished < Exception; end
  class BoardAndBagTilesDoNotMatch < Exception; end

  attr_reader :name, :game, :bag, :board

  def initialize(name, game, bag, board)
    @name = name
    @game = game
    @bag = bag
    @board = board
  end

  def finished?
    bag.empty? && board.valid?
  end

  def adopt!(board)
    raise BoardAndBagTilesDoNotMatch unless correct_letters?(board)

    self.board = board
  end

  def correct_letters?(board)
    Set.new(board.all_letters) == Set.new(bag.tiles)
  end

  def peel!
    raise NoPeelUnlessUserBagEmpty unless bag.empty?
  end

  def bananas!
    raise NoBananasUnlessFinished unless finished?

    game.bananas!
  end

  def dump!(tile)

  end

end
