from aws_cdk import Stack
from product_service.api_gateway import ApiGateway
from product_service.get_product_by_id import ProductById
from product_service.get_products import GetProducts
from constructs import Construct

class MyCdkAppStack(Stack):
  def __init__(self, scope: Construct, id: str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    get_products_list_lbd = GetProducts(self, 'ProductsList')
    get_product_by_id_lbd = ProductById(self, 'ProductByID')
    ApiGateway(self, 'APIGateway', get_products_list_fn=get_products_list_lbd.get_products_list, get_product_by_id_fn=get_product_by_id_lbd.get_product_by_id)