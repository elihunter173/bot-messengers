#!/usr/bin/env python3

"""Send tweets from a twitter account.

This module contains functions enabling easy tweeting from a Twitter account
using the secrets set up in ''. This also contains a command line interface for
tweeting.

Authors:
    Eli W. Hunter
"""

import fileinput
from TwitterAPI import TwitterAPI
import twitter_secrets


SIGNATURE = ' - TweeterBot'

# Set up Twitter API with the required contents
api = TwitterAPI(twitter_secrets.consumer_key,
                 twitter_secrets.consumer_secret,
                 twitter_secrets.access_token_key,
                 twitter_secrets.access_token_secret)


def tweet(text):
    """Send tweets using this modules api."""
    r = api.request('statuses/update', {'status': text})
    print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)


if __name__ == '__main__':
    tweet_text = ''
    for line in fileinput.input():
        tweet_text += line
    tweet_text += SIGNATURE

    tweet(tweet_text)
