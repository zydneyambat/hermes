#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch, PropertyMock

import imaplib
import pytest

from hermes.lib.exceptions import HermesException
from hermes.lib.email import Google
from hermes.lib.model import Account, Config


@patch('hermes.lib.email.imaplib.IMAP4_SSL')
class TestGoogle:

    def get_email_and_config(self):
        account = Account(**dict(email='blah@yahoo.com', password='asd'))
        config = Config(**dict(slack_webhook_url='test'))

        return account, config

    def test_login_throw_exception_when_login_failed(self, imap):
        imap.return_value.login.side_effect = imaplib.IMAP4.error()

        account, config = self.get_email_and_config()
        email = Google(account=account, config=config)
        with pytest.raises(HermesException):
            email.login()

    def test_login_will_select_inbox_when_ok(self, imap):
        account, config = self.get_email_and_config()
        email = Google(account=account, config=config)
        email.login()

        assert imap.select.is_called_once()

    def test_logout(self, imap):
        account, config = self.get_email_and_config()
        email = Google(account=account, config=config)
        email.imap = imap
        email.logout()

        assert imap.close.is_called_once()
        assert imap.logout.is_called_once()

    # @patch('hermes.lib.email.sleep')
    # @patch('hermes.lib.email.Slack')
    # def test_watch(self, slack, sleep, imap):
    #     imap.search.return_value = ('OK', [b'1'])
    #     imap.fetch.return_value = ('OK', [
    #          (b'8 (RFC822 {7290}',
    #           b'From: Test Blah <blah@test.com>\r\n'
    #           b'Date: Thu, 27 May 2021 00:04:38 +1000\r\n'
    #           b'Subject: Test\r\n'),
    #          b')'
    #     ])
    #     imap.return_value = imap
    #
    #     account, config = self.get_email_and_config()
    #     email = Google(account=account, config=config)
    #     with patch('hermes.lib.email.Email.is_watching', new=PropertyMock) as is_watching:
    #         is_watching.side_effect = [True, False]
    #     email.watch()
    #
    #     imap.login.is_called_once()
    #     imap.select.is_called_once()
    #     imap.noop.is_called()
    #     imap.search.is_called()
    #     slack.post.is_called()
    #     sleep.is_called()

    @pytest.mark.parametrize('data, expected', [
        ([], None),
        (['test'], None),
        ([
             (b'8 (RFC822 {7290}',
              b'From: Test Blah <blah@test.com>\r\n'
              b'Date: Thu, 27 May 2021 00:04:38 +1000\r\n'
              b'Subject: Test\r\n'),
             b')'
         ], {
            'date': 'Thu, 27 May 2021 00:04:38 +1000',
            'icon': 'https://i.imgur.com/h6MIrAj.png',
            'receiver': 'blah@yahoo.com',
            'sender': 'Test Blah <blah@test.com>',
            'service_name': 'Gmail',
            'subject': 'Test',
            'url': 'https://mail.google.com/',
        }),
    ])
    def test_parse_message(self, imap, data, expected):
        imap.fetch.return_value = ('OK', data)

        account, config = self.get_email_and_config()
        email = Google(account=account, config=config)
        email.imap = imap

        assert email.parse_message(uid=b'123') == expected

    @pytest.mark.parametrize('message, part, expected', [
        ({'Subject': 'Test Blah!'}, 'Subject', 'Test Blah!'),
        ({'Subject': '=?UTF-8?B?8J+Tow==?= Test Blah!'}, 'Subject', '📣'),
    ])
    def test_get_email_parts(self, imap, message, part, expected):
        account, config = self.get_email_and_config()
        email = Google(account=account, config=config)

        assert email.get_email_parts(message=message, part=part) == expected

    @pytest.mark.parametrize('last_uid, expected', [
        ('0', ['1', '2', '3']),
        ('1', ['2', '3']),
        ('2', ['3']),
        ('3', []),
    ])
    def test_get_messages(self, imap, last_uid, expected):
        uids = ['1 2 3']
        imap.search.return_value = ('OK', uids)

        account, config = self.get_email_and_config()
        email = Google(account=account, config=config)
        email.imap = imap
        email.last_uid = last_uid

        assert email.get_messages() == expected
        assert imap.noop.is_called_once()

    def test_get_latest_uids_will_return_uids(self, imap):
        uids = ['1 2 3']
        imap.search.return_value = ('OK', uids)

        account, config = self.get_email_and_config()
        email = Google(account=account, config=config)
        email.imap = imap

        assert email.get_latest_uids() == uids[0].split()
