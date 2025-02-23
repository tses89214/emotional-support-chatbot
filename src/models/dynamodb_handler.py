# pylint: disable=missing-module-docstring
import logging
import time
from typing import List, Dict, Union

from boto3.dynamodb.conditions import Key

from src.models.user import User
from src.models.log import Log
from src.models.prompt import Prompt
from src.models.dynamodb_connector import DynamoDBConnector

logger = logging.getLogger(__name__)


class DynamoDBHandler:
    """
    A class for reading and writing data to DynamoDB,
    included user and log.
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
        Get user's profile from user table, including id and prompt.

        Params:
            user_id (str): user's id.
        """
        response = self.db.user_table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        if response['Items']:
            item = response['Items'][0]
            return True, User(
                user_id=item['user_id'], create_at=item['create_at'], status=item['status'])
        else:
            return False, None

    def add_user(self, user: User) -> bool:
        """
        Add user to user table. If user_id exists, record will be overwrite.

        Params:
            user (User): an User object.
        """
        response = self.db.user_table.put_item(Item=user.to_item())
        logger.info("PutItem succeeded: %s", response)
        return True

    def get_log(self, user: User, n: int = 10) \
            -> List[Dict[str, Union[str, int]]]:
        """
        Get n records of an user' from log table.

        Params:
            user (User): an User object.
            n (int): number of record we want to get. Default is 10.

        Returns:
            log of an user (List of Dict), like:
            [{
                "user_id":"abc",
                "timestamp":123456,
                "input":"你是誰",
                "output":"我是 ChatGPT",
                "prompt":"你是有禮貌的機器人"
            }]
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

    def get_prompt(self, user: User) -> Prompt:
        """
        Get prompt from prompt table.

        Params:
            user (User): an User object.
        """
        response = self.db.prompt_table.query(
            KeyConditionExpression=Key('user_id').eq(user.user_id)
        )
        if response['Items']:
            item = [item for item in response['Items'] if item['is_current']]
            item = item[0]
            return True, Prompt(
                user_id=item['user_id'],
                prompt=item['prompt'],
                valid_from=item['valid_from'],
                valid_to=item['valid_to'],
                is_current=item['is_current']
            )
        else:
            raise LookupError('No prompt found')

    def add_prompt(self, prompt: Prompt) -> bool:
        """
        Add prompt to prompt table.

        Params:
            prompt (Prompt): a Prompt object.
        """
        response = self.db.prompt_table.put_item(
            Item=prompt.to_item()
        )
        logger.info("PutItem succeeded: %s", response)
        return True

    def update_prompt(self, new_prompt: Prompt) -> bool:
        """
        Update prompt to prompt table.
            1. Get old prompt
            2. update its `is_current` value as False, `valid_to` as now time.
            3. put it back
            4. then put new prompt

        Params:
            new_prompt (Prompt): a Prompt object.
        """
        reponse = self.db.prompt_table.query(
            KeyConditionExpression=Key('user_id').eq(new_prompt.user_id)
        )
        print(reponse)
        old_prompt = [item for item in reponse['Items']
                      if item['is_current']]
        old_prompt = old_prompt[0]
        if old_prompt:
            old_prompt = Prompt(
                user_id=old_prompt['user_id'],
                prompt=old_prompt['prompt'],
                valid_from=old_prompt['valid_from'],
                valid_to=int(time.time()),
                is_current=False
            )
            self.db.prompt_table.put_item(
                Item=old_prompt.to_item()
            )
            self.add_prompt(new_prompt)
        else:
            raise LookupError('No prompt found')
