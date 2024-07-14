from aws_cdk import (
  aws_lambda as _lambda,
  aws_apigateway as apigateway,
  Stack
)
from constructs import Construct

class ApiGateway(Stack):

  def __init__(self, scope: Construct, construct_id: str, import_products_fn: _lambda, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    basic_authorizer_lambda = _lambda.Function.from_function_name(self, "authFunction", "AuthFunction")

    api = apigateway.RestApi(
      self, 
      "importApi",
      rest_api_name="Import Service",
      default_cors_preflight_options={
                    "allow_origins": apigateway.Cors.ALL_ORIGINS,
                    "allow_methods": ["GET", "POST", "PUT", "DELETE"],
                    "allow_headers": apigateway.Cors.DEFAULT_HEADERS,
                  },
    )

    authorizer = apigateway.TokenAuthorizer(
      self, 'BasicAuthorizer',
      handler=basic_authorizer_lambda,
      identity_source='method.request.header.Authorization'
    )

    api.add_gateway_response(
      "UnauthorizedResponse",
      type=apigateway.ResponseType.UNAUTHORIZED,
      response_headers={
        "Access-Control-Allow-Origin": "'*'",
        "Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        "Access-Control-Allow-Methods": "'GET,POST,PUT,DELETE'",
      },
      status_code="401",
      templates={"application/json": '{"message": "Unauthorized"}'},
    )

    api.add_gateway_response(
      "ForbiddenResponse",
      type=apigateway.ResponseType.ACCESS_DENIED,
      response_headers={
        "Access-Control-Allow-Origin": "'*'",
        "Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        "Access-Control-Allow-Methods": "'GET,POST,PUT,DELETE'",
      },
      status_code="403",
      templates={"application/json": '{"message": "Forbidden"}'},
    )

    import_resource = api.root.add_resource("import")
    import_resource.add_method("GET", apigateway.LambdaIntegration(import_products_fn), authorization_type=apigateway.AuthorizationType.CUSTOM, authorizer=authorizer)