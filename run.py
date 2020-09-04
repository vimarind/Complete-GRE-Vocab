from core.api.OxfordAPI import OxfordAPI
from core.api.WordsAPI import WordsAPI
from core.core import load_vocabulary, populate_words, write_to_tsv, write_incomplete_words
import secrets

oxford_api = OxfordAPI(secrets.oxford_app_id, secrets.oxford_app_key, 'cache/')
words_api = WordsAPI(secrets.words_api_key)

words = load_vocabulary('input/vince_list.csv')
incomplete_words = populate_words(words, oxford_api, words_api)
write_to_tsv(words, 'output/deck.tsv')
write_incomplete_words(incomplete_words, 'output/incomplete_words.txt')
