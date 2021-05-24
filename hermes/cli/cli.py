#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Entry point for the CLI
"""
from click import group, version_option

from hermes import __version__
from hermes.cli.command.notify import notify

CONTEXT_SETTINGS = dict(
    help_option_names=['--help', '-h'],
    auto_envvar_prefix='HERMES'
)


@group(context_settings=CONTEXT_SETTINGS)
@version_option(version=__version__)
def cli():
    """
    \b
    ╦ ╦┌─┐┬─┐┌┬┐┌─┐┌─┐
    ╠═╣├┤ ├┬┘│││├┤ └─┐
    ╩ ╩└─┘┴└─┴ ┴└─┘└─┘
    \b
    New email notifier on Slack!
    \b
      * Github Issues  https://github.com/zydneyambat/hermes/issues
    """


"""
Register commands into cli group"
"""
cli.add_command(notify)

if __name__ == "__main__":
    cli()  # pragma: no cover
