import json
import sys
import os
import pytest
import boto3
from moto import mock_aws
from product_service.lambda_func import product_by_id

lambda_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(lambda_dir)

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"

@pytest.fixture
def setup_environment():
    with mock_aws():
        # Setup mock DynamoDB tables
        dynamodb = boto3.client('dynamodb', region_name='eu-central-1')
        dynamodb.create_table(
            TableName='Products',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        dynamodb.create_table(
            TableName='Stocks',
            KeySchema=[{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'product_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        
        # Insert mock data
        dynamodb.put_item(
            TableName='Products',
            Item={
                'id': {'S': '1'},
                'title': {'S': 'Terraforming Mars'},
                'description': {'S': 'A board game about terraforming Mars'},
                'price': {'N': '35'},
                'img': {'S': 'terraforming_mars.jpg'}
            }
        )
        dynamodb.put_item(
            TableName='Stocks',
            Item={
                'product_id': {'S': '1'},
                'count': {'N': '10'}
            }
        )
        
        # Set environment variables
        os.environ['AWS_REGION'] = 'eu-central-1'
        os.environ['PRODUCTS_TABLE_NAME'] = 'Products'
        os.environ['STOCKS_TABLE_NAME'] = 'Stocks'
        
        yield dynamodb

def test_handler_returns_product(setup_environment):
    event = {
        'pathParameters': {
            'productId': '1'
        }
    }
    response = product_by_id.handler(event, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['title'] == 'Terraforming Mars'
    assert body['price'] == 35

def test_handler_returns_404_for_nonexistent_product(setup_environment):
    event = {
        'pathParameters': {
            'productId': '100'
        }
    }
    response = product_by_id.handler(event, None)
    assert response['statusCode'] == 404
    body = json.loads(response['body'])
    assert body == "'message': 'Product not found'"

if __name__ == '__main__':
    pytest.main()
