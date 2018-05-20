class Bag
  LETTER_COUNT = { 'a' => 13, 'b' => 3, 'c' => 3, 'd' => 6, 'e' => 18, 'f' => 3, 'g' => 4, 'h' => 3, 'i' => 12, 'j' => 2, 'k' => 2, 'l' => 5, 'm' => 3, 'n' => 8, 'o' => 11, 'p' => 3, 'q' => 2, 'r' => 9, 's' => 6, 't' => 9, 'u' => 6, 'v' => 3, 'w' => 3, 'x' => 2, 'y' => 3, 'z' => 2 }
  DUMP_TILE_REPLACEMENT_COUNT = 3

  class NotEnoughTilesForDump < Exception; end

  attr_reader :tiles

  def initialize
    @tiles = LETTER_COUNT.inject([]) do |coll, (letter, count)|
      coll + count.times.map { letter }
    end

    @tiles = @tiles.shuffle
  end

  def dump(tile)
    raise NotEnoughTilesForDump unless can_take?(DUMP_TILE_REPLACEMENT_COUNT)

    take(3)
  end

  def empty?
    tiles.empty?
  end

  def can_take?(n)
    tiles.count >= n
  end

  def take(n)
    tiles.pop(n)
  end
end

