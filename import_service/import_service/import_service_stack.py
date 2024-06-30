from aws_cdk import Stack
from import_service.api_gateway import ApiGateway
from import_service.import_products_lambda import ImportServiceLambda
from constructs import Construct

class ImportServiceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_name = 'rsschool-import-bucket '

        import_products_lambda = ImportServiceLambda(self, 'ImportLambda', bucket_name)
        ApiGateway(self, 'APIGateway', import_products_fn=import_products_lambda.import_products_file)
    
