#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from pydantic import ValidationError
from yaml import safe_load

from hermes.lib.exceptions import HermesException
from hermes.lib.model import Notifier as DataModel
from hermes.lib.validator import FileValidator


class Normalizer:

    def __init__(self, file_name: str):
        self.file_name = file_name

    def get_content(self) -> DataModel:
        self.validate_file_exists()
        content = self.parse_file()

        return content

    def validate_file_exists(self) -> None:
        validator = FileValidator(file_name=self.file_name)
        validator.validate()

    def parse_file(self):
        file_path = os.path.abspath(self.file_name)

        with open(file_path, 'r') as file:
            try:
                data = safe_load(file)
            except Exception as err:
                raise HermesException('Unable to decode file!', err)
            else:
                content = self.modelized(data=data)

        return content

    def modelized(self, data: dict) -> DataModel:
        try:
            content = DataModel(**data)
        except ValidationError as err:
            raise HermesException(err)
        else:
            return content
