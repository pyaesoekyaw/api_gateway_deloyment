import json
import boto3
import os
import hashlib

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'ApiKeysTable')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    token = event.get('authorizationToken')
    
    if not token:
        print("DEBUG: No token provided in the event.")
        return generate_policy('unauthorized_user', 'Deny', event['methodArn'])

    # Hash the token
    hashed_token = hashlib.sha256(token.encode('utf-8')).hexdigest()
    
    # Log exactly what Lambda is processing
    print(f"DEBUG: Original Token received: '{token}'")
    print(f"DEBUG: Hashed Token being searched: '{hashed_token}'")
    print(f"DEBUG: Searching in Table Name: '{TABLE_NAME}'")

    try:
        response = table.get_item(Key={'ApiKey': hashed_token})
        item = response.get('Item')
        
        # Log exactly what came back from DynamoDB
        print(f"DEBUG: DynamoDB Response Item: {item}")
        
        if item:
            is_active = item.get('isActive')
            print(f"DEBUG: isActive value: {is_active} | type: {type(is_active)}")
            
            if is_active == True:
                print("DEBUG: SUCCESS! Token valid and active. Allowing access.")
                return generate_policy(f"user_{hashed_token[:8]}", 'Allow', event['methodArn'])
            else:
                print("DEBUG: FAILED. Token found, but isActive is not strictly the boolean True.")
                return generate_policy('invalid_user', 'Deny', event['methodArn'])
        else:
            print("DEBUG: FAILED. Token was NOT FOUND in the DynamoDB table.")
            return generate_policy('invalid_user', 'Deny', event['methodArn'])
            
    except Exception as e:
        print(f"DEBUG: Exception occurred querying DynamoDB: {e}")
        return generate_policy('error_user', 'Deny', event['methodArn'])

def generate_policy(principal_id, effect, resource):
    auth_response = {'principalId': principal_id}
    if effect and resource:
        auth_response['policyDocument'] = {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
    return auth_response
