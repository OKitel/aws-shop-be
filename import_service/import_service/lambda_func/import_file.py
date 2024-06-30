import os
import boto3

s3 = boto3.client('s3')

def handler(event, context):
  print('GET /import request. Parameters: ', event.get('queryStringParameters'))

  try:
    if event['queryStringParameters'] is None or 'name' not in event.get('queryStringParameters', {}):
      raise ValueError('name is required')
    
    file_name = event['queryStringParameters']['name']
      
    if not file_name:
      raise ValueError('name should not be empty')
  
    bucket_name = os.environ['BUCKET_NAME']
    key = f"uploaded/{file_name}"

    params = {
      'Bucket': bucket_name,
      'Key': key,
    }

    signed_url = s3.generate_presigned_url('put_object', Params=params)

    return {
      'statusCode': 200,
      'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'content-type': 'text/plain'
      },
      'body': signed_url
    }
  
  except ValueError as e:
    return {
          'statusCode': 400,
          "headers": {
              "Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
              "content-type": "text/plain"
          },
          'body': f'Invalid input: {str(e)}'
      }
  
  except Exception as e:
      return {
          'statusCode': 500,
          "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "content-type": "text/plain"
          },
          'body': f'An error occurred: {str(e)}'
      }