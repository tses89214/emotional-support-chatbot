import requests_mock

from src.models.openai_agent import OpenAIAgent
from src.models.user import User

def test_openai_agent():
    with requests_mock.Mocker() as m:
        agent = OpenAIAgent(
            api_key = 'test_key',
            model_engine = 'test_model_engine'
        )

        # check_token_valid
        m.get('https://api.openai.com/v1/models', text='{"response":"ok"}')
        assert agent.check_token_valid() is True

        m.get('https://api.openai.com/v1/models',
                text='{"error":{"message":"meet_error"}}')
        assert agent.check_token_valid() is False

        # chat_completions
        m.post('https://api.openai.com/v1/chat/completions',
                text='{"response":"ok"}')
        assert agent.chat_completions(
            user=User(user_id='test_id',prompt='test_prompt'),
            history=[],
            text='test_input'
        )[0] is True

        m.post('https://api.openai.com/v1/chat/completions',
               text='{"error":{"message":"meet_error"}}')
        
        assert agent.chat_completions(
            user=User(user_id='test_id',prompt='test_prompt'),
            history=[],
            text='test_input'
        )[0] is False

        # log_formatting
        assert agent.log_formatting(
                prompt='test_prompt',
                history=[{
                    'user_id': 'user1',
                    'prompt': 'prompt1',
                    'input': 'input1',
                    'output': 'output1',
                    'timestamp': 12345}]
                ) == \
            [{'role': 'system', 'content': 'test_prompt'},
            {'role': 'user', 'content': 'input1'},
            {'role': 'assistant', 'content': 'output1'}]