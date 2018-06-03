require 'rest-client'
require 'json'

class PearsonDictionary
  CACHE_FILE_NAME = '.dict.json'

  def initialize
    File.write(CACHE_FILE_NAME, "{}") unless File.exist?(CACHE_FILE_NAME)
  end

  def read_cache
    JSON.parse(File.read(CACHE_FILE_NAME))
  end

  def save_cache(cache)
    File.write(CACHE_FILE_NAME, cache.to_json)
  end

  def headers
    {}
  end

  def url(word)
    "http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=#{word}"
  end

  def check_api(word)
    response = RestClient.get(
      url(word),
      headers
    )

    results = JSON.parse(response)['results']

    !results.empty?
  end

  def confirm(word)
    cache = read_cache

    if cache.include?(word)
      return cache[word]
    end

    result = check_api(word)

    cache[word] = result

    save_cache(cache)

    result
  end
end


