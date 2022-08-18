# AWS Integration for Apache Guacamole

This repository is a walk through of scripts that were made to quickly set up an automated VDI - Virtual Desktop Infrastructure - using the [Apache Guacamole](https://guacamole.apache.org/) using Amazon EC2 Spot Instances.

<p align="center">
<img src="/images/EAD-FireTV-blogpost.png" width="550">
</p>

## Requirements

This demo is configured to run in `sa-east-1`. If you need to run it in a different region, edit the `AWS_REGION` variable in all the scripts.

You will need:

- VPC with one public subnet and one or two private subnets, a NAT Gateway and/or Proxy or the AWS Network Firewall
- Apache Guacamole installed
- Guacamole API Credentials
- S3 Bucket shared with the Organization or Account with the AWS Service Catalog Products
- A domain or subdomain

### Demo walkthrough

1. Apache Guacamole setup:<br>
  a) install Guacamole in EC2 instances or ECS/Fargate containers<br>
  b) configure a domain or subdomain in the Route53 or your DNS <br>
  c) configure the domain and validate in ACM - Amazon Certificate Manager<br>
  d) setup ALB to listen in 443 port and attach the Certificate from ACM<br>
  e) configure a target group point to Guacamole instances<br>
  f) create a Guacamole API user <br>
2. Create S3 BUCKET to save [Service Catalog Templates files and the Userdata scripts](servicecatalog-templates)
3. Run the solution [cloudformation script vdi-automated-solution.yaml](scripts)
4. Now just scheduele an Eventbridge Rule with a target to Lambdas functions to Add and Remove EC2 instances, see a [sample here](eventbridge-integration) 


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
