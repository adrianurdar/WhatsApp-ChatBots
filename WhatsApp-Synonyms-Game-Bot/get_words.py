import requests
import random
import os


def get_word():
    # Get a list of random words
    common_words_url = "https://raw.githubusercontent.com/dariusk/corpora/master/data/words/common.json"
    res = requests.get(common_words_url)
    common_words = res.json()['commonWords']

    # Select a random word from the common_words list
    random_word = random.choice(common_words)

    # Setup for MW API call
    mw_api_key = os.environ["MW_API_KEY"]
    mw_endpoint = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
    params = {
        "key": mw_api_key,
    }

    # Get the synonyms from the MW API
    res = requests.get(url=mw_endpoint + random_word, params=params)
    res.raise_for_status()
    synonyms = res.json()[0]["meta"]["syns"][0]
    print(synonyms)

    return random_word, synonyms


if __name__ == "__main__":
    get_word()
