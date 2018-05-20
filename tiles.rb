require 'json'
require 'set'

class Dictionary
  def initialize
  end

  def confirm(word)
    [
      'apple',
      'eat',
      'eats',
      'reads'
    ].include? word
  end
end

class WordFinder
  attr_reader :grid

  def initialize(grid)
    @grid = grid
  end

  def reduce_group(group, i, transposed)
    group.each_with_index.reduce([]) do |coll, (square, j)|
      if square == nil && coll.last != nil
        # end of a word
        coll << []
        coll
      elsif square == nil && coll.last == nil
        # beginning of the row
        coll << []
        coll

      elsif square != nil && coll.last != nil
        row_index, col_index = transposed ? [j, i] : [i, j]

        coll.last << { letter: square, row: row_index, column: col_index }
        coll

      elsif square != nil && coll.last == nil
        row_index, col_index = transposed ? [j, i] : [i, j]

        coll << [{ letter: square, row: row_index, column: col_index }]
        coll
      end
    end
  end

  def all_tile_groups
    in_place = grid.each_with_index.reduce([]) do |coll, (row, row_index)|
      coll + reduce_group(row, row_index, false)
    end

    transposed = grid.transpose.each_with_index.reduce([]) do |coll, (column, column_index)|
      coll + reduce_group(column, column_index, true)
    end

    in_place + transposed
  end

  def two_or_more
    all_tile_groups
      .select { |group| group.length > 1 }
  end

  def words(with_metadata=false)
    two_or_more.map do |word|
      with_metadata ? word : word.reduce('') { |w, tile| w + tile[:letter] }
    end
  end

  def consistent_shape?
    row_count = grid.size

    grid.all? { |row| row.size == row_count }
  end
end

class Board
  class InvalidTileLocation < Exception; end
  class InvalidTileContents < Exception; end

  VALID_LETTERS=%w|a b c d e f g h i j k l m n o p q r s t u v w x y z|

  def self.parse(board)
    grid = board.split("\n")
      .map do |row|
      row.split("")
        .reject { |l | l == ' ' }
        .map { |l| l == '.' ? nil : l }
    end

    Board.new(grid)
  end

  attr_reader :grid, :dictionary

  def initialize(grid, dictionary=Dictionary.new)
    @grid = grid
    @dictionary = dictionary
  end

  def all_letters
    grid.flatten.compact
  end

  def valid?
    valid_shape? && valid_words?
  end

  def words
    WordFinder.new(grid).words
  end

  def add(letter, row, column)
    raise InvalidTileLocation.new("row: #{row} column: #{column} is out of bounds") unless in_bounds?(row, column)
    raise InvalidTileContents.new("'#{letter}' is not valid, see rules") unless valid_tile_contents?(letter)

    existing = at(row, column)

    grid[row][column] = letter

    existing
  end

  private

  def valid_tile_contents?(letter)
    VALID_LETTERS.include? letter
  end

  def valid_words?
    words.all? { |word| dictionary.confirm(word) }
  end

  def valid_shape?
    all_letters.size == first_tree.size
  end

  def first_tree
    walk_tree(*first)
  end

  def in_bounds?(row, col)
    row >= 0 && row < grid.length && col >= 0 && col < grid.first.length
  end

  def neighbors(r, c)
    if r == 0
      top = nil
      bottom = [r + 1, c]
    elsif r == grid.length - 1
      top = [r - 1, c]
      bottom = nil
    else
      top = [r - 1, c]
      bottom = [r + 1, c]
    end

    if c == 0
      left = nil
      right = [r, c + 1]
    elsif c == grid.first.length - 1
      right = nil
      left = [r, c - 1]
    else
      right = [r, c + 1]
      left = [r, c - 1]
    end

    [
      left, right, top, bottom
    ].compact
  end

  def at(row, col)
    grid[row][col]
  end

  def first
    grid.length.times do |r|
      grid[r].length.times do |c|
        tile = at(r, c)

        return [r, c] if tile
      end
    end
  end

  def walk_tree(start_row, start_col)
    checked = [[start_row, start_col]].to_set
    found = [[start_row, start_col]].to_set

    to_check = neighbors(start_row, start_col).to_set

    until to_check.empty?
      to_check = to_check.reduce(Set.new) do |coll, (row, col)|
        if at(row, col)
          neighbors(row, col).each { |pair|
            coll << pair
          }

          coll.add([row, col])
          found.add([row, col])
        end

        checked.add([row, col])

        coll
      end

      to_check = to_check - checked
    end

    found
  end
end


invalid_example = <<-INVALID_EXAMPLE
e . . . .
q . . . e
a b c d e
. . . . w
e . e . f
. . g . g
. . e . .
. . t p p
. . t . .
INVALID_EXAMPLE

board = Board.parse(invalid_example)

puts board.valid?

valid_example = <<-VALID_EXAMPLE
. . . . .
e . . . r
a p p l e
t . . . a
. . . . d
. . . . s
. . . . .
. . . . .
. . . . .
VALID_EXAMPLE

board = Board.parse(valid_example)

puts board.valid?

board.add('s', 4, 0)

puts board.valid?
