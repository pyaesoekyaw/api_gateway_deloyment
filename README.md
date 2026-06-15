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
VPCFullAccess

Step 3: Write the Lambda Authorizer Code
Go to the Lambda Console -> Create function.

Choose Author from scratch, name it ApiGatewayAuthorizer, choose Python 3.12 (or your preferred version), and assign the IAM role you just created.

Under Advanced settings (or Configuration -> VPC), attach the function to your VPC, selecting the Private Subnets shown in your diagram, and assign a Security Group that allows outbound HTTPS traffic.

Replace the default code with the following Python script: Lambda_authorizer.py

Go to the Configuration tab.

Click General configuration on the left.

Click Edit.

Change the Timeout from 3 seconds to 10 seconds.

Click Save.

How to Create a DynamoDB VPC Endpoint
Step 1: Navigate to Endpoints

Open the AWS VPC Console.

On the left-hand navigation pane, scroll down and click on Endpoints.

Click the orange Create endpoint button.

Step 2: Configure the Endpoint

Name tag: Give it a name like DynamoDB-Endpoint.

Service category: Leave it as AWS services.

Services: In the search box, type dynamodb and press Enter.

Type: Gateway
Step 3: Attach to Your Network

VPC: Select the VPC where your Lambda Authorizer is running.

Route tables: private route table

Step 4: Configure API Gateway
Now you need to tell API Gateway to use this function.  

Go to the API Gateway Console and select your API.  

In the left menu, click Authorizers -> Create New Authorizer.  

Name: MyCustomAuthorizer.  

Type: Lambda.  

Lambda Function: Select the ApiGatewayAuthorizer function you just created.
Lambda Event Payload: Token
Token source : authorizationToken

Click Create and test it directly in the console using your test token.
