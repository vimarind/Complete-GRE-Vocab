from core.Word import Word
import json
import requests
from os import path
from PyDictionary import PyDictionary


class OxfordAPI:

    def __init__(self, app_id, app_key, cache_path):
        self.app_id = app_id
        self.app_key = app_key
        self.cache_path = cache_path

    def __parse_sense(self, word, sense):
        for definition in sense.get('definitions', list()):
            word.definitions.append(definition)
        for example in sense.get('examples', list()):
            word.examples.append(example.get('text', None))
        for synonym in sense.get('synonyms', list()):
            word.synonyms.append(synonym.get('text', None))
        for subsense in sense.get('subsenses', list()):
            self.__parse_sense(word, subsense)
            # for definition in subsense.get('definitions', list()):
            #     word.definitions.append(definition)
            # for example in subsense.get('examples', list()):
            #     word.examples.append(example.get('text', None))
            # for synonym in subsense.get('synonyms', list()):
            #     word.synonyms.append(synonym.get('text', None))

    def __parse_pronunciation(self, word, pronunciation):
        audioFile = pronunciation.get('audioFile', None)
        if audioFile is not None:
            word.audio_file = audioFile

    def __parse_entry(self, word, entry):
        for pronunciation in entry.get('pronunciations', list()):
            self.__parse_pronunciation(word, pronunciation)
        for sense in entry.get('senses', list()):
            self.__parse_sense(word, sense)

    def __parse_lexical_entry(self, word, lexical_entry):
        for entry in lexical_entry.get('entries', list()):
            self.__parse_entry(word, entry)

    def __parse_result(self, word, result):
        for lexical_entry in result.get('lexicalEntries', list()):
            self.__parse_lexical_entry(word, lexical_entry)

    def __parse_word(self, word, data):
        success = False
        if data.get('error') is None:
            for result in data.get('results', list()):
                self.__parse_result(word, result)
            success = True
        return success

    def __get_word_data(self, word):
        filepath = self.cache_path + word.text + '.json'
        with open(filepath, 'w') as file:
            url = "https://od-api.oxforddictionaries.com/api/v2/words/en-us?q=" + word.text
            r = requests.get(url, headers={"app_id": self.app_id, "app_key": self.app_key})
            file.write(r.text)
        return r.json()

    def get_word(self, word):
        """
        Populates the given word object with the relevant information from the Oxford Dictionary API
        (cached json files).
        :param word: The word object to be requested.
        :return:
        """
        success = False
        if path.exists(self.cache_path):
            filepath = self.cache_path + word.text + '.json'
            if path.exists(filepath):
                with open(filepath, 'r') as file:
                    data = json.load(file)
            else:
                data = self.__get_word_data(word)
            success = self.__parse_word(word, data)
        else:
            print('OxfordAPI: Please provide a valid cache path.')
        return success

    def load_words_jsons_oxford(self, words):
        """
        Populates the folder containing the cached json files, for easier retrieval.
        :param words: The list of word objects.
        :param app_id: Oxford API id authentication.
        :param app_key: Oxford API key authentication.
        :return: Nothing.
        """
        i = 0
        for word in words:
            print(str(i) + ': ' + word.text)
            i = i + 1
            with open(self.cache_path + word.text + '.json', 'w') as file:
                url = "https://od-api.oxforddictionaries.com/api/v2/words/en-us?q=" + word.text
                r = requests.get(url, headers={"app_id": self.app_id, "app_key": self.app_key})
                file.write(r.text)



