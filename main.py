"""
DocString.
"""
import os
import time
import logging
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, AudioMessage, ImageMessage
)

from src.models.user import User
from src.models.log import Log
from src.models.models import DynamoDBHandler
from src.models.openai_agent import OpenAIAgent

# line
line_bot_api = LineBotApi(
    channel_access_token=os.getenv(key='LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(channel_secret=os.getenv(key='LINE_CHANNEL_SECRET'))

# chatGPT
openai_agent = OpenAIAgent(
    api_key=os.getenv(key='DEFAULT_API_KEY'),
    model_engine=os.getenv(key='MODEL_ENGINE'))

default_prompt = os.getenv(key='DEFAULT_PROMPT')

# dynamoDB
dynamodb = DynamoDBHandler(region_name='ap-northeast-1')
users_prompt = dynamodb.load_all_user()
history = {}

# logger
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event):
        """
        Currently we only received text message,
        """
        user_id = event.source.user_id
        if not users_prompt.get(user_id):
            users_prompt[user_id] = default_prompt
            dynamodb.set_user(User(user_id=user_id, prompt=default_prompt))
        user = User(user_id=user_id, prompt=users_prompt[user_id])
        text = event.message.text.strip()
        logger.info('%s: %s', user_id, text)

        try:
            if text.startswith('/設定指令'):
                pass
                # we add at next version.
            else:
                # check memory
                if not history.get(user.user_id):
                    history[user.user_id] = dynamodb.get_log(user=user, n=10)

                is_successful, response, error_message = \
                    openai_agent.chat_completions(
                        user=user,
                        history=history[user.user_id],
                        text=text
                    )

                # pylint: disable=broad-exception-raised
                if not is_successful:
                    raise BaseException(error_message)

                msg = TextSendMessage(text=response)
                dynamodb.write_log(
                    Log(
                        timestamp=int(time.time()),
                        user_id=user_id,
                        prompt=users_prompt[user_id],
                        input_=text,
                        output=response))

        # pylint: disable=broad-exception-caught
        except Exception as error:
            logger.error(str(error))

            if str(error).startswith('Incorrect API key provided'):
                msg = TextSendMessage(text='OpenAI API Token 有誤，請重新註冊。')

            elif str(error).startswith(
                    'That model is currently overloaded with other requests.'):
                msg = TextSendMessage(text='已超過負荷，請稍後再試')

            else:
                msg = TextSendMessage(
                    text='系統遇到一些錯誤，請截圖提供以下訊息給管理員。\n' + str(error))

        line_bot_api.reply_message(event.reply_token, msg)

    @handler.add(MessageEvent, message=AudioMessage)
    def handle_audio_message(event):
        """
        No audio message.
        """
        user_id = event.source.user_id
        line_bot_api.reply_message(event.reply_token, '我目前只接受文字訊息，未來敬請期待!')
        logger.info('%s send a audio message.', user_id)

    @handler.add(MessageEvent, message=ImageMessage)
    def handle_image_message(event):
        """
        No image message.
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
        'body': json.dumps("Hello from Lambda!")
    }
