require 'rest-client'
require 'json'

PEARSON_APP_ID=ENV.fetch('PEARSON_APP_ID')
PEARSON_API_KEY=ENV.fetch('PEARSON_API_KEY')

class PearsonDictionary
  CACHE_FILE_NAME = '.dict.json'
  attr_reader :app_id, :api_key

  def initialize(app_id, api_key)
    @app_id = app_id
    @api_key = api_key

    File.write(CACHE_FILE_NAME, "{}") unless File.exist?(CACHE_FILE_NAME)
  end

  def read_cache
    JSON.parse(File.read(CACHE_FILE_NAME))
  end

  def save_cache(cache)
    File.write(CACHE_FILE_NAME, cache.to_json)
  end

  def headers
    @_headers ||= {
      'app_id' => app_id,
      'app_key' => api_key
    }
  end

  def url(word)
    "http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=#{word}"
  end

  def check_api(word)
    response = RestClient.get(
      url(word),
      headers
    )

    results = JSON.parse(response)

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


