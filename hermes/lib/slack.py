#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class Slack:

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def post(
            self,
            subject: str,
            sender: str,
            receiver: str,
            date: str,
            icon: str,
            url: str,
            service_name: str):
        payload = {
            'attachments': [
                {
                    'fallback': f'{sender} - {subject} - {date}',
                    'color': '#3AA3E3',
                    'author_name': service_name,
                    'author_link': url,
                    'author_icon': icon,
                    'title': subject,
                    'title_link': url,
                    'fields': [
                        {
                            "title": "From",
                            "value": sender,
                        },
                        {
                            "title": "To",
                            "value": receiver,
                        },
                        {
                            "title": "Date Received",
                            "value": date,
                        }
                    ]
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        return requests.post(
            url=self.webhook_url,
            headers=headers,
            json=payload
        )
