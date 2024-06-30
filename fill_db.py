import boto3
import uuid
import json

dynamodb = boto3.resource('dynamodb')

products_table = dynamodb.Table('Products')
stocks_table = dynamodb.Table('Stocks')

def populate_tables(items):

  for item in items:
    product_id = str(uuid.uuid4())
    title = item['title']
    description = item['description']
    price = item['price']
    img = item['img']
    count = item['count']

    products_table.put_item(
      Item={
        'id': product_id,
        'title': title,
        'description': description,
        'price': price,
        'img': img
      }
    )

    stocks_table.put_item(
      Item={
        'product_id': product_id,
        'count': count
      }
    )

with open('data/products.json', 'r') as json_file:
  data = json.load(json_file)

populate_tables(data)