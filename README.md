# api_gateway_deloyment
Step 1: Set Up Your DynamoDB Table
Before the Lambda function can verify anything, it needs a place to check the keys.

Go to the DynamoDB Console in AWS.

Click Create table.
Table name: ApiKeysTable (or a name of your choice).
Partition key (Hash Key): ApiKey (String).
Leave settings as default and click Create table.
Once created, add a test item. Click Explore table items -> Create item. Set ApiKey to my-secret-hash-token and add a boolean attribute isActive set to true.

Step 2: Create the IAM Role for Your Lambda
Your Lambda needs permission to read from DynamoDB, write logs to CloudWatch, and run inside a VPC.
Go to the IAM Console -> Roles -> Create role.
Select AWS Service -> Lambda.
Attach the following policies:
AWSLambdaVPCAccessExecutionRole (Required because your diagram shows Lambda in a Private Subnet).
AmazonDynamoDBReadOnlyAccess (To read the hash keys).
VPCNetwork

Step 3: Write the Lambda Authorizer Code
Go to the Lambda Console -> Create function.

Choose Author from scratch, name it ApiGatewayAuthorizer, choose Python 3.12 (or your preferred version), and assign the IAM role you just created.

Under Advanced settings (or Configuration -> VPC), attach the function to your VPC, selecting the Private Subnets shown in your diagram, and assign a Security Group that allows outbound HTTPS traffic.

Replace the default code with the following Python script:
