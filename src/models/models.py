"""
This module provides a DynamoDBHandler class for
reading and writing data to DynamoDB, including users and logs.
"""
import logging

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from src.models.user import User
from src.models.log import Log
from src.models.dynamodb import DynamoDB


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
            resource: A Boto3 DynamoDB resource.
        """
        self.db = DynamoDB(region_name=region_name)

    def get_user(self, user_id: str) -> User:
        """
        Get user's prompt from Users table.
        """
        try:
            response = self.db.user_table.query(
                KeyConditionExpression=Key('user_id').eq(user_id)
            )
            item = response['Items'][0]
            return User(user_id=item['user_id'], prompt=item['prompt'])

        except ClientError as err:
            self._handle_error("get_user", err)

    def set_user(self, user: User):
        """
        Set user's prompt to Users table.
        """
        try:
            response = self.db.user_table.put_items(Item=user.to_item)
            logger.info("PutItem succeeded: %s", response)

        except ClientError as err:
            self._handle_error("set_user", err)

    def load_all_user(self):
        """
        Load all users prompt when system up.
        """
        try:
            response = self.db.user_table.scan()
            users_prompt = {}
            for item in response['Items']:
                users_prompt[item['user_id']] = item['prompt']
            return users_prompt

        except ClientError as err:
            self._handle_error("get_user", err)

    def get_log(self, user: User, n: int = 10):
        """
        Get an user's log from log table.
        """
        try:
            condition = Key('user_id').eq(user.user_id)

            response = self.db.log_table.query(
                KeyConditionExpression=condition,
                Limit=n,
                ScanIndexForward=False
            )
            items = response['Items']
            return items

        except ClientError as err:
            self._handle_error("get_user", err)

    def write_log(self, log: Log):
        """
        Write log to log table.
        """
        try:
            response = self.db.log_table.put_items(Item=log.to_item)
            logger.info("PutItem succeeded: %s", response)

        except ClientError as err:
            self._handle_error("write_log", err)

    def _handle_error(self, method_name: str, err: ClientError):
        """
        Handle errors.

        Params:
            method_name: The name of the method where the error occurred.
            err: The ClientError instance containing error details.
        """
        logger.error(
            "Meet exception on %s: %s",
            method_name, err.response['Error']['Message'])

        # pylint: disable=broad-exception-raised
        raise Exception("Meet dynamoDB exception.") from err
