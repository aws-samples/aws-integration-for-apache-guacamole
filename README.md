# AWS Integration for Apache Guacamole

This repository is a walk through of scripts that were made to quickly set up an automated VDI - Virtual Desktop Infrastructure - using the [Apache Guacamole](https://guacamole.apache.org/) using Amazon EC2 Spot Instances.

This sample is an AWS automation to integrate with Apache Guacamole using Eventbridge Rules and Lambda Functions to detect EC2 events in the VPC and create or remove connections in the Guacamole 

<p align="center">
<img src="/images/EAD-FireTV-blogpost.png" width="550">
</p>

## Requirements

This demo is configured to run in `sa-east-1`. If you need to run it in a different region, edit the `AWS_REGION` variable in all the scripts.

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
3. Create two SSM secure Parameters (SecureString with default account KMS key)<br>
  a) "guacaApiPassword" with the Apache Guacamole API password <br>
  b) "developerUserPassword" with a MS Windows password<br>
5. Run the solution [cloudformation script vdi-automated-solution.yaml](scripts)
6. Now just scheduele an Eventbridge Rule with a target to Lambda functions to **create (CreateProductScheduledbyEventBridge)** and **Remove (DeleteProductScheduledbyEventBridge)** Service Catalog products. Here you can find a python sample to create the Eventbridge Rules [sample here](eventbridge-integration) 


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
