import os
import boto3
import pytest
from moto import mock_aws
from import_service.lambda_func import import_file

def test_import_file_lambda_returns_signed_url():
    bucket_name = 'test-aws-import-bucket'
    os.environ['BUCKET_NAME'] = bucket_name

    # Create a mock S3 client and bucket
    with mock_aws():
      s3 = boto3.client('s3', region_name='eu-central-1')
      s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
              'LocationConstraint': 'eu-central-1'
          })

    event = {
        'queryStringParameters': {
            'name': 'test-file.csv'
        }
    }

    response = import_file.handler(event, None)

    assert response['statusCode'] == 200
    assert 'body' in response
    assert 'https://' in response['body']

if __name__ == '__main__':
    pytest.main()
