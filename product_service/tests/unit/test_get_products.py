import json

import sys
import os
import pytest

lambda_dir = os.path.dirname('../../product_service/lambda_func')
sys.path.append(lambda_dir)
from product_service.lambda_func import product_list

def test_handler_returns_products_list():
    response = product_list.handler(None, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body[0]['name'] == 'Product 1'
    assert body[0]['price'] == 1
    assert body[1]['name'] == 'Product 2'
    assert body[1]['price'] == 2
    assert body[2]['name'] == 'Product 3'
    assert body[2]['price'] == 3

if __name__ == '__main__':
    pytest.main()

