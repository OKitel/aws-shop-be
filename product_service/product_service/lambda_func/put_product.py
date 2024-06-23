import json
import os
import boto3
import uuid

def handler(event, context):
    print("CREATE product request. Body: ", event.get('body'))

    try:
      product_data = json.loads(event['body'])

      dynamodb = boto3.client('dynamodb', region_name=os.getenv('AWS_REGION'))

      products_table_name = os.getenv('PRODUCTS_TABLE_NAME')
      stocks_table_name = os.getenv('STOCKS_TABLE_NAME')

      product_id = str(uuid.uuid4())

      product_item = {
        'Put': {
          'TableName': products_table_name,
          'Item': {
            'id': {'S': product_id},
            'title': {'S': product_data['title']},
            'price': {'N': str(product_data['price'])},
            'description': {'S': product_data['description']},
            'img': {'S': product_data.get('img')}
          }
        }
      }

      stock_item = {
        'Put': {
          'TableName': stocks_table_name,
          'Item': {
            'product_id': {'S': product_id},
            'count': {'N': str(product_data['count'])},
          }
        }
      }

      dynamodb.transact_write_items(
        TransactItems=[product_item, stock_item]
      )

      return {
          'statusCode': 200,
          "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "content-type": "application/json"
          },
          'body': json.dumps({
              'message': 'Product created successfully',
              'productId': product_id
          })
      }
    
    except KeyError as e:
      return {
          'statusCode': 400,
          "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "content-type": "application/json"
          },
          'body': json.dumps({'error': f'Provided products data invalid: {str(e)}'})
      }

    except Exception as e:
      return {
          'statusCode': 500,
          "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "content-type": "application/json"
          },
          'body': json.dumps({'error': f'An error occurred: {str(e)}'})
      }
