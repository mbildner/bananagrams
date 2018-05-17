LETTER_COUNT = { 'a' => 13, 'b' => 3, 'c' => 3, 'd' => 6, 'e' => 18, 'f' => 3, 'g' => 4, 'h' => 3, 'i' => 12, 'j' => 2, 'k' => 2, 'l' => 5, 'm' => 3, 'n' => 8, 'o' => 11, 'p' => 3, 'q' => 2, 'r' => 9, 's' => 6, 't' => 9, 'u' => 6, 'v' => 3, 'w' => 3, 'x' => 2, 'y' => 3, 'z' => 2 }

class GameOver < Exception; end

class TileBag
  attr_reader :tiles

  def initialize
    @tiles = LETTER_COUNT.inject([]) do |coll, (letter, count)|
      coll + count.times.map { letter }
    end

    @tiles = @tiles.shuffle
  end

  def empty?
    tiles.empty?
  end

  def can_take?(n)
    tiles.count >= n
  end

  def take(n)
    raise GameOver unless can_take?(n)

    tiles.pop(n)
  end
end


# f     t
# r     a
# e     l
# s     l
# h e l l o
  # l
  # e
  # p
  # h
  # a
  # n
  # t


class Board
  attr_reader :board

  EMPTY_CELL_VALUE = nil

  def initialize(size)
    @board = size.times.map do
      size.times.map {
        EMPTY_CELL_VALUE
      }
    end
  end
end

class Player
  attr_reader :cards

  def initialize(cards)
    @cards = cards
  end
end




