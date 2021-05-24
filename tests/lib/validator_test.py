#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest

from hermes.lib.exceptions import HermesException
from hermes.lib.model import Notifier as DataModel
from hermes.lib.validator import FileValidator, EmailValidator, SlackWebHookUrlValidator, validator_registry


class TestFileValidator:

    @pytest.mark.parametrize('is_file_value, file_name', [
        (False, 'test.yaml'),
        (True, 'test.txt'),
    ])
    @patch('os.path.isfile')
    def test_validate_will_throw_exception_when_failed_validation(self, is_file, is_file_value, file_name):
        is_file.return_value = is_file_value
        validator = FileValidator(file_name=file_name)

        with pytest.raises(HermesException):
            validator.validate()


class TestEmailValidator:

    @pytest.mark.parametrize('accounts', [
        ([dict(email='', password='asd')]),
        ([dict(email='blah@yahoocom', password='asd')]),
    ])
    def test_validate_will_throw_exception_when_email_is_invalid(self, accounts):
        data = DataModel(**dict(
            config=dict(slack_webhook_url='test'),
            accounts=accounts
        ))
        validator = EmailValidator(data=data)

        with pytest.raises(HermesException):
            validator.validate()

    @patch('hermes.lib.email.Google')
    def test_validate_can_login_is_successful(self, google):
        data = DataModel(**dict(
            config=dict(slack_webhook_url='test'),
            accounts=[dict(email='blah@yahoo.com', password='asd')]
        ))
        validator = EmailValidator(data=data)
        validator.validate()

        assert google.login.is_called_once()
        assert google.logout.is_called_once()


class TestSlackWebHookUrlValidator:

    @pytest.mark.parametrize('webhook_url', [
        (''),
        ('test'),
        ('https://hooks.slack.com/'),
        ('https://hooks.slack.com/services'),
    ])
    def test_validate_will_throw_exception_when_url_is_invalid(self, webhook_url):
        data = DataModel(**dict(
            config=dict(slack_webhook_url=webhook_url)
        ))
        validator = SlackWebHookUrlValidator(data=data)

        with pytest.raises(HermesException):
            validator.validate()


def test_validator_registry_will_return_validators():
    assert validator_registry.get_validators() == [
        EmailValidator.__name__,
        SlackWebHookUrlValidator.__name__
    ]


def test_validator_registry_will_add_validator():
    validator_registry.add_validator('test')
    assert validator_registry.get_validators() == [
        EmailValidator.__name__,
        SlackWebHookUrlValidator.__name__,
        'test'
    ]
