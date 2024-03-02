from moto import mock_aws
from src.models.dynamodb_connector import DynamoDBConnector
 
@mock_aws
def test_dynamodb_connector():
    d = DynamoDBConnector(region_name='us-east-1')
    assert d.user_table.table_name == 'users'
    assert d.log_table.table_name == 'logs'