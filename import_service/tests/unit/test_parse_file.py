import os
import boto3
import pytest
import json
from moto import mock_aws
from import_service.lambda_func import parse_file

# Fixture to set up environment variables for AWS credentials
@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'

# Fixture to set up the mocked S3 and SQS environment
@pytest.fixture
def aws_services(aws_credentials):
    with mock_aws():
        s3 = boto3.client('s3', region_name='eu-central-1')
        sqs = boto3.client('sqs', region_name='eu-central-1')

        bucket_name = 'test-aws-import-bucket'
        os.environ['BUCKET_NAME'] = bucket_name

        # Create the bucket
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
            'LocationConstraint': 'eu-central-1'
        })

        # Create the SQS queue
        queue_url = sqs.create_queue(QueueName='catalogItemsQueue')['QueueUrl']
        queue_arn = sqs.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=['QueueArn']
        )['Attributes']['QueueArn']

        os.environ['SQS_QUEUE_URL'] = queue_url
        os.environ['SQS_QUEUE_ARN'] = queue_arn

        yield s3, sqs

def test_parse_file_lambda(aws_services):
    s3, sqs = aws_services
    bucket_name = os.environ['BUCKET_NAME']

    # Upload a test CSV file to the 'uploaded' folder
    csv_content = "title,description,price,count\nCatan,Catan description,45,150\nPandemic,Pandemic description,40,200"
    s3.put_object(Bucket=bucket_name, Key='uploaded/test-file.csv', Body=csv_content)

    # Define the event to simulate the S3 trigger
    event = {
        'Records': [
            {
                's3': {
                    'bucket': {
                        'name': bucket_name
                    },
                    'object': {
                        'key': 'uploaded/test-file.csv'
                    }
                }
            }
        ]
    }

    parse_file.handler(event, None)

    # Check if the file was copied to the 'parsed' folder
    copied_object = s3.get_object(Bucket=bucket_name, Key='parsed/test-file.csv')
    assert copied_object['Body'].read().decode('utf-8') == csv_content

    # Check if the original file was deleted
    with pytest.raises(s3.exceptions.NoSuchKey):
        s3.get_object(Bucket=bucket_name, Key='uploaded/test-file.csv')

    # Check if the messages were sent to SQS
    messages = sqs.receive_message(QueueUrl=os.environ['SQS_QUEUE_URL'], MaxNumberOfMessages=10)
    assert 'Messages' in messages
    message_bodies = [json.loads(msg['Body']) for msg in messages['Messages']]
    expected_messages = [
        {'title': 'Catan', 'description': 'Catan description', 'price': '45', 'count': '150'},
        {'title': 'Pandemic', 'description': 'Pandemic description', 'price': '40', 'count': '200'}
    ]
    assert message_bodies == expected_messages

if __name__ == '__main__':
    pytest.main()