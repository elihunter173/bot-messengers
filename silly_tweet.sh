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
script_path=$(readlink -f $0)
parent_path=${script_path%/*}
text_gen_path="${HOME}/src/github/text-generator"

# Load the virtualenv
source ${parent_path}/virtualenv/bin/activate

# Run the program
echo $(${text_gen_path}/text_generator.py -s ${text_gen_path}/data/silly_dictionary.json) '-- TweeterBot' \
    | ${parent_path}/tweeter.py
