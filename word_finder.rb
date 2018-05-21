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
