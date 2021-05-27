#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch, mock_open

import pytest

from hermes.lib.exceptions import HermesException
from hermes.lib.model import Notifier as DataModel
from hermes.lib.normalizer import Normalizer


class TestNormalizer:

    @patch('hermes.lib.normalizer.safe_load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('hermes.lib.normalizer.FileValidator')
    def test_get_content(self, file_validator, open_mock, safe_load_mock):
        file_content = {'config': {'slack_webhook_url': 'test'}}
        safe_load_mock.return_value = file_content

        normalizer = Normalizer(file_name='test.yaml')

        assert normalizer.get_content() == DataModel(**file_content)

    @patch('hermes.lib.normalizer.FileValidator')
    def test_validate_file_exists(self, file_validator):
        normalizer = Normalizer(file_name='test.yaml')
        normalizer.validate_file_exists()

        assert file_validator.validate.is_called_once()

    @patch('hermes.lib.normalizer.safe_load')
    @patch('builtins.open', new_callable=mock_open)
    def test_parse_file_get_content_when_ok(self, open_mock, safe_load_mock):
        file_content = {'config': {'slack_webhook_url': 'test'}}
        safe_load_mock.return_value = file_content

        normalizer = Normalizer(file_name='test.yaml')

        assert normalizer.parse_file() == DataModel(**file_content)

    @patch('hermes.lib.normalizer.safe_load')
    @patch('builtins.open', new_callable=mock_open)
    def test_parse_file_throw_exception_when_unable_to_decode_file(self, open_mock, safe_load_mock):
        safe_load_mock.side_effect = Exception()

        normalizer = Normalizer(file_name='test.yaml')
        with pytest.raises(HermesException):
            normalizer.parse_file()

    def test_modelized_return_content_when_ok(self):
        data = {'config': {'slack_webhook_url': 'test'}}

        normalizer = Normalizer(file_name='test.yaml')
        assert normalizer.modelized(data=data) == DataModel(**data)

    def test_modelized_throw_exception_when_validation_failed(self):
        normalizer = Normalizer(file_name='test.yaml')
        with pytest.raises(HermesException):
            normalizer.modelized(data={})
