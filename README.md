# Bot Messengers

A collection of programs that act as a command line interface for sending single messages on a
variety of social media platforms.

These modules can be used in conjunction with other pieces of software to automatically send
messages with random or meaningful content.

## Included Bots

* **TweeterBot:** A bot that sends messages for [@EliHunter173](https://twitter.com/EliHunter173).

## Getting Started

The specific setup required depends on the bot you want to use. However, generally the setup
consists of setting up the secrets for your desired platform and then running the bot.

Additionally, you must install the requirements listed in `requirements.txt` in a python virtualenv
named `virtualenv` at the top level of this project.

### TweeterBot

1. Copy `twitter_secrets_example.py` to `twitter_secrets.py`
2. Edit `twitter_secrets.py` to contain your `consumer_key`, `consumer_secret`, `access_token_key`,
   and `access_token_secret`.
3. Run `tweeter.py`. Either pipe in the content you want TweeterBot to tweet at the end of a
   pipeline or specify any number of files for TweeterBot to tweet the contents of.

## Authors

* Eli W. Hunter

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
