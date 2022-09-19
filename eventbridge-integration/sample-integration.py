import boto3
import json

def event_bridge_permissions(rolename='EventBridgeLambdaPermission'):
    # To allow EventBridge to call a Lambda function,
    # Let’s create a role for Lambda and give it the
    # ‘CloudWatchEventsFullAccess’ and ‘AWSLambda_FullAccess’
    # permissions.
    iam = boto3.client('iam')
    role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            },
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "events.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    iam.create_role(
        RoleName=rolename,
        AssumeRolePolicyDocument=json.dumps(role_policy),
    )


def add_schedule(id, lambda_name, lambda_arn, role_name):
    # CRON expression
    # Minute Hour Day Month WeekDay Year
    expression = "cron(10 10 10 10 ? 2022)"

    #JSON WITH PARAMETER TO PROVISIONING THE SERVICE CATALOG PRODUCT
    provisioning_parameters = {
      "ProvisionedProductName": "A_UNIQUE_NAME",
      "ProductId": "prod-########",
      "ArtifactId": "pa-#########",
      "InstanceType": "t2.micro",
      "Quantity": "5",
      "GuacamoleParent": "1",
      "UserData": "s3://S3_BUCKET_NAME/linux-user-data.sh",
      "KeyPair": "A_KEY_PAR",
      "RemoteAccessCIDR": "172.31.0.0/20",
      "VPC": "vpc-########",
      "Subnet": "subnet-#########",
      "InstanceOverride1": "t3.medium",
      "InstanceOverride2": "t3.small",
      "InstanceOverride3": "t3.large",
      "InstanceOverride4": "t2.small",
      "InstanceOverride5": "t2.medium",
      "Users": "",
      "S3TemplateBucketName": "S3_BUCKET_NAME"
    }

    iam_client = boto3.client('iam')
    client = boto3.client('events')
    lambda_client = boto3.client('lambda')
    role = iam_client.get_role(RoleName=role_name)
    rule_id = f'ScheduleRule{id}'
    rule = client.put_rule(
        Name=rule_id,
        ScheduleExpression=expression,
        State="ENABLED",
        RoleArn=role['Role']['Arn']
	)
    lambda_client.add_permission(
	    FunctionName=lambda_name,
	    StatementId=f"Statement{id}",
	    Action="lambda:InvokeFunction",
	    Principal="events.amazonaws.com",
	    SourceArn=rule["RuleArn"]
	)
    #
    client.put_targets(
	    Rule=rule_id,
        Targets=[
	        {
		        "Id": f"Target{id}",
		        "Arn": lambda_arn,
                "Input": json.dumps(provisioning_parameters)
	        }
	    ]
	)

def remove_schedule(id, lambda_name):
    client = boto3.client('events')
    lambda_client = boto3.client('lambda')
    #
    rule_id = f'ScheduleRule{id}'
    target_id = f'Target{id}'
    client.remove_targets(Rule=rule_id, Ids=[target_id])
    client.delete_rule(Name=rule_id)
    lambda_client.remove_permission(
        FunctionName=lambda_name,
	    StatementId=f"Statement{id}",
    )
