import argparse
import fileinput
import random
import sys

from tweeter_bot import Dictionary, TweeterBot


def tweet():
    parser = argparse.ArgumentParser(
        description="A command line interface for the bot module of tweeter_bot"
    )
    parser.add_argument(
        "config", help="path to the TOML-formatted Twitter API config"
    )
    args = parser.parse_args()

    tweeter = TweeterBot.from_file(args.config)
    for line in fileinput.input():
        tweeter.tweet(line)


def generate_prose():
    parser = argparse.ArgumentParser(
        description="A command line interface for text_gen module of tweeter_bot"
    )
    parser.add_argument("dictionary_filepath", help="path to the JSON dictionary")
    parser.add_argument(
        "-n",
        "--number",
        default=1,
        type=int,
        help="number of random strings to generate (default: 1)",
    )
    parser.add_argument(
        "-p",
        "--perpetual",
        action="store_true",
        help="whether to create words perpetually",
    )
    parser.add_argument(
        "-w",
        "--word",
        action="append_const",
        dest="generators",
        const=Dictionary.word,
        help="add a word generator to the list of the possible generators",
    )
    parser.add_argument(
        "-s",
        "--simple-sentence",
        action="append_const",
        dest="generators",
        const=Dictionary.simple_sentence,
        help="add a simple sentence generator to the list of the possible generators",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_const",
        dest="generators",
        const=[Dictionary.word, Dictionary.simple_sentence],
        help="add a all possile generators to the list of the possible generators",
    )
    args = parser.parse_args()

    # Error Checking
    if not args.generators:
        print("At least one generator must be specified")
        sys.exit(2)
    if args.number < 0:
        print("A negative number of items cannot be specified")
        sys.exit(3)
    if args.dictionary_filepath is None:
        print("A dictionary filepath must be specified")
        sys.exit(4)

    # Create all text generators
    # This is done so that the dictionary_filepath can be detected at the same
    # time as all other args
    dictionary = Dictionary.from_json(args.dictionary_filepath)
    # Output Text
    if args.perpetual:
        while True:
            print(random.choice(args.generators)(dictionary))
    else:
        for _ in range(args.number):
            print(random.choice(args.generators)(dictionary))
