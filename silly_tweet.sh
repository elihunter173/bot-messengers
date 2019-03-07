#!/usr/bin/env sh

# Handles the tweeting out of silly tweets, tweeter and my text_generator python
# module with the default silly dictionary.
#
# Dependencies:
#   * text_generator by Eli W. Hunter
#   * A set up virtualenv in this directory with TwitterAPI installed
#
# Authors:
#   * Eli W. Hunter

# Set up common variables
DIRPATH=$(dirname $(readlink -f $0))
text_gen_path="../text-generator"

# Load the virtualenv
source ${DIRPATH}/virtualenv/bin/activate

# Run the program
${text_gen_path}/text_generator.py -s ${text_gen_path}/data/silly_dictionary.json \
    | ${DIRPATH}/tweeter_bot.py
