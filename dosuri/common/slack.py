import requests
import json


class SlackClient:
    def __init__(self):
        self.channel_to_url = {
            'bot': 'https://hooks.slack.com/services/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'
        }

    def set_api_header(self):
        return {
            'Content-Type': 'application/json; charset=utf-8'
        }

    def send_message_to_bot_channel(self, message):
        url = self.channel_to_url['bot']
        data = {'text': message}
        return requests.post(url=url, data=json.dumps(data), headers=self.set_api_header())
