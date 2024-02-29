from moto import mock_aws
from src.models.dynamodb import DynamoDB
 
@mock_aws
def test_DynamoDB():
    d = DynamoDB(region_name='us-east-1')
    assert d.user_table.table_name == 'users'
    assert d.log_table.table_name == 'logs'