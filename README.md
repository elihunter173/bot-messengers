# tweeter-bot

Twitter bot that sends non-semantic, random sentences.

This uses a custom JSON dictionary format. You can see an example in
`data/silly_dictionary.json`.

## Installation

First, figure out your consumer key, consumer secret, access token key, and
access token secret to access Twitter's API. Put these values in a
`secrets.toml` file somewhere safe. You can find an example file in
`examples/secrets.toml`. Then, install the project.

```sh
$ pip install git+https://github.com/elihunter173/tweeter-bot.git
```

Now, you can run `tweeter-bot-gen` and `tweeter-bot-tweet`. `tweeter-bot-gen`
generates either words or sentences given a JSON dictionary and
`tweeter-bot-tweet` tweets messages from stdin given a TOML config file. Every
line is an individual tweet for `tweeter-bot-tweet`.
