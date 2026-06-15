# API Gateway Deployment with Lambda Authorizer and DynamoDB

This guide explains how to configure a custom Lambda Authorizer for Amazon API Gateway using DynamoDB to validate API keys.

---

## Prerequisites

* Amazon API Gateway
* AWS Lambda
* Amazon DynamoDB
* Amazon VPC
* IAM permissions to create and manage AWS resources

---

## Step 1: Create the DynamoDB Table

The Lambda Authorizer validates API keys against records stored in DynamoDB.

### Create the Table

1. Open the **AWS DynamoDB Console**.
2. Click **Create Table**.
3. Configure the table:

| Setting       | Value             |
| ------------- | ----------------- |
| Table Name    | `ApiKeysTable`    |
| Partition Key | `ApiKey` (String) |

4. Leave the remaining settings as default.
5. Click **Create Table**.

### Add a Test Record

1. Open the newly created table.
2. Select **Explore Table Items**.
3. Click **Create Item**.
4. Add the following attributes:

```json
{
  "ApiKey": "my-secret-hash-token",
  "isActive": true
}
```

---

## Step 2: Create the IAM Role for Lambda

The Lambda Authorizer requires permissions to:

* Read API keys from DynamoDB
* Write logs to CloudWatch
* Access resources within a VPC

### Create the Role

1. Open the **IAM Console**.
2. Navigate to **Roles** → **Create Role**.
3. Select:

   * **Trusted Entity Type:** AWS Service
   * **Use Case:** Lambda
4. Attach the following policies:

* `AWSLambdaVPCAccessExecutionRole`
* `AmazonDynamoDBReadOnlyAccess`
* `VPCFullAccess`

5. Complete the role creation process.

> **Note:** For production environments, follow the principle of least privilege and avoid using broad permissions such as `VPCFullAccess`.

---

## Step 3: Create the Lambda Authorizer

### Create the Function

1. Open the **AWS Lambda Console**.
2. Click **Create Function**.
3. Select **Author from Scratch**.
4. Configure:

| Setting        | Value                      |
| -------------- | -------------------------- |
| Function Name  | `ApiGatewayAuthorizer`     |
| Runtime        | Python 3.12                |
| Execution Role | IAM role created in Step 2 |

### Configure VPC Settings

1. Open **Configuration** → **VPC**.
2. Attach the function to:

   * Your target VPC
   * Private subnets
   * A security group allowing outbound HTTPS traffic

### Deploy the Authorizer Code

Replace the default Lambda code with the contents of:

```text
Lambda_authorizer.py
```

### Increase Lambda Timeout

1. Open **Configuration** → **General Configuration**.
2. Click **Edit**.
3. Change the timeout value:

| Setting | Value      |
| ------- | ---------- |
| Timeout | 10 seconds |

4. Click **Save**.

---

## Step 4: Create a DynamoDB VPC Endpoint

Because the Lambda function runs inside private subnets, a DynamoDB VPC Endpoint is required for DynamoDB access without internet connectivity.

### Create the Endpoint

1. Open the **Amazon VPC Console**.
2. Navigate to **Endpoints**.
3. Click **Create Endpoint**.

### Configure the Endpoint

| Setting          | Value               |
| ---------------- | ------------------- |
| Name Tag         | `DynamoDB-Endpoint` |
| Service Category | AWS Services        |
| Service          | DynamoDB            |
| Endpoint Type    | Gateway             |

### Attach to the Network

| Setting      | Value                  |
| ------------ | ---------------------- |
| VPC          | Lambda VPC             |
| Route Tables | Private Route Table(s) |

4. Create the endpoint.

---

## Step 5: Configure API Gateway Authorizer

Configure API Gateway to use the Lambda function for request authorization.

### Create the Authorizer

1. Open the **API Gateway Console**.
2. Select your API.
3. Navigate to **Authorizers**.
4. Click **Create Authorizer**.

### Configure Authorizer Settings

| Setting              | Value                  |
| -------------------- | ---------------------- |
| Name                 | `MyCustomAuthorizer`   |
| Authorizer Type      | Lambda                 |
| Lambda Function      | `ApiGatewayAuthorizer` |
| Lambda Event Payload | Token                  |
| Token Source         | `authorizationToken`   |

5. Click **Create Authorizer**.

### Test the Authorizer

1. Open the newly created authorizer.
2. Click **Test**.
3. Provide a valid API key (for example, `my-secret-hash-token`).
4. Verify that authorization succeeds.

---

## Architecture Flow

```text
Client Request
      |
      v
API Gateway
      |
      v
Lambda Authorizer
      |
      v
DynamoDB (ApiKeysTable)
      |
      v
Allow / Deny Request
      |
      v
Backend Integration
```

---

## Security Recommendations

* Use least-privilege IAM permissions instead of broad managed policies.
* Store hashed API keys instead of plain-text values.
* Enable CloudWatch logging for monitoring and troubleshooting.
* Rotate API keys regularly.
* Enable API Gateway throttling and request validation where applicable.
