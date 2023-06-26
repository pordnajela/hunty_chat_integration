import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env.test')
load_dotenv(dotenv_path)

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from webhook import webhook_bp

class WebhookTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(webhook_bp)
        self.client = self.app.test_client()

    def test_webhook_get(self):
        test_token = os.getenv('WHATSAPP_WEBHOOK_TOKEN_VERIFICATION')
        response = self.client.get('/webhook/?hub.verify_token='+ test_token +'&hub.challenge=success')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'success')

    @patch("webhook.insert_message")
    @patch("webhook.send_message")
    @patch("webhook.chat")
    def test_webhook_post(self, mock_chat, mock_send_message, mock_insert_message):
        payload = {
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "messages": [
                                    {
                                        "id": "212312312312123",
                                        "from": "573111111111",
                                        "text": {
                                            "body": "Hello!"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
        mock_chat.return_value = 'Bot message'
        mock_send_message.return_value = True
        mock_insert_message.return_value = True

        response = self.client.post('/webhook/', json=payload)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()