from moto import mock_aws
import boto3

from src.models.user import User
from src.models.log import Log
from src.models.dynamodb_handler import DynamoDBHandler
from tests.fixture import mock_env_aws_auth
 
@mock_aws
def test_dynamodb_handler(mock_env_aws_auth):
    region = 'ap-northeast-1'
    dynamodb = boto3.resource('dynamodb',region_name = region)

    # Create the DynamoDB table.
    dynamodb.create_table(
        TableName='users',
        KeySchema = [{
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
        KeySchema = [
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

    handler = DynamoDBHandler(region_name=region)

    # test write user
    test_user = User(user_id='123abc',prompt='test_prompt')
    handler.set_user(test_user)

    # test get user
    response, user = handler.get_user(user_id= '123abc')
    assert response is True and user.user_id == '123abc' and user.prompt == 'test_prompt'

    response, user = handler.get_user(user_id= 'not_exists')
    assert response is False and user is None

    # test write log
    handler.write_log(log=Log(
        user_id='123abc',
        prompt='test_prompt',
        input_='inputs',
        output='output',
        timestamp=123456
    ))

    ## NOTE: this part weird, should be user_id not a user object.
    # test get log
    logs = handler.get_log(user=User(user_id='123abc',prompt='test'))
    assert logs[0]['timestamp'] == 123456