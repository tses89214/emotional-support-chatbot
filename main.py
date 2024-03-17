# pylint: disable=broad-exception-caught,missing-function-docstring,broad-exception-raised

"""
Entry Point - main.py:
This file acts as the primary gateway for the Line chatbot.
It handles the reception of user input messages, 
communication with OpenAI for responses,
and ultimately dispatches those responses back to the client.

In traditional MVC architecture,
it recommended to delegate such functionality to a "controller".
However, given the scale and specific requirements of our ongoing project,
I've opted to centralize all business logic within main.py for simplicity.

Deployment Note:
At present, we deploy the application using AWS Lambda,
where the lambda_handler function serves as the designated entry point.
"""
import os
import time
import logging
import json
import re

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import \
    MessageEvent, TextMessage, TextSendMessage, AudioMessage, ImageMessage

from src.models.user import User
from src.models.log import Log
from src.models.dynamodb_handler import DynamoDBHandler
from src.models.openai_agent import OpenAIAgent

# line
line_bot_api = LineBotApi(
    channel_access_token=os.getenv(key='LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(channel_secret=os.getenv(key='LINE_CHANNEL_SECRET'))

# chatGPT
openai_agent = OpenAIAgent(
    api_key=os.getenv(key='DEFAULT_API_KEY'),
    model_engine=os.getenv(key='OPENAI_MODEL_ENGINE'))

default_prompt = os.getenv(key='DEFAULT_PROMPT')

# dynamoDB
dynamodb = DynamoDBHandler(region_name='ap-northeast-1')
users_prompt = {}
history = {}

# logger
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event):
        """
        This function act as text message controller,
        you can find most of business logic here.
        """

        # Auth and get user prompt
        user_id = event.source.user_id
        if not users_prompt.get(user_id):
            susscess, user = dynamodb.get_user(user_id)
            if susscess:
                users_prompt[user.user_id] = user.prompt
            else:
                user = User(user_id=user_id, prompt=default_prompt) 
                dynamodb.add_user(user)
                users_prompt[user_id] = default_prompt

        text = event.message.text.strip()
        logger.info('%s: %s', user_id, text)

        try:
            # feature1: set users's prompt
            if text.startswith('/設定指令'):
                prompt = re.sub('/設定指令', '', text)
                users_prompt[user_id] = prompt
                dynamodb.add_user(User(user_id=user_id, prompt=prompt))
                msg = TextSendMessage(text='設定完成')

            # feature2: regular text message response
            else:
                # check history log
                if not history.get(user.user_id):
                    history[user.user_id] = dynamodb.get_log(user=user, n=10)

                is_successful, response, error_message = \
                    openai_agent.chat_completions(
                        user=user,
                        history=history[user.user_id],
                        text=text
                    )
                response_text = response['choices'][0]['message']['content']

                if not is_successful:
                    raise BaseException(error_message)

                msg = TextSendMessage(text=response_text)
                dynamodb.write_log(
                    Log(
                        timestamp=int(time.time()),
                        user_id=user_id,
                        prompt=users_prompt[user_id],
                        input_=text,
                        output=response_text))

        except Exception as error:
            logger.error(str(error),exc_info=True)

            if str(error).startswith('Incorrect API key provided'):
                msg = TextSendMessage(text='OpenAI API Token 有誤，請重新註冊。')

            elif str(error).startswith(
                    'That model is currently overloaded with other requests.'):
                msg = TextSendMessage(text='已超過負荷，請稍後再試')

            else:
                msg = TextSendMessage(
                    text='系統遇到一些錯誤，請截圖提供以下訊息給管理員。\n' + \
                         'User ID: ' + user_id + \
                         'Meet Error: ' + str(error))

        line_bot_api.reply_message(event.reply_token, msg)

    @handler.add(MessageEvent, message=AudioMessage)
    def handle_audio_message(event):
        """
        We don't accept audio messages at this moment.
        """
        user_id = event.source.user_id
        line_bot_api.reply_message(event.reply_token, '我目前只接受文字訊息，未來敬請期待!')
        logger.info('%s send a audio message.', user_id)

    @handler.add(MessageEvent, message=ImageMessage)
    def handle_image_message(event):
        """
        we don't accept image messages at this moment.
        """
        user_id = event.source.user_id
        line_bot_api.reply_message(event.reply_token, '我目前只接受文字訊息，未來敬請期待!')
        logger.info('%s send a image message.', user_id)

    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    # get request body as text
    body = event['body']

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 502,
            'body':
            json.dumps(
                "Invalid signature.  \
                Check your channel access token/channel secret.")
        }
    return {
        'statusCode': 200,
        'body': "ok"
    }
