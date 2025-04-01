# Fake Data Pipeline on AWS

This project creates a secure, event-driven data pipeline on AWS that:
- Generates fake employee data using a Lambda function
- Stores it in a KMS-encrypted S3 bucket
- Triggers an EventBridge rule on file upload
- Starts a Glue crawler via another Lambda function
- Updates the Glue Data Catalog for downstream analytics

# AWS Infrastructure Overview

```
            +---------------------------+
            |      User / Test Event    |
            +------------+--------------+
                         |
                         v
             +-----------+-----------+
             |   Lambda Function     |  (fake_data.lambda_handler)
             |   - Generates CSV     |
             |   - Uploads to S3     |
             +-----------+-----------+
                         |
                         v
          +--------------+---------------+
          |      S3: jon-data-pipeline    |
          |  - KMS Encrypted              |
          |  - Triggers EventBridge       |
          +--------------+---------------+
                         |
                         v
             +-----------+-----------+
             |    EventBridge Rule   |
             +-----------+-----------+
                         |
                         v
             +-----------+-----------+
             | Lambda: TriggerGlue   |
             | - Starts Glue Crawler |
             +-----------+-----------+
                         |
                         v
             +-----------+-----------+
             |     AWS Glue Crawler  |
             | - Scans S3 data       |
             | - Updates Glue Catalog|
             | - Athena SQL Queries  |
             +-----------+-----------+
```

# Security

- Data buckets are encrypted using a customer-managed KMS key.
- IAM roles follow least privilege (adjusted during dev/testing).
- CloudTrail logs all S3 activity for auditing and compliance.

# Key Files

- fake_data.py: Lambda script to generate fake data
- template.yaml: CloudFormation infrastructure template
- README.md: Project overview with architecture diagram

# Deployment

- Be sure to use the zipped fake_data.zip or zip up fake_data_boto3.py
- Be sure to update the faker layer to Lambda and update the cloudformation template with the correct arn
- (Option) Alternatively use a Container and deploy the Image with faker packaged to ECR
- Upload the to your S3 scripts bucket (and rename the reference in cloudformation)

# Testing

- Once deployed you can use the test.json file in Lambda to test that your system is working.