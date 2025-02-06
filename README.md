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
  [1/6] Project Name: Awesome New Bot
  [2/6] Different models used in your project (comma-separated list) (model_a): bert, roberta
  [3/6] Your E-Mail (author@ait.ac.at): Your Mail
  [4/6] Description (A short description of what the bot does): Description
  [5/6] Github URL (''): Github repo URL (if you want to publish repo)
  [6/6] Initialize git repo? [y/n] (n):

```
Cookiecutter will create a project directory with the correct structure and pre-defined configs for you.

```bash
AwesomeNewBot/
├── app.py
├── awesome_new_bot
│   ├── bert.py
│   ├── config.py
│   ├── decorators.py
│   ├── __init__.py
│   ├── log.py
│   ├── __main__.py
│   ├── predictor_factory.py
│   ├── predictor.py
│   ├── roberta.py
│   ├── router.py
│   └── tests
├── build_container.sh
├── Containerfile
├── LICENSE.md
├── pyproject.toml
├── README.md
└── tox.ini
```

Since we gave two possible models (bert & roberta), cookiecutter created a bert.py and a roberta.py file.
You can import the respective models and implement the bot logic there.

The only other file that needs to be changed is router.py

Here, you need to implement the post method, that receives data from a POST request and calls the predict method of the appropriate models.


## Build and run

You can run the Bot locally or build a container image from it.
More information can be found in the README.md of your created bot project.