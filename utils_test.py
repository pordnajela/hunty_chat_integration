from dotenv import load_dotenv
load_dotenv()

import unittest
from unittest.mock import patch, MagicMock
from utils import send_message, chat

class UtilsTestCase(unittest.TestCase):
    @patch("utils.WhatsApp")
    def test_send_message(self, mock_send_message):
        mock_send_message.send_message.return_value = True

        self.assertEqual(send_message('Hello'), None)

    @patch("utils.openai.ChatCompletion")
    def test_chat(self, mock_chat):
        mock_response = MagicMock()
        mock_response.choices = [
            {
                "message": {
                    "content": 'Test message'
                }
            }
        ]
        mock_chat.create.return_value = mock_response
        self.assertEqual(chat('Hello'), 'Test message')

if __name__ == '__main__':
    unittest.main()