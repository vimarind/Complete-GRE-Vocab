from core.Word import Word

import csv, random


def __safe_list_get(l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default


def load_vocabulary(filename):
    """
    Reads the words from the given csv and generates a dictionary of words for easier processing.
    :param filename: The name of the file to load the vocabulary from.
    :return: The dictionary where the key is the text of the word and the value the Word object itself.
    """
    tags = ['vince', 'gregmat', 'magoosh', 'manhattan', 'prep_scholar', 'powerscore', 'greenlight_basic',
            'greenlight_advanced']
    words = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            row = row[1:]
            for i in range(len(row)):
                word_text = row[i]
                if word_text is not '':
                    word = words.get(word_text, None)
                    if word is None:
                        word = Word(word_text)
                        words[word_text] = word
                    word.tags.append(tags[i])
                    word.rank += 1
        random.seed(123456789)
        random_words_list = list(words.items())
        random.shuffle(random_words_list)
        random_words = dict(random_words_list)
        words = dict(sorted(random_words.items(), key=lambda x: x[1].rank, reverse=True))
    return words


def populate_words(words, oxford_api, words_api=None, allow_messages=True):
    """
    Iterates the words dictionary, populating the data of each object using the OxfordAPI and with the optional
    WordsAPI to be used in the case the word is not found in the Oxford dictionary.
    :param words: The dictionary containing the words to be populated.
    :param oxford_api: The OxfordAPI object.
    :param words_api: The WordsAPI object.
    :param allow_messages: Boolean value to indicate if messages should be displayed in the console.
    :return: A list of those words that have not been found.
    """
    incomplete_words = []
    i = 0
    for word in words.values():
        if allow_messages:
            print(i, ': ', word.text)
            i = i + 1
        success = oxford_api.get_word(word)
        if not success and words_api:
            definitions = words_api.definitions(word.text)
            if definitions and definitions.get('definitions', False):
                for definition in definitions.get('definitions', list()):
                    word.definitions.append(definition.get('definition', None))
    for item in words.items():
        key = item[0]
        word = item[1]
        if len(word.definitions) == 0:
            incomplete_words.append(key)
    return incomplete_words


def write_to_tsv(words, filename):
    """
    Writes the list of words to a file in the format of a Tab Separated Values (TSV).
    :param words: The list of words to be saved.
    :param filename: The name of the file to be written.
    """
    with open(filename, 'wt') as file:
        tsv_writer = csv.writer(file, delimiter='\t')
        for word in words.values():
            row = [word.text, __safe_list_get(word.definitions, 0, ' ')]
            for example in word.examples[:5]:
                row.append(example)
            for _ in range(5 - len(word.examples)):
                row.append(' ')
            row.append(', '.join(word.synonyms))
            if word.synonyms == 0:
                row.append(' ')
            row.append(('[sound:' + word.text + '.mp3]') if word.audio_file is not '' else ' ')
            row.append(' '.join(word.tags) + ' rank_' + str(word.rank))
            tsv_writer.writerow(row)


def write_incomplete_words(incomplete_words, filename):
    """
    Write the list of incomplete words (those that do not have definitions) to a text file.
    :param incomplete_words: The array of word strings.
    :param filename: The name of the file to be written.
    """
    with open(filename, 'w') as file:
        for word in incomplete_words:
            file.write(word + '\n')



