import json
import os
import boto3
import uuid

def handler(event, context):
    try:
      product_data = json.loads(event['body'])

      dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))

      products_table_name = os.getenv('PRODUCTS_TABLE_NAME')
      stocks_table_name = os.getenv('STOCKS_TABLE_NAME')

      products_table = dynamodb.Table(products_table_name)
      stocks_table = dynamodb.Table(stocks_table_name)

      product_id = str(uuid.uuid4())

      product = {
        'id': product_id,
        'title': product_data['title'],
        'price': product_data['price'],
        'description': product_data['description'],
        'img': product_data.get('img')
      }

      products_table.put_item(Item=product)
      stocks_table.put_item(Item={
        'product_id': product_id,
        'count': product_data['count']
      })

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
