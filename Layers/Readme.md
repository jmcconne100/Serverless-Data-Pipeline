# AWS Lambda: Generate Fake CSVs with Faker (from CloudShell)

This guide shows how to package and deploy a Python Lambda function that uses `faker` to generate fake CSVs and upload them to S3 — entirely from AWS CloudShell.

## Prerequisites

- AWS account with an S3 bucket ready
- A Lambda-compatible Python script (e.g., `fake_data_boto3.py`) with a `lambda_handler(event, context)` function
- AWS CloudShell access

## Steps (Single Markdown Block)

1. Launch AWS CloudShell.

2. Create and enter a working directory:
   mkdir my-lambda-faker && cd my-lambda-faker

3. Upload or create your Lambda script:
   You can use the CloudShell "Actions > Upload File" option or create it directly using:
   nano fake_data_boto3.py

4. Install the `faker` library into the current directory:
   pip install faker -t .

5. Confirm files are in place (optional):
   ls

6. Zip everything into a deployment package:
   zip -r function.zip .

7. Deploy the function via AWS Console:
   - Go to AWS Lambda > Create Function (choose Python 3.11)
   - Under Code > Upload from: choose .zip file
   - Upload function.zip
   - Click Deploy

8. Create a test event in the Lambda console with the following payload:
   {
     "filename": "fake_employees.csv",
     "s3_bucket": "your-bucket-name",
     "s3_key": "output/fake_employees.csv",
     "config": {
       "num_rows": 50,
       "num_duplicates": 5,
       "null_probability": 0.1
     },
     "schema_drift": true,
     "data_errors": true,
     "dataset_type": "employee"
   }

9. Run the test. If your Lambda has the right IAM role permissions for S3, it will generate and upload the CSV.

10. (Optional) Clean up:
    rm -rf faker* dateutil* python_dateutil* six.py* __pycache__
