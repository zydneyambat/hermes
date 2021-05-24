#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest

from hermes.lib.exceptions import HermesException
from hermes.lib.model import Notifier as DataModel
from hermes.lib.handler import NotifyHandler


@patch('hermes.lib.handler.Halo')
@patch('hermes.lib.validator.SlackWebHookUrlValidator')
@patch('hermes.lib.validator.EmailValidator')
class TestNotifyHandler:

    def get_data_model(self):
        return DataModel(**dict(
            config=dict(slack_webhook_url='test'),
            accounts=[dict(email='blah@yahoo.com', password='asd')]
        ))

    def test_run_throw_exception_when_validation_failed(self, email_validator, slack_url_validator, halo):
        email_validator.side_effect = HermesException()

        data = self.get_data_model()
        data.accounts[0].email = 'blahyahoo.com'
        handler = NotifyHandler(data=data)
        with pytest.raises(SystemExit):
            handler.run()

    @patch('concurrent.futures')
    def test_run_when_ok(self, futures, email_validator, slack_url_validator, halo):
        handler = NotifyHandler(data=self.get_data_model())
        handler.run()

        assert email_validator.validate.is_called_once()
        assert slack_url_validator.validate.is_called_once()
        assert futures.submit.is_called()

    def test_validate(self, email_validator, slack_url_validator, halo):
        handler = NotifyHandler(data=self.get_data_model())
        handler.validate()

        assert email_validator.validate.is_called_once()
        assert slack_url_validator.validate.is_called_once()

    @patch('concurrent.futures')
    def test_watch(self, futures, email_validator, slack_url_validator, halo):
        handler = NotifyHandler(data=self.get_data_model())
        handler.watch()

        assert futures.submit.is_called()
