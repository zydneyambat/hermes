#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch

from hermes.lib.slack import Slack


class TestSlack:

    @patch('hermes.lib.slack.requests')
    def test_post(self, requests):
        slack = Slack(webhook_url='blah')
        slack.post(**dict(
            subject='test 123',
            sender='sender1',
            receiver='receiver1',
            date='28/05/21 00:00:00',
            icon='https://imgur.com',
            url='https://google.com',
            service_name='TestService'
        ))

        assert requests.post.is_called_once()
