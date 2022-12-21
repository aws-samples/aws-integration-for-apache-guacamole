# AWS Integration for Apache Guacamole

This repository is a walk through of scripts that were made to quickly set up an automated VDI - Virtual Desktop Infrastructure - using the [Apache Guacamole](https://guacamole.apache.org/) using Amazon EC2 Spot Instances.

This sample is an AWS automation to integrate with Apache Guacamole using Eventbridge Rules and Lambda Functions to detect EC2 events in the VPC and create or remove connections in the Guacamole 

<p align="center">
<img src="/images/EAD-FireTV-blogpost.png" width="550">
</p>

## Requirements

You will need:

- VPC with one public subnet and one or two private subnets, a NAT Gateway and/or Proxy or the AWS Network Firewall
- Apache Guacamole installed
- Guacamole API Credentials (User and Password)
- S3 Bucket shared with the Organization or Account with the AWS Service Catalog Products
- A domain or subdomain

### Demo walkthrough

1. Apache Guacamole setup:<br>
  a) install Guacamole in EC2 instances or ECS/Fargate containers<br>
  b) configure a domain or subdomain in the Route53 or your DNS <br>
  c) In the ACM - Amazon Certificate Manager configure the domain/subdomain and validate it in the Route 53/DNS <br>
  d) Create a target group in the 8080 port with the Apache Guacamole instances or ECS cluster<br>
  e) setup ALB to listen in 443 port, attach the Certificate from ACM and the target group<br>
  g) create a Guacamole API user <br>
2. Create S3 BUCKET to save [Service Catalog Templates files and the Userdata scripts](servicecatalog-templates)
3. Create two secure Parameters (SecureString with default account KMS key) inside the AWS System Manager<br>
  a) "guacaApiPassword" with the Apache Guacamole API password <br>
  b) "developerUserPassword" with a MS Windows password<br>
5. Run the solution [cloudformation script vdi-automated-solution.yaml](scripts)
6. Now just scheduele an Eventbridge Rule with a target to Lambda functions to **create (CreateProductScheduledbyEventBridge)** and **Remove (DeleteProductScheduledbyEventBridge)** Service Catalog products. Here you can find a python sample to create the Eventbridge Rules [sample here](eventbridge-integration) 

### Multi-Account Environment

There are aways to work in a multi-account environment, for example, using CloudFormation StackSet, creating Eventbridge Rules in each account, etc. But we tested one solution using the SNS Topic in the managemnent account as a EventBridge Rule Target and subscribe the provisioning Lambda functions in the child accounts.<br>

1. Read and follow this documentation https://docs.aws.amazon.com/lambda/latest/dg/with-sns-example.html<br>
2. Create the SNS Topic (account A)<br>
3. Create the lambda function (account B)<br>
4. Create cross-acount roles<br>
5. From the LMS Create the EnventBridge Rule with the SNS Topic as a target<br>

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
