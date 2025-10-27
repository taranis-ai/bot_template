# bot_template

A copier template for bots compatible with taranis-ai

## Pre-requisites

copier - https://copier.readthedocs.io/en/stable/#installation


## Create Bot project from template

This is a quick example of how to create your own bot from this template. Let's say, you want to create the new awesome bot, the **AwesomeBot**:

First, create a project from the template:

    copier copy --trust https://github.com/taranis-ai/bot_template AwesomeBot

> **Note:** copier will use the latest tag of this repository by default. You can specify a different ref with the `--vcs-ref` option

You will be prompted a few questions:

```bash
🎤 Project Name
   Awesome New Bot
🎤 Different models used in your project (comma-separated list, e.g. model_a, model_b)
   bert, roberta
🎤 Your E-Mail
   employee@ait.ac.at
🎤 A short description of what the bot does
   Cool things
🎤 Github URL
   https://github.com/taranis-ai/awesome_bot
🎤 Initialize git repo?
   Yes

```
copier will create a directory `AwesomeBot` and copy the files from the template with the correct structure and pre-defined configs for you.

```bash
AweseomeBot/
├── app.py
├── awesome_new_bot
│   ├── bert.py
│   ├── config.py
│   ├── __init__.py
│   └── roberta.py
├── build_container.sh
├── Containerfile
├── docker
│   └── compose.e2e.yml
├── LICENSE.md
├── pyproject.toml
├── README.md
└── tests
    ├── conftest.py
    ├── __init__.py
    └── test_function.py
```

Since we gave two possible models (bert & roberta), copier created a bert.py and a roberta.py file.
You can import the respective models and implement the bot logic there.

The only other file that needs to be changed is `config.py`

Here, you need to set the `PAYLOAD_KEY` config to what you want your JSON data to have as a key, e.g. "text".


## Update Bot project after template has changed

A cool feature of copier is to update projects created from templates when the template evolves.
For example, if you add a new file to the template, commit it and create a new tag, then you can switch to your created bot repo and run

    copier update --trust -A

copier will fetch the newest changes and you can then easily update your bot repo.

> **Note:** again, copier will use the latest tag for updating. Make sure to update it or run with `--vcs-ref` option


## Build and run your bot

You can run the Bot locally or build a container image from it.
More information can be found in the README.md of your created bot project.