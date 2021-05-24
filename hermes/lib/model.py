#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from typing import List

from pydantic import BaseModel


class Config(BaseModel):
    slack_webhook_url: str
    refresh_interval: int = 5


class EmailService(str, Enum):
    google = 'Google'


class Account(BaseModel):
    email: str
    password: str
    driver: EmailService = 'Google'


class Notifier(BaseModel):
    config: Config
    accounts: List[Account] = []

    class Config:
        extra = 'allow'
