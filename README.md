# Hermes

<a href="https://codeclimate.com/github/zydneyambat/hermes/maintainability"><img src="https://api.codeclimate.com/v1/badges/a0bf863579e4a571dde2/maintainability" /></a>
<a href="https://codeclimate.com/github/zydneyambat/hermes/test_coverage"><img src="https://api.codeclimate.com/v1/badges/a0bf863579e4a571dde2/test_coverage" /></a>

Hermes is a simple slack notification tool that watches for unseen messages on multiple emails!

## Architecture

## Requirements

Hermes is written in <a href="https://www.python.org/downloads/release/python-390/" target="_blank">Python3.9</a> and uses <a href="https://api.slack.com/messaging/webhooks" target="_blank">Slack Incoming Webhook</a>.

It is build on top of <a href="https://click.palletsprojects.com/en/8.0.x/" target="_blank">Click CLI</a> with <a href="https://pydantic-docs.helpmanual.io/" target="_blank">Pydantic</a> for data parsing and validation and 
also uses:
 
* <a href="https://pipenv-fork.readthedocs.io/en/latest/" target="_blank">Pipenv</a> to manage the virtualenv + install packages
* <a href="https://docs.pytest.org/en/stable/" target="_blank">Pytest</a> to execute unit tests

# Installation

Before installing the application, make sure all the dependencies are resolved.

## Dependencies

The application and its dependencies are fully containerized and rely on docker to manage 
the containers and uses of Make as our build automation tool.

So, if you don't have them installed already, please follow the links below:

* <a href="https://www.docker.com/" target="_blank">Docker</a> - Instructions to <a href="https://docs.docker.com/get-docker/" target="_blank">install</a>
* <a href="https://en.wikipedia.org/wiki/Make_%28software%29" target="_blank">Make</a>

Also make sure to create <a href="https://api.slack.com/messaging/webhooks" target="_blank">Slack Incoming Webhook</a>

## Installation

Once the dependencies are installed, just follow the simple steps below to have the application up and running.

Clone the repo and change the directory to the newly cloned folder.

```bash
git clone https://github.com/zydneyambat/hermes.git
cd hermes
```

Create a config yaml file based on config.yaml.dist and follow the instruction there.
```bash
cp config.yaml.dist config.yaml
```
 
Use the command `make` to trigger the installation.

```
make
```

The `make` command build the image, configure dependencies and install the application.

*Obs:* You can simply run `make` or `make help` for a list of all available commands.
 
# Running tests

To run the unit tests simply call `make test`.

It will use run the testing container and run the unit tests.

The coverage/index.html can be found on the root folder.
