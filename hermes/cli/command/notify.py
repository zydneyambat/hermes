#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click import command, option
from halo import Halo

from hermes.lib.exceptions import HermesException
from hermes.lib.handler import NotifyHandler
from hermes.lib.normalizer import Normalizer


@command(short_help='Sends slack notification for every new email')
@option(
    '-f',
    '--file',
    type=str,
    required=True,
    help='Path to config yaml file'
)
def notify(file):
    """
    Sends slack notification for every new email
    """
    normalizer = Normalizer(file_name=file)

    try:
        data = normalizer.get_content()
    except HermesException as err:
        spinner = Halo(spinner='dots')
        spinner.fail('Error occured: {}'.format(err))
        exit(1)
    else:  # pragma: no cover
        handler = NotifyHandler(data=data)
        handler.run()
