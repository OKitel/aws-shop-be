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
    assert body[0]['name'] == 'Terraforming Mars'
    assert body[0]['price'] == 35
    assert body[1]['name'] == 'Wingspan'
    assert body[1]['price'] == 40
    assert body[2]['name'] == 'Everdell'
    assert body[2]['price'] == 45

if __name__ == '__main__':
    pytest.main()

