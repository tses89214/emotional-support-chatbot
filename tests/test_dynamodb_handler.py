from moto import mock_aws
import boto3

from src.models.user import User
from src.models.log import Log
from src.models.prompt import Prompt
from src.models.dynamodb_handler import DynamoDBHandler


@mock_aws
def test_dynamodb_handler():
    region = 'ap-northeast-1'
    dynamodb = boto3.resource('dynamodb', region_name=region)

    # Create the DynamoDB table.
    dynamodb.create_table(
        TableName='user',
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'S'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
    )
    dynamodb.create_table(
        TableName='log',
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
            }
        ],
        BillingMode='PAY_PER_REQUEST',
    )
    dynamodb.create_table(
        TableName='prompt',
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'prompt',
                'KeyType': 'RANGE'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'S'
            }, {
                'AttributeName': 'prompt',
                'AttributeType': 'S'
            },
        ],
        BillingMode='PAY_PER_REQUEST',
    )

    handler = DynamoDBHandler(region_name=region)

    # test write user
    test_user = User(user_id='123abc', create_at=123456, status='active')
    handler.add_user(test_user)

    # test get user
    response, user = handler.get_user(user_id='123abc')
    assert response is True and user.user_id == '123abc' and user.status == 'active'

    response, user = handler.get_user(user_id='not_exists')
    assert response is False and user is None

    # test write prompt
    test_prompt = Prompt(
        user_id='123abc',
        prompt='test_prompt',
        valid_from=123456,
        valid_to=123456 + 3600 * 24 * 7,
        is_current=True
    )
    handler.add_prompt(test_prompt)

    # test get prompt
    response, prompt = handler.get_prompt(user=test_user)
    assert response is True \
        and prompt.user_id == '123abc' \
        and prompt.prompt == 'test_prompt' \
        and prompt.valid_from == 123456 \
        and prompt.valid_to == 123456 + 3600 * 24 * 7 \
        and prompt.is_current is True

    # test update prompt
    new_prompt = Prompt(
        user_id='123abc',
        prompt='new_prompt',
        valid_from=123456,
        valid_to=123456 + 3600 * 24 * 7,
        is_current=True
    )
    handler.update_prompt(new_prompt)
    response, prompt = handler.get_prompt(user=test_user)
    assert response is True\
        and prompt.user_id == '123abc' \
        and prompt.prompt == 'new_prompt' \
        and prompt.valid_from == 123456 \
        and prompt.valid_to == 123456 + 3600 * 24 * 7 \
        and prompt.is_current is True

    # test write log
    test_log = Log(
        user_id='123abc',
        input_='test_input',
        output='test_output',
        timestamp=123456
    )
    handler.write_log(test_log)

    # test get log
    log = handler.get_log(user=test_user)
    assert len(log) == 1
    assert log[0]['user_id'] == '123abc' \
        and log[0]['input'] == 'test_input' \
        and log[0]['output'] == 'test_output'\
        and log[0]['timestamp'] == 123456
