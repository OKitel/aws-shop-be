import json
import boto3
import os
import uuid

dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns', region_name='eu-central-1')

def handler(event, context):
    dynamodb = boto3.client('dynamodb', 'eu-central-1')
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    products_table_name = 'Products'
    stocks_table_name = 'Stocks'

    required_fields = ['title', 'description', 'price', 'count']

    for record in event['Records']:
        record = json.loads(record['body'])

        for field in required_fields:
            if field not in record:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'{field} is required'})
                }
        
        product_id = str(uuid.uuid4())

        new_product = {
            'id': {'S': product_id},
            'title': {'S': record['title']},
            'description': {'S': record['description']},
            'price': {'N': str(record['price'])}
        }

        new_count = {
            'product_id': {'S': product_id},
            'count': {'N': str(record['count'])}
        }

        sns_product = {
            'id': product_id,
            'title': record['title'],
            'description': record['description'],
            'price': record['price'],
            'count': record['count']
        }

        product_item = {
            'Put': {
                'TableName': products_table_name,
                'Item': new_product
            }
        }

        stock_item = {
            'Put': {
                'TableName': stocks_table_name,
                'Item': new_count
            }
        }

        try:
            dynamodb.transact_write_items(
                TransactItems=[product_item, stock_item]
            )
            response = sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=json.dumps(sns_product),
                MessageAttributes={
                    'price': {
                        'DataType': 'Number',
                        'StringValue': str(sns_product['price'])
                    }
                }
            )
            print(f"Message sent to SNS topic: {response['MessageId']}")
        except Exception as e:
            print(f"Error writing to DynamoDB: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        },
        'body': json.dumps('Batch processed successfully')
    }
