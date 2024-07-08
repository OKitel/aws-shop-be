import os
import json
import boto3
import pytest
from moto import mock_aws
from product_service.lambda_func import catalog_batch_process

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
        # Setup mock DynamoDB
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
        
        # Setup mock SNS
        sns = boto3.client('sns', region_name='eu-central-1')
        topic_arn = sns.create_topic(Name='createProductTopic')['TopicArn']
        os.environ['SNS_TOPIC_ARN'] = topic_arn
        
        yield dynamodb, sns

@pytest.fixture
def lambda_event():
    return {
        "Records": [
            {
                "body": json.dumps({
                    "title": "Sample Product",
                    "description": "This is a sample product",
                    "price": 10.99,
                    "count": 5
                })
            }
        ]
    }

def test_handler_missing_fields(lambda_event, setup_environment):
    dynamodb, sns = setup_environment

    incomplete_event = {
        "Records": [
            {
                "body": json.dumps({
                    "title": "Sample Product",
                    "description": "This is a sample product",
                    # 'price' and 'count' are missing
                })
            }
        ]
    }

    response = catalog_batch_process.handler(incomplete_event, None)

    assert response['statusCode'] == 400
    assert 'error' in json.loads(response['body'])

def test_handler_success(lambda_event, setup_environment):
    dynamodb, sns = setup_environment

    response = catalog_batch_process.handler(lambda_event, None)

    assert response['statusCode'] == 200
    assert json.loads(response['body']) == 'Batch processed successfully'

    # Check if items are written to the DynamoDB tables
    products_response = dynamodb.scan(TableName='Products')
    stocks_response = dynamodb.scan(TableName='Stocks')

    assert len(products_response['Items']) == 1
    assert len(stocks_response['Items']) == 1

    # Check if message was published to SNS
    topics = sns.list_topics()
    assert len(topics['Topics']) == 1

if __name__ == '__main__':
    pytest.main()
