import os
import boto3
import pytest
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

# Fixture to set up the mocked S3 environment
@pytest.fixture
def s3(aws_credentials):
    with mock_aws():
        s3 = boto3.client('s3', region_name='eu-central-1')
        yield s3

def test_parse_file_lambda(s3):
    bucket_name = 'test-aws-import-bucket'
    
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
        'LocationConstraint': 'eu-central-1'
    })

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

    response = parse_file.handler(event, None)

    # Check if the file was read and processed
    copied_object = s3.get_object(Bucket=bucket_name, Key='parsed/test-file.csv')
    assert copied_object['Body'].read().decode('utf-8') == csv_content

    # Check if the original file was deleted
    with pytest.raises(s3.exceptions.NoSuchKey):
        s3.get_object(Bucket=bucket_name, Key='uploaded/test-file.csv')

if __name__ == '__main__':
    pytest.main()
