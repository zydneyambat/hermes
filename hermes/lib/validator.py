#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from abc import ABC, abstractmethod
from typing import List

import hermes.lib.email as email_module
from hermes.lib.exceptions import HermesException
from hermes.lib.model import Account, Notifier as DataModel


class FileValidator:

    SUPPORTED_FORMAT = '.yaml'

    def __init__(self, file_name: str):
        self.file_name = file_name

    def validate(self):
        if not (
            os.path.isfile(self.file_name)
            and self.file_name.endswith(self.SUPPORTED_FORMAT)
        ):
            raise HermesException('File is not valid!')


class BaseValidator(ABC):

    def __init__(self, data: DataModel):
        self.data = data

    @abstractmethod
    def validate(self):
        """ Validate here """


class EmailValidator(BaseValidator):

    def validate(self):
        for account in self.data.accounts:
            self.validate_email_format(email=account.email)
            self.validate_can_login(account=account)

    def validate_email_format(self, email: str) -> None:
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if not re.search(regex, email):
            raise HermesException(f'Email "{email}" is not valid!')

    def validate_can_login(self, account: Account) -> None:
        email_class = getattr(email_module, account.driver)
        email = email_class(account=account, config=self.data.config)
        email.login()
        email.logout()


class SlackWebHookUrlValidator(BaseValidator):

    SLACK_WEBHOOK_URL_FORMAT = 'https://hooks.slack.com/services/'

    def validate(self) -> None:
        self.validate_incoming_webhook_url_format()

    def validate_incoming_webhook_url_format(self) -> None:
        webhook_url = self.data.config.slack_webhook_url

        if not webhook_url.startswith(self.SLACK_WEBHOOK_URL_FORMAT):
            raise HermesException(f'Invalid Slack Webhook URL: {webhook_url}')


class ValidatorRegistry:

    def __init__(self):
        self.validators = []

    def get_validators(self) -> List:
        return self.validators

    def add_validator(self, validator: str) -> None:
        self.validators.append(validator)


validator_registry = ValidatorRegistry()
validator_registry.add_validator(EmailValidator.__name__)
validator_registry.add_validator(SlackWebHookUrlValidator.__name__)
