import requests
import json
from django.conf import settings


class SlackClient:
    def __init__(self):
        self.channel_to_url = {
            'bot': settings.SLACK_BOT_URL
        }

    def set_api_header(self):
        return {
            'Content-Type': 'application/json; charset=utf-8'
        }

    def send_message_to_bot_channel(self, message):
        url = self.channel_to_url['bot']
        data = {'text': message}
        return requests.post(url=url, data=json.dumps(data), headers=self.set_api_header())
