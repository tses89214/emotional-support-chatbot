#pylint: disable=missing-module-docstring
from typing import List, Dict, Tuple

import requests

from src.models.user import User

class OpenAIAgent:
    """
    The `OpenAIAgent` class is a Python class
    that interacts with the OpenAI API to perform chat completions..
    """

    def __init__(self, api_key: str, model_engine: str):
        """
        Initialize the Open AI Agent.

        Params:
            api_key (str): The API key obtained from OpenAI.
            model_engine (str): The engine we want to use. 
                Different engine has different performance and pricing. 
                Check for Detail: https://platform.openai.com/docs/models
        """
        self.api_key = api_key
        self.model_engine = model_engine
        self.base_url = 'https://api.openai.com/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

    # pylint: disable=missing-timeout
    def _request(self, method: str, endpoint: str, body=None) \
        -> Tuple[bool, Dict, str]:
        """
        Send a request to the OpenAI API.

        Params:
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

        return True, response, None

    def check_token_valid(self) -> bool:
        """
        Check the validity of the token with the OpenAI API.
        """
        return self._request('GET', '/models')[0]

    def chat_completions(
            self, user: User, history: List[Dict], text: str) \
                -> Tuple[bool, Dict, str]:
        """
        Get chat completions from the OpenAI model based on the input messages.

        Params:
            user (User): The User.
            history (List[Dict[str,str]]): the log from this user.
            text: input text.

        Returns:
            (
                success status (bool),
                response data (dict),
                and error message (str)
            )
        Example:
            (True,
            {'id': 'chatcmpl-8yCEY04OwNNrOhVArvMLPRryHpSlD',
            'object': 'chat.completion',
            'created': 1709357398,
            'model': 'gpt-3.5-turbo-0125',
            'choices': [{'index': 0,
                'message': {'role': 'assistant',
                'content': "(the response of gpt) ..."},
                'logprobs': None,
                'finish_reason': 'stop'}],
            'usage': {
                    'prompt_tokens': 26,
                    'completion_tokens': 31, 
                    'total_tokens': 57},
            'system_fingerprint': 'fp_2b778c6b35'},
            None)
        """
        messages = self.log_formatting(
            prompt=user.prompt, history=history
        )
        messages.append(
            {'role': 'user', 'content': text}
        )
        json_body = {
            'model': self.model_engine,
            'messages': messages
        }
        response = self._request('POST', '/chat/completions', body=json_body)
        return response

    def log_formatting(self, prompt, history) -> List[Dict[str,str]]:
        """
        Convert log into chatGPT acceptable history log format.

        Params:
            prompt (str):the command we gave gpt.
            history (List[Dict]): the log item we get from dynamoDB.

        Example:
            log(user_id='123', prompt='你是有禮貌的機器人', input='hi', output='你好', timestamp)
            ->
            [
                {'role': 'system', 'content': '你是有禮貌的機器人'},
                {'role': 'user', 'content': 'hi'},
                {'role': 'assistant', 'content': '你好'}
            ]
        """
        messages = []
        messages.append(
            {'role': 'system', 'content': prompt}
        )
        if len(history):
            for item in history:
                messages.append(
                    {'role': 'user', 'content': item['input']}
                )
                messages.append(
                    {'role': 'assistant', 'content': item['output']}
                )
        return messages
