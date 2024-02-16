"""
The `OpenAIAgent` class is a Python class
that interacts with the OpenAI API to perform chat completions.
"""
from typing import List, Dict
import traceback

import requests

from src.models.user import User


class OpenAIAgent:
    """
    A class to interact with Open AI API.
    """

    def __init__(self, api_key: str, model_engine: str):
        """
        Initialize the Open AI Agent.
        """
        self.api_key = api_key
        self.model_engine = model_engine
        self.base_url = 'https://api.openai.com/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

    # pylint: disable=missing-timeout
    def _request(self, method: str, endpoint: str, body=None):
        """
        Send a request to the OpenAI API.

        Args:
            method: str. The HTTP method to use (GET or POST).
            endpoint: str. API endpoint.
            body: dict. Body of the request.

        Returns:
                (
                success status (bool),
                response data (dict),
                error message (str)
                )
        """
        try:
            if method == 'GET':
                response = requests.get(
                    f'{self.base_url}{endpoint}', headers=self.headers)
            elif method == 'POST':
                if body:
                    self.headers['Content-Type'] = 'application/json'
                response = requests.post(
                    f'{self.base_url}{endpoint}',
                    headers=self.headers, json=body)
            response = response.json()
            if response.get('error'):
                return False, {}, response.get('error', {}).get('message')

        # pylint: disable=broad-exception-caught
        except Exception as e:
            error_message = traceback.format_exc()
            return False, {}, f'{str(e), {error_message}}'

        return True, response, None

    def check_token_valid(self):
        """
        Check the validity of the token with the OpenAI API.

        """
        return self._request('GET', '/models')

    def chat_completions(
            self, user: User, history: List[Dict], text: str) -> str:
        """
        Get chat completions from the OpenAI model based on the input messages.

        Args:
            user: The User.
            history: the log from this user.
            text: input text.

        Returns:
            (
                success status (bool),
                response data (dict),
                and error message (str)
            )
        """
        messages = self.log_formatting(
            prompt=user.prompt, history=history, limit=8)
        messages.append(
            {'role': 'user', 'content': text}
        )
        json_body = {
            'model': self.model_engine,
            'messages': messages
        }
        return self._request('POST', '/chat/completions', body=json_body)

    def log_formatting(self, prompt, history, limit=8):
        """
        Convert log into chatGPT acceptable history log format.
        """
        messages = []
        messages.append(
            {'role': 'system', 'content': prompt}
        )
        for item in history[-limit:]:
            messages.append(
                {'role': 'user', 'content': item['input']}
            )
            messages.append(
                {'role': 'assistant', 'content': item['output']}
            )
        return history
