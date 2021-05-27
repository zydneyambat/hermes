#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import email
import imaplib
from abc import ABC
from email.header import decode_header
from time import sleep

from hermes.lib.exceptions import HermesException
from hermes.lib.model import Account, Config
from hermes.lib.slack import Slack


class Email(ABC):

    IMAP_HOST = ''
    ICON = ''
    URL = ''
    SERVICE_NAME = ''
    SELECTED_MAILBOX = 'INBOX'
    DEFAULT_CHAR_ENCODING = 'utf-8'

    def __init__(self, account: Account, config: Config):
        self.account = account
        self.config = config
        self.imap = None
        self.slack = Slack(webhook_url=config.slack_webhook_url)
        self.last_uid = 0
        self.is_watching = True

    def login(self):
        self.imap = imaplib.IMAP4_SSL(self.IMAP_HOST)

        try:
            self.imap.login(self.account.email, self.account.password)
        except imaplib.IMAP4.error:
            raise HermesException(
                f'Unable to login for this email {self.account.email}'
            )
        else:
            self.imap.select(self.SELECTED_MAILBOX, True)

    def logout(self):
        self.imap.close()
        self.imap.logout()

    def watch(self):
        self.login()

        while self.is_watching:
            try:
                self.send_notification()
            except Exception:
                break

    def send_notification(self):
        messages = self.get_messages()
        for uid in messages:
            message = self.parse_message(uid=uid)
            if message:
                self.last_uid = uid
                self.slack.post(**message)

        sleep(self.config.refresh_interval)

    def parse_message(self, uid: bytes):
        result, data = self.imap.fetch(uid, '(RFC822)')
        if not data:
            return

        for response in data:
            if not isinstance(response, tuple):
                continue
            message = email.message_from_bytes(response[1])
            subject = self.get_email_parts(message=message, part='Subject')
            sender = self.get_email_parts(message=message, part='From')
            date = self.get_email_parts(message=message, part='Date')

            return dict(
                subject=subject,
                sender=sender,
                receiver=self.account.email,
                date=date,
                icon=self.ICON,
                url=self.URL,
                service_name=self.SERVICE_NAME
            )

    def get_email_parts(self, message: dict, part: str):
        subject, encoding = decode_header(message[part])[0]
        if isinstance(subject, bytes):
            encoding = encoding if encoding else self.DEFAULT_CHAR_ENCODING
            subject = subject.decode(encoding)

        return subject

    def get_messages(self):
        self.imap.noop()

        uids = self.get_latest_uids()

        try:
            uid_start = uids.index(self.last_uid) + 1
        except ValueError:
            uid_start = 0

        return uids[uid_start:]

    def get_latest_uids(self):
        date_today = datetime.date.today().strftime('%d-%b-%Y')
        result, messages = self.imap.search(
            None,
            '(UNSEEN)', f'(SENTSINCE {date_today})'
        )
        uids = messages[0].split()

        return uids


class Google(Email):
    IMAP_HOST = 'imap.gmail.com'
    ICON = 'https://i.imgur.com/h6MIrAj.png'
    URL = 'https://mail.google.com/'
    SERVICE_NAME = 'Gmail'
