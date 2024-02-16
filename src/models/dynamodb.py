"""
dynamoDB connector.
"""

import boto3


class DynamoDB:
    """
    DynamoDB connector for handling interactions with Amazon DynamoDB.

    This class provides a simple interface for connecting to DynamoDB
    and obtaining instances of specific tables.
    Currently, it is designed to work with two tables: 'users' and 'logs'.
    You can modify the class to accommodate additional use cases.
    """

    def __init__(self, region_name):
        self._dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self._user_table = self._get_table('users')
        self._log_table = self._get_table('logs')

    @property
    def user_table(self):
        """The user table."""
        return self._user_table

    @property
    def log_table(self):
        """The log table."""
        return self._log_table

    def _get_table(self, table_name):
        try:
            table = self._dynamodb.Table(table_name)
            return table
        except Exception as e:
            raise ValueError(
                f"Error connecting to table '{table_name}': {e}") from e
