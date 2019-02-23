#!/usr/bin/env python3

"""Text generators from a JSON dictionary.

This module contains a list of generators for text using a properly formatted
JSON dictionary along with a few helper functions.

TODO:
    * Describe the JSON dictionary structure in the module docstring.
    * Create a Dictionary class to simplify access.
    * Create numbers, tenses, special verb type enums.

Authors:
    Eli W. Hunter
"""

import argparse
import sys

import random
import json

VOWELS = ('a', 'e', 'i', 'o', 'u')
NUMBERS = ('singular', 'plural')
TENSES = ('future', 'present', 'past')
WEIGHTED_TENSES = ('future', 'present', 'present', 'present', 'past', 'past')


def capitalize(string):
    """Capitalize the first letter of the string, ignoring others.

    This exists to prevent .capitalize() from lowercasing characters that
    should be capitalized.

    Args:
        string (str): The string to be capitalized.

    Args:
        str: The capitalized string.
    """
    return "%s%s" % (string[0].upper(), string[1:])


def _get_noun(dictionary, number):
    """Get a random noun from a dictionary with nouns.

    Args:
        dictionary (dict): A dictionary of words, containing nouns.
        number (str): The grammatical number of a word as a string.

    Returns:
        str: The noun that has been randomly chosen from the dictionary
            separated by a single space.
    """
    noun = random.choice(dictionary['nouns'])[number]
    return noun


def _get_adjectives(dictionary, n):
    """Make a string of unique adjectives from the dictionary.

    Args:
        dictionary (dict): A dictionary of words, containing adjectives.
        n (int): The number of adjectives to string together.

    Returns:
        str: The string of unique adjectives selected from the dictionary.

    Raises:
        ValueError: If the given n is less than 0 or larger than the length of
            the set of words.
    """
    if n < 0:
        raise TypeError('n must be non-negative')
    if n > len(dictionary['adjectives']):
        raise TypeError('n cannot be greater than the number of adjectives in \
                        the dictionary')

    adjectives = []
    while len(adjectives) < n:
        choice = random.choice(dictionary['adjectives'])
        if choice not in adjectives:
            adjectives.append(choice)

    string = ''
    for adjective in adjectives:
        string += ', ' + adjective
    return string[2:]  # Remove the first comma and spacing


def _get_article(dictionary, number, suffix_type):
    """Get an random article from a dictionary with articles.

    Args:
        dictionary (dict): A dictionary of words, containing articles.
        number (str): The grammatical number of a word as a string.
        suffix_type (str): The suffix type of the article. (e.g. vowel or
            normal)

    Returns:
        str: The article that has been randomly chosen from the articles in the
            dicitonary of the given number and suffix type.
    """
    article = random.choice(dictionary['articles'])[number][suffix_type]
    return article


def _get_special_verb(dictionary, number, tense, verb_type):
    """Get a special verb from a dictionary with special verbs.

    Args:
        dictionary (dict): A dictionary of words, containing special verbs.
        number (str): The grammatical number of a word as a string.
        tense (str): The grammatical tense of a verb as a string.
    """
    verb = dictionary['special_verbs'][verb_type][tense][number]
    return verb


def _get_verb(dictionary, number, tense, transitivity):
    """Get a random verb from a dictionary with verbs.

    Each verb has multiple different forms that are weighted based on how much
    they "naturally" occur in speech. This weighting is opinionated.

    Args:
        dictionary (dict): A dictionary of words, containing verbs.
        number (str): The grammatical number of a word as a string.
        tense (str): The grammatical tense of a verb as a string.
    """
    verb = random.choice(dictionary['verbs'][transitivity])

    # To weight a verb form in the list, it is added more times. That is, it is
    # added more times if it is "common" and fewer times if it is "uncommon"
    forms = list()

    # Participle form: is/was/will be + participle
    participle_form = \
        _combine_strings(_get_special_verb(dictionary, number, tense, 'linking'),
                         verb['participle']['present'])
    forms += 3 * [participle_form]
    # Declarative form: do/does/did + simple singular present
    declarative_form = \
        _combine_strings(_get_special_verb(dictionary, number, tense, 'declarative'),
                         verb['simple']['plural'])
    forms += 2 * [declarative_form]

    if tense == 'present':
        # Simple present: simple_present
        simple_present = verb['simple'][number]
        forms += 3 * [simple_present]

    elif tense == 'future':
        # Simple future: will + simple present
        will_form = _combine_strings('will', verb['simple']['plural'])
        forms += 3 * [will_form]
        # Simple future: shall + simple present
        shall_form = _combine_strings('shall', verb['simple']['plural'])
        forms += 1 * [shall_form]

    elif tense == 'past':
        # Simple past: simple past
        simple_past = verb['simple']['past']
        forms += 3 * [simple_past]
        # Future perfect: will have + simple present verb
        future_perfect = \
            _combine_strings(_get_special_verb(dictionary, number, 'future', 'possessive'),
                             verb['simple']['past'])
        forms += 1 * [future_perfect]
        # Present perfect: has/have + simple present verb
        present_perfect = \
            _combine_strings(_get_special_verb(dictionary, number, 'present', 'possessive'),
                             verb['simple']['past'])
        forms += 3 * [present_perfect]
        # Pluperfect: had + simple present verb
        pluperfect = \
            _combine_strings(_get_special_verb(dictionary, number, 'past', 'possessive'),
                             verb['simple']['past'])
        forms += 2 * [pluperfect]

    chosen_form = random.choice(forms)

    return chosen_form


