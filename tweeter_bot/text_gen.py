"""Text generators from a JSON dictionary.

This module contains a list of generators for text using a properly formatted
JSON dictionary along with a few helper functions.

TODO:
    * Describe the JSON dictionary structure in the Dictionary class docstring.
    * Create numbers, tenses, special verb type enums.
"""

import json
import random


class Dictionary:

    VOWELS = ("a", "e", "i", "o", "u")
    NUMBERS = ("singular", "plural")
    TENSES = ("future", "present", "past")
    WEIGHTED_TENSES = ("future", "present", "present", "present", "past", "past")

    @classmethod
    def from_json(cls, filepath):
        """Load dictionary from `filepath`.

        Args:
            filepath (str): Path of file to load. File must be properly
                formatted JSON.

        Returns:
            `Dictionary` constructed from dictionary loaded from `filepath` as
            JSON.
        """
        with open(filepath) as f:
            return cls(json.load(f))

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def _get_noun(self, number):
        """Get a random noun from a dictionary with nouns.

        Args:
            number (str): The grammatical number of a word as a string.

        Returns:
            str: The noun that has been randomly chosen from the dictionary
                separated by a single space.
        """
        noun_form = random.choice(self.dictionary["nouns"])
        return noun_form[number]

    def _get_adjectives(self, n):
        """Make a string of unique adjectives from the dictionary.

        Args:
            n (int): The number of adjectives to string together.

        Returns:
            str: The string of unique adjectives selected from the dictionary.

        Raises:
            ValueError: If the given n is less than 0 or larger than the length of
                the set of words.
        """
        adjectives = random.sample(self.dictionary["adjectives"], n)
        return ", ".join(adjectives)

    def _get_article(self, number, suffix_type):
        """Get an random article from a dictionary with articles.

        Args:
            number (str): The grammatical number of a word as a string.
            suffix_type (str): The suffix type of the article. (e.g. vowel or
                normal)

        Returns:
            str: The article that has been randomly chosen from the articles in the
                dicitonary of the given number and suffix type.
        """
        article_form = random.choice(self.dictionary["articles"])
        return article_form[number][suffix_type]

    def _get_special_verb(self, number, tense, verb_type):
        """Get a special verb from a dictionary with special verbs.

        Args:
            number (str): The grammatical number of a word as a string.
            tense (str): The grammatical tense of a verb as a string.
        """
        return self.dictionary["special_verbs"][verb_type][tense][number]

    def _get_verb(self, number, tense, transitivity):
        """Get a random verb from a dictionary with verbs.

        Each verb has multiple different forms that are weighted based on how much
        they "naturally" occur in speech. This weighting is opinionated.

        Args:
            number (str): The grammatical number of a word as a string.
            tense (str): The grammatical tense of a verb as a string.
            transitivity (str): Whether the verb is transitive or intransitive.
        """
        verb = random.choice(self.dictionary["verbs"][transitivity])

        # To weight a verb form in the list, it is added more times. That is, it is
        # added more times if it is "common" and fewer times if it is "uncommon"
        forms = []

        # Participle form: is/was/will be + participle
        participle_form = (
            self._get_special_verb(number, tense, "linking")
            + " "
            + verb["participle"]["present"]
        )
        forms += 3 * [participle_form]
        # Declarative form: do/does/did + simple singular present
        declarative_form = (
            self._get_special_verb(number, tense, "declarative")
            + " "
            + verb["simple"]["plural"]
        )
        forms += 2 * [declarative_form]

        if tense == "present":
            # Simple present: simple_present
            simple_present = verb["simple"][number]
            forms += 3 * [simple_present]

        elif tense == "future":
            # Simple future: will + simple present
            will_form = "will " + verb["simple"]["plural"]
            forms += 3 * [will_form]
            # Simple future: shall + simple present
            shall_form = "shall " + verb["simple"]["plural"]
            forms += 1 * [shall_form]

        elif tense == "past":
            # Simple past: simple past
            simple_past = verb["simple"]["past"]
            forms += 3 * [simple_past]
            # Future perfect: will have + simple present verb
            future_perfect = (
                self._get_special_verb(number, "future", "possessive")
                + " "
                + verb["simple"]["past"]
            )
            forms += 1 * [future_perfect]
            # Present perfect: has/have + simple present verb
            present_perfect = (
                self._get_special_verb(number, "present", "possessive")
                + " "
                + verb["simple"]["past"]
            )
            forms += 3 * [present_perfect]
            # Pluperfect: had + simple present verb
            pluperfect = (
                self._get_special_verb(number, "past", "possessive")
                + " "
                + verb["simple"]["past"]
            )
            forms += 2 * [pluperfect]

        return random.choice(forms)

    def _get_full_noun(self, number, number_of_adjectives):
        """Get a noun with an article and adjectives from a dictionary.

        Args:
            number (str): The grammatical number of the noun as a string.
            number_of_adjectives (int): The number of adjectives to for the
                full noun.

        Returns:
            str: A random, fully described noun consisting of a random noun
                with a the given number of adjectives and a random article.
        """
        word = self._get_noun(number)

        adjectives = self._get_adjectives(number_of_adjectives)
        # Temporary described_noun to figure out the correct article
        if adjectives:
            word = adjectives + " " + word

        if word[0].lower() in self.VOWELS:
            suffix_type = "vowel"
        else:
            suffix_type = "normal"
        article = self._get_article(number, suffix_type)
        if article:
            word = article + " " + word

        return word

    def word(self, max_adjectives=2):
        """Generate a word with adjectives.

        This acts partially like a wrapper around _get_full_noun().

        Args:
            dictionary_filepath (str): A valid filepath to a properly formatted
                JSON dictionary.
            max_adjectives (int, optional): A maximum number of adjectives
                for the word to have. Defaults to 3.

        Returns:
            str: A random word consisting of a noun with a random number of
                adjectives from 0 to the given max.
        """
        number_of_adjectives = random.randint(0, max_adjectives)
        number = random.choice(self.NUMBERS)
        word = self._get_full_noun(number, number_of_adjectives)
        return word

    def simple_sentence(self, max_adjectives=2):
        """Generate a simple sentence.

        Args:
            max_adjectives (int, optional): A maximum number of adjectives
                for the word to have. Defaults to 3.

        Yields:
            str: A random word consisting of a noun with a random number of
                adjectives from 0 to the given max.
        """
        subject_number_of_adjectives = random.randint(0, max_adjectives)
        subject_number = random.choice(self.NUMBERS)
        subject = self._get_full_noun(subject_number, subject_number_of_adjectives)

        transitivity = random.choice(["transitive", "intransitive"])
        tense = random.choice(self.WEIGHTED_TENSES)
        verb = self._get_verb(subject_number, tense, transitivity)

        sentence_parts = [subject, verb]
        if transitivity == "transitive":
            # Name it complement rather than object to prevent name shadowing
            complement_number_of_adjectives = random.randint(0, max_adjectives)
            complement_number = random.choice(self.NUMBERS)
            complement = self._get_full_noun(
                complement_number, complement_number_of_adjectives
            )
            sentence_parts.append(complement)

        sentence = " ".join(sentence_parts) + "."

        # We capitalize the first letter of the string. We don't use
        # sentence.capitalize() to keep the other upper case letters upper case
        return "{}{}".format(sentence[0].upper(), sentence[1:])
