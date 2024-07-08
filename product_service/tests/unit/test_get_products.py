import json
import sys
import os
import pytest
import boto3
from moto import mock_aws
from product_service.lambda_func import product_list

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
        # Setup mock DynamoDB tables and insert mock data
        dynamodb = boto3.client('dynamodb', region_name='eu-central-1')
        
        # Create Products table
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
        
        # Insert mock data into Products table
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
            TableName='Products',
            Item={
                'id': {'S': '2'},
                'title': {'S': 'Wingspan'},
                'description': {'S': 'A competitive bird-collection, engine-building game'},
                'price': {'N': '40'},
                'img': {'S': 'wingspan.jpg'}
            }
        )

        dynamodb.put_item(
            TableName='Products',
            Item={
                'id': {'S': '3'},
                'title': {'S': 'Everdell'},
                'description': {'S': 'A charming board game of building and critters'},
                'price': {'N': '45'},
                'img': {'S': 'everdell.jpg'}
            }
        )

        dynamodb.put_item(
            TableName='Stocks',
            Item={
                'product_id': {'S': '1'},
                'count': {'N': '10'}
            }
        )

        dynamodb.put_item(
            TableName='Stocks',
            Item={
                'product_id': {'S': '2'},
                'count': {'N': '5'}
            }
        )

        dynamodb.put_item(
            TableName='Stocks',
            Item={
                'product_id': {'S': '3'},
                'count': {'N': '8'}
            }
        )
        
        yield dynamodb

def test_handler_returns_products_list(setup_environment):

    response = product_list.handler(None, None)
    
    assert response['statusCode'] == 200
    
    body = json.loads(response['body'])
    
    assert len(body) == 3  # Check if there are three products in the list
    assert body[0]['title'] == 'Terraforming Mars'
    assert body[0]['price'] == 35
    assert body[1]['title'] == 'Wingspan'
    assert body[1]['price'] == 40
    assert body[2]['title'] == 'Everdell'
    assert body[2]['price'] == 45

if __name__ == '__main__':
    pytest.main()
