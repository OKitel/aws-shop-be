import os
import base64

def handler(event, context):
  print('Auth event', event)
  
  authorization_header = event['authorizationToken']

  if not authorization_header:
    return {
      'statusCode': 401,
      'body': 'Unauthorized'
    }
  
  encoded_credentials = authorization_header.split(' ')[1]
  decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
  username, password = decoded_credentials.split('=')
  password = password.strip()

  stored_password = os.getenv(username)

  if stored_password and stored_password == password:
    return generatePolicy(username, 'Allow', event['methodArn'])
  else:
    return {
      'statusCode': 403,
      'body': 'Forbidden'
    }
  
def generatePolicy(principalId, effect, resource):
  authResponse = {}
  authResponse['principalId'] = principalId
  if(effect and resource):
    policyDocument = {}
    policyDocument['Version'] = '2012-10-17'
    policyDocument['Statement'] = []
    statementOne = {}
    statementOne['Action'] = 'execute-api:Invoke'
    statementOne['Effect'] = effect
    statementOne['Resource'] = resource
    policyDocument['Statement'] = [statementOne]
    authResponse['policyDocument'] = policyDocument

  return authResponse
