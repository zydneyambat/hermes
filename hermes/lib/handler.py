#!/usr/bin/env python
# -*- coding: utf-8 -*-

import concurrent.futures

from halo import Halo

import hermes.lib.email as email_module
import hermes.lib.validator as validator_module
from hermes.lib.exceptions import HermesException
from hermes.lib.model import Notifier as DataModel


class NotifyHandler:

    def __init__(self, data: DataModel):
        self.data = data
        self.spinner = Halo(
            text='Setting up notifications',
            spinner='dots'
        )

    def run(self):
        self.spinner.start('Validating file')

        try:
            self.validate()
        except HermesException as err:
            self.spinner.fail('Error occured: {}'.format(err))
            exit(1)

        self.spinner.succeed()

        self.spinner.start('Watching inbox')
        self.watch()

    def validate(self):
        validators = validator_module.validator_registry.get_validators()

        for validator_name in validators:
            validator_class = getattr(validator_module, validator_name)
            validator = validator_class(data=self.data)
            validator.validate()

    def watch(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for account in self.data.accounts:
                email_class = getattr(email_module, account.driver)
                email_service = email_class(
                    account=account,
                    config=self.data.config
                )

                executor.submit(email_service.watch)
