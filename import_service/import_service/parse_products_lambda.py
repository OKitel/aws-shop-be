from aws_cdk import (
  Stack,
  aws_lambda as _lambda,
  aws_s3 as s3,
  aws_s3_notifications as s3n,
  aws_sqs as sqs,
)
import boto3

from constructs import Construct

class ParseFileLambda(Stack):

  def __init__(self, scope: Construct, id: str, bucket_name: str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    bucket = s3.Bucket.from_bucket_name(self, 'ImportBucket', bucket_name)
    
    sqs_client = boto3.client('sqs')

    response = sqs_client.get_queue_url(QueueName='catalogItemsQueue')

    queue_url = response['QueueUrl']

    response = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['QueueArn'])

    queue_arn = response['Attributes']['QueueArn']

    queue = sqs.Queue.from_queue_arn(self, 'InstanceQueue', queue_arn=queue_arn)

    self.import_file_parser = _lambda.Function(
      self, "ImportFileParser",
      runtime=_lambda.Runtime.PYTHON_3_11,
      handler="parse_file.handler",
      code=_lambda.Code.from_asset("import_service/lambda_func/"),
      environment={
        "BUCKET_NAME": bucket.bucket_name,
      }
    )

    bucket.grant_put(self.import_file_parser)
    bucket.grant_read_write(self.import_file_parser)
    bucket.grant_delete(self.import_file_parser)

    notification = s3n.LambdaDestination(self.import_file_parser)
    bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification, s3.NotificationKeyFilter(prefix="uploaded/"))
    queue.grant_send_messages(self.import_file_parser)