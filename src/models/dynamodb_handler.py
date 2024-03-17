# pylint: disable=missing-module-docstring
import logging
from typing import List, Dict, Union

from boto3.dynamodb.conditions import Key

from src.models.user import User
from src.models.log import Log
from src.models.dynamodb_connector import DynamoDBConnector

logger = logging.getLogger(__name__)


class DynamoDBHandler:
    """
    A class for reading and writing data to DynamoDB,
    included users and logs.
    """

    def __init__(self, region_name='ap-northeast-1'):
        """
        Initialize the DynamoDBLogHandler instance.

        Params:
            region_name (str): Region of DynamoDB. Default is ap-northeast-1.
        """
        self.db = DynamoDBConnector(region_name=region_name)

    def get_user(self, user_id: str) -> User:
        """
        Get user's profile from Users table, including id and prompt.

        Params:
            user_id (str): user's id.
        """
        response = self.db.user_table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        if response['Items']:
            item = response['Items'][0]
            return True, User(user_id=item['user_id'], prompt=item['prompt'])
        else:
            return False, None

    def add_user(self, user: User) -> bool:
        """
        Add user to Users table. If user_id exists, record will be overwrite.

        Params:
            user (User): an User object.
        """
        response = self.db.user_table.put_item(Item=user.to_item())
        logger.info("PutItem succeeded: %s", response)
        return True

    def get_log(self, user: User, n: int = 10) \
            -> List[Dict[str, Union[str, int]]]:
        """
        Get n records of an users' from log table.

        Params:
            user (User): an User object.
            n (int): number of record we want to get. Default is 10.

        Returns:
            logs of an user (List of Dict), like:
            [{
                "user_id":"abc",
                "timestamp":123456,
                "input":"你是誰",
                "output":"我是 ChatGPT",
                "prompt":"你是有禮貌的機器人"
            }]

        NOTE:
            maybe use user_id directly will be better?
        """
        condition = Key('user_id').eq(user.user_id)

        response = self.db.log_table.query(
            KeyConditionExpression=condition,
            Limit=n,
            ScanIndexForward=False
        )
        items = response['Items']
        return items

    def write_log(self, log: Log):
        """
        Write log to log table.

        Params:
            log: a log Object.
        """
        response = self.db.log_table.put_item(Item=log.to_item())
        logger.info("PutItem succeeded: %s", response)
