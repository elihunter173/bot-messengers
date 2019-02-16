# Text Generator

A non-semantic random text generator that uses a custom JSON dictionary to store and organize valid
words.

A small selection of predefined dictionaries are present in the `data/` subdirectory of this
project. However, custom dictionaries could be easily defined as long as they conform to the
standard described [here](#creating-custom-dictionaries)

This is used in conjunction with my [TweeterBot](https://github.com/EliHunter173/bot-messengers)
and cron to periodically produce silly tweets on my personal Twitter
([@EliHunter173](https://twitter.com/EliHunter173)).

## Getting Started

To use this `text_generator` module in your project, either include it as submodule in your project
or clone it and then add it to your `PYTHONPATH`

### Global Installation

```sh
git clone https://github.com/EliHunter173/text-generator.git
# In your bashrc (or similar) add this
export PYTHONPATH="$PATH:<repo_path>"
```

### Project Installation

```sh
# In your project
git submodule add https://github.com/EliHunter173/text-generator.git
# Add this module to your Python project (or other) as you would any other submodule
```

### Creating Custom Dictionaries

***TO BE CREATED***

## Authors

* Eli W. Hunter