def _get_full_noun(dictionary, number, number_of_adjectives):
    """Get a noun with an article and adjectives from a dictionary.

    Args:
        dictionary (dict): A dictionary of words, containing nouns, adjectives,
            and articles.
        number (str): The grammatical number of a word as a string.
        number_of_adjectives (int): The number of adjectives to for the full
            noun.

    Returns:
        str: A random, fully described noun consisting of a random noun with a
            the given number of adjectives and a random article.
    """
    noun = _get_noun(dictionary, number)
    adjectives = _get_adjectives(dictionary, number_of_adjectives)
    # Temporary word to figure out the correct article
    word = _combine_strings(adjectives, noun)
    suffix_type = ''
    if word[0].lower() in VOWELS:
        suffix_type = 'vowel'
    else:
        suffix_type = 'normal'
    article = _get_article(dictionary, number, suffix_type)

    word = _combine_strings(article, word)
    return word


def _combine_strings(*strings):
    """Combine a list of strings into a single string.

    Each string, if it is not empty, is added to the string separated by a
    space in the same order as given.

    Args:
        *strings (str): The list of strings to be combined into one.

    Returns:
        The string formed from combining all given strings.
    """
    combined = ''
    for string in strings:
        if len(string) != 0:
            combined += string + ' '
    return combined.rstrip()  # Remove the last trailing space


def word(dictionary_filepath, max_adjectives=2):
    """Generate words with adjectives.

    This acts partially like a wrapper around _get_full_noun().

    Args:
        dictionary_filepath (str): A valid filepath to a properly formatted
            JSON dictionary.
        max_adjectives (int, optional): A maximum number of adjectives
            for the word to have. Defaults to 3.

    Yields:
        str: A random word consisting of a noun with a random number of
            adjectives from 0 to the given max.

    Raises:
        FileNotFoundError: If any specified file does not exist.
    """
    while True:
        file = open(dictionary_filepath)
        dictionary = json.load(file)
        file.close()

        number_of_adjectives = random.randint(0, max_adjectives)
        number = random.choice(NUMBERS)
        word = _get_full_noun(dictionary, number, number_of_adjectives)

        del(dictionary)

        yield word


def simple_sentence(dictionary_filepath, max_adjectives=2):
    """Generate a simple sentence.

    Args:
        dictionary_filepath (str): A valid filepath to a properly formatted
            JSON dictionary.
        max_adjectives (int, optional): A maximum number of adjectives
            for the word to have. Defaults to 3.

    Yields:
        str: A random word consisting of a noun with a random number of
            adjectives from 0 to the given max.

    Raises:
        FileNotFoundError: If any specified file does not exist.
    """
    while True:
        file = open(dictionary_filepath)
        dictionary = json.load(file)
        file.close()

        subject_number_of_adjectives = random.randint(0, max_adjectives)
        subject_number = random.choice(NUMBERS)
        subject = _get_full_noun(dictionary, subject_number,
                                 subject_number_of_adjectives)

        transitivity = random.choice(['transitive', 'intransitive'])
        tense = random.choice(WEIGHTED_TENSES)
        verb = _get_verb(dictionary, subject_number, tense, transitivity)

        complement = ''
        if transitivity == 'transitive':
            complement_number_of_adjectives = random.randint(0, max_adjectives)
            complement_number = random.choice(NUMBERS)
            complement = _get_full_noun(dictionary, complement_number,
                                        complement_number_of_adjectives)

        sentence = _combine_strings(subject, verb, complement)
        sentence += '.'

        del(dictionary)

        yield capitalize(sentence)


if __name__ == '__main__':
    # sys.argv is of the form `generator.py [options] DICTIONARY_FILEPATH `

    # Argument Setup
    parser = argparse.ArgumentParser(
        description='A command line interface for text_generator module')
    parser.add_argument('dictionary_filepath',
                        help='path to the JSON dictionary')
    parser.add_argument('-n', '--number', default=1, type=int,
                        help='number of random strings to generate (default: 1)')
    parser.add_argument('-p', '--perpetual', action='store_true',
                        help='whether to create words perpetually')
    parser.add_argument('-w', '--word', action='append_const',
                        dest='generators', const=word,
                        help='add a word generator to the list of the possible generators')
    parser.add_argument('-s', '--simple-sentence', action='append_const',
                        dest='generators', const=simple_sentence,
                        help='add a simple sentence generator to the list of the possible generators')
    parser.add_argument('-a', '--all', action='store_const',
                        dest='generators', const=[word, simple_sentence],
                        help='add a all possile generators to the list of the possible generators')
    args = parser.parse_args()
    # These 'aliases' of sort simply clean up the usage of arguments
    generators = args.generators
    number_to_generate = args.number
    dictionary_filepath = args.dictionary_filepath

    # Error Checking
    if not generators:
        print('At least one generator must be specified')
        sys.exit(2)
    if number_to_generate < 0:
        print('A negative number of items cannot be specified')
        sys.exit(3)
    if dictionary_filepath is None:
        print('A dictionary filepath must be specified')
        sys.exit(4)

    # Create all text generators
    # This is done so that the dictionary_filepath can be detected at the same
    # time as all other args
    for i in range(len(generators)):
        generators[i] = generators[i](dictionary_filepath)

    # Output Text
    if args.perpetual:
        while True:
            print(next(random.choice(generators)))
    else:
        for _ in range(number_to_generate):
            print(next(random.choice(generators)))
