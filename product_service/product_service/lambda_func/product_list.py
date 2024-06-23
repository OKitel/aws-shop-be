import json
import os
import boto3

BASE_URL = "https://d266s2h0r1qt2p.cloudfront.net/assets/img/"

def handler(event, context):
  
  try:
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))

    products_table_name = os.getenv('PRODUCTS_TABLE_NAME')
    stocks_table_name = os.getenv('STOCKS_TABLE_NAME')

    products_table = dynamodb.Table(products_table_name)
    stocks_table = dynamodb.Table(stocks_table_name)

    products_response = products_table.scan()
    products_items = products_response.get('Items', [])

    stocks_response = stocks_table.scan()
    stocks_items = stocks_response.get('Items', [])

    product_dict = {item['id']: item for item in products_items}

    for stock_item in stocks_items:
      product_id = stock_item['product_id']
      if product_id in product_dict:
        product_dict[product_id]['count'] = str(stock_item['count'])
        product_dict[product_id]['price'] = str(product_dict[product_id]['price'])
        product_dict[product_id]['title'] = str(product_dict[product_id]['title'])
        product_dict[product_id]['description'] = str(product_dict[product_id]['description'])
        product_dict[product_id]['img'] = BASE_URL + str(product_dict[product_id]['img'])
      else:
        product_dict[product_id] = {
          'id': product_id,
          'count': str(stock_item['count'])
        }

    products = list(product_dict.values())
    
    return {
      "statusCode": 200,
      "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "content-type": "application/json"
      },
      "body": json.dumps(products)
    }
  
  except Exception as e:
    return {
      'statusCode': 500,
      "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "content-type": "application/json"
      },
      'body': json.dumps({'error': str(e)})
    }