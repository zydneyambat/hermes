#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner

from hermes.cli.command.notify import notify


def test_notify_failed():
    runner = CliRunner()
    result = runner.invoke(notify, ['-f', 'test'])

    assert result.exception
    assert result.exit_code == 1
