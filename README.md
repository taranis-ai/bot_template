# bot_template

A cookiecutter template for bots compatible with taranis-ai

## Pre-requisites

cookiecutter - https://cookiecutter.readthedocs.io

    pip install cookiecutter


## Example: Create Bot project from template

This is a quick example of how to create your own bot from this template. Let's say, you want to create the new awesome bot AwesomeBot:

First, create a project from the template:

    cookiecutter https://github.com/taranis-ai/bot_template.git

You will be prompted a few questions:

```bash
  [1/5] Project Name: AwesomeBot
  [2/5] Your E-Mail (author@ait.ac.at): Your Mail
  [3/5] Description (A short description of what the bot does): Description
  [4/5] Github URL (''): Github repo URL (if you want to publish repo)
  [5/5] Initialize git repo? [y/n] (n):
```
Cookiecutter will create a project directory with the correct structure and pre-defined configs for you.

```bash
AwesomeBot/
├── app.py
├── awesomebot
│   ├── awesomebot.py
│   ├── config.py
│   ├── __init__.py
│   ├── log.py
│   ├── __main__.py
│   └── router.py
├── build_container.sh
├── Containerfile
├── LICENSE.md
├── pyproject.toml
└── README.md
```

You can go right ahead and implement your bot logic.
There are only two files that need to be changed:

- awesomebot.py - The actual inference code goes here
- router.py - Need to implement data pre-processing and calling the bot in post method


## Build and run

You can run the Bot locally or build a container image from it.
More information can be found in the README.md of your created bot project.