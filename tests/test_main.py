import os

from moto import mock_aws
import requests_mock
import boto3
from linebot.webhook import SignatureValidator

from tests.fixture import lambda_input
from main import lambda_handler


@mock_aws
def test_dynamodb_handler(lambda_input, monkeypatch):
    #### perpare data and mock ####
    with requests_mock.Mocker() as m:

        ## mock open_ai ##
        m.get('https://api.openai.com/v1/models', text='{"response":"ok"}')
        m.post('https://api.openai.com/v1/chat/completions',
               text='{"response":"ok"}')

        # mock line chatbot
        m.post('https://api.line.me/v2/bot/message/reply',
               text='{"response":"ok"}')

        def mock_valiate_sigture(*args, **kwargs):
            return True
        monkeypatch.setattr(SignatureValidator, "validate",
                            mock_valiate_sigture)

        ## mock dynamoDB ##
        region = 'ap-northeast-1'
        dynamodb = boto3.resource('dynamodb', region_name=region)

        # Create the DynamoDB table.
        dynamodb.create_table(
            TableName='users',
            KeySchema=[{
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            }],
            AttributeDefinitions=[{
                'AttributeName': 'user_id',
                'AttributeType': 'S'
            }],
            BillingMode='PAY_PER_REQUEST',
        )
        dynamodb.create_table(
            TableName='logs',
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'N'
                },
            ],
            BillingMode='PAY_PER_REQUEST',
        )

        #### test ####

        # case1: normal chat condition
        r = lambda_handler(lambda_input, context="")
        assert r['statusCode'] == 200
        assert r['body'] == 'ok'
