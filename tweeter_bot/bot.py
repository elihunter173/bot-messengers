"""Send tweets from a twitter account.

This module contains functions enabling easy tweeting from a Twitter account
using the secrets set up in the twitter_secrets module. This also contains a
simple command line interface that sends a single tweet for every line in stdin
or of the files provided as arguments.
"""

import toml
from TwitterAPI import TwitterAPI


class TweeterBot:
    @classmethod
    def from_file(cls, file):
        config = toml.load(file)
        # Set up Twitter API with the required contents
        api = TwitterAPI(
            config["consumer_key"],
            config["consumer_secret"],
            config["access_token_key"],
            config["access_token_secret"],
        )
        signature = config.get("signature", None)
        return cls(api, signature)

    def __init__(self, api, signature=None):
        self.api = api
        self.signature = signature

    def tweet(self, text):
        """Send tweets using self.api."""
        if self.signature is not None:
            text += self.signature
        r = self.api.request("statuses/update", {"status": text})
        if r.status_code != 200:
            raise RuntimeError(r.text)
