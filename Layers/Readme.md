# AWS Lambda: Generate Faker Layer CloudShell

This guide shows how to package and deploy a Python Lambda function that uses `faker` to generate fake CSVs and upload them to S3 — entirely from AWS CloudShell.

## Prerequisites

- AWS account with an S3 bucket ready
- A Lambda-compatible Python script (e.g., `fake_data_boto3.py`) with a `lambda_handler(event, context)` function
- AWS CloudShell access

## Steps (Single Markdown Block)

1. Launch AWS CloudShell.

2. Create and install the faker library:
   mkdir -p faker_layer/python/lib/python3.11/site-packages
   pip install faker -t faker_layer/python/lib/python3.11/site-packages

3. CD into the directory and zip everything:
   cd faker_layer
   zip -r ../faker_layer.zip python

4. Download the zip file

5. Deploy the function via AWS Console:
   - Go to AWS Lambda > Create Function (choose Python 3.11)
   - Under Code > Upload from: choose .zip file
   - Upload function.zip
   - Click Deploy

6. From your Lambda function, scroll down to the bottom underneath the code section and add the layer.

7. Double check you've used Python 3.11

8. in your function perform 
   - import faker
   - print("faker module location:", faker.__file__)
   - print("faker contents:", dir(faker))
