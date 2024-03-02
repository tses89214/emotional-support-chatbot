#pylint: disable=missing-module-docstring
import boto3
from boto3.dynamodb import table
class DynamoDBConnector:
    """
    DynamoDB connector provides a simple interface for connecting to DynamoDB.
    Currently, it is designed to work with two tables: 'users' and 'logs'.
    You can modify the class to accommodate additional use cases.
    """
    def __init__(self, region_name: str):
        """
        Params:
            region_name (str): The region of DynamoDB.
        """
        self._dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self._user_table = self._get_table('users')
        self._log_table = self._get_table('logs')

    @property
    def user_table(self) -> table:
        """user table instance."""
        return self._user_table

    @property
    def log_table(self) -> table:
        """log table instance."""
        return self._log_table

    def _get_table(self, table_name) -> table:
        return self._dynamodb.Table(table_name)
