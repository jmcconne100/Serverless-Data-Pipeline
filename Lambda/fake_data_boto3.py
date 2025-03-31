import csv
import json
import random
import boto3
import os
from faker import Faker
import time

### **Configuration Class** ###
class CSVConfig:
    def __init__(self, config_list=None):
        default_values = [100, 0, 0.1]
        self.config_list = config_list if config_list else default_values

        if not isinstance(self.config_list, list) or len(self.config_list) != 3:
            raise ValueError("Config must be a list of exactly 3 items: [num_rows, num_duplicates, null_probability]")

        num_rows, num_duplicates, null_probability = self.config_list

        if not isinstance(num_rows, int) or num_rows <= 0:
            raise ValueError("num_rows must be a positive integer.")

        if not isinstance(num_duplicates, int) or not (0 <= num_duplicates <= num_rows):
            raise ValueError("num_duplicates must be an integer between 0 and num_rows.")

        if not isinstance(null_probability, float) or not (0 <= null_probability <= 1):
            raise ValueError("null_probability must be a float between 0 and 1.")

        self.num_rows = num_rows
        self.num_duplicates = num_duplicates
        self.null_probability = null_probability


### **Parent Class for CSV Generation** ###
class FakeCSVGenerator:
    def __init__(self, filename="fake_data.csv", config=CSVConfig(), schema_drift=False, data_errors=False):
        # Always write to /tmp/ in Lambda
        self.filename = os.path.join("/tmp", os.path.basename(filename))
        self.config = config
        self.schema_drift = schema_drift
        self.data_errors = data_errors
        self.fake = Faker()
        self.original_fieldnames = self.fieldnames.copy()

    def generate_csv(self):
        data = []
        for i in range(1, self.config.num_rows + 1):
            row = self.generate_row(i)
            if self.config.null_probability > 0:
                row = self.introduce_nulls(row)
            if self.data_errors:
                row = self.introduce_data_errors(row)
            data.append(row)

        if self.config.num_duplicates > 0:
            duplicates = random.choices(data, k=self.config.num_duplicates)
            data.extend(duplicates)

        random.shuffle(data)

        fieldnames = self.apply_schema_drift() if self.schema_drift else self.fieldnames

        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                cleaned_row = {col: row.get(col, "") for col in fieldnames}
                writer.writerow(cleaned_row)

        print(f"CSV file '{self.filename}' with {len(data)} rows (including duplicates) generated successfully!")

    def generate_row(self, index):
        raise NotImplementedError("Child class must implement generate_row()")

    def introduce_nulls(self, row):
        id_keys = ["Employee ID", "Transaction ID"]
        return {
            key: (value if (key in id_keys or random.random() > self.config.null_probability) else None)
            for key, value in row.items()
        }

    def introduce_data_errors(self, row):
        for key in row.keys():
            if random.random() < 0.1:
                if isinstance(row[key], int):
                    row[key] = f"{row[key]:02d}"
                elif isinstance(row[key], float):
                    row[key] = str(row[key])
                elif isinstance(row[key], str) and row[key].isdigit():
                    row[key] = int(row[key])
        return row

    def apply_schema_drift(self):
        new_fieldnames = []
        for col in self.original_fieldnames:
            if col in self.schema_variants and random.random() < 0.3:
                new_fieldnames.append(random.choice(self.schema_variants[col]))
            elif random.random() < 0.1:
                continue
            else:
                new_fieldnames.append(col)
        return new_fieldnames if new_fieldnames else self.original_fieldnames


### **Child Classes** ###
class FakeEmployeeData(FakeCSVGenerator):
    fieldnames = ["Employee ID", "Full Name", "Department", "Salary", "Hire Date", "Email"]

    schema_variants = {
        "Full Name": ["Full_Name", "fullName", "FullName"],
        "Email": ["email", "Email_Address", "EmailAddress"],
        "Phone Number": ["Phone", "phone_number", "ContactNumber"],
        "Department": ["Dept", "Team", "Division"],
        "Salary": ["Annual_Salary", "BasePay"],
    }

    def generate_row(self, index):
        return {
            "Employee ID": f"EMP{index:05d}",
            "Full Name": self.fake.name(),
            "Department": random.choice(["HR", "IT", "Finance", "Marketing", "Operations"]),
            "Salary": round(random.uniform(40000, 120000), 2),
            "Hire Date": self.fake.date_between(start_date="-10y", end_date="today").isoformat(),
            "Email": self.fake.company_email(),
        }


class FakeTransactionData(FakeCSVGenerator):
    fieldnames = ["Transaction ID", "User ID", "Amount", "Transaction Type", "Timestamp"]

    schema_variants = {
        "Transaction ID": ["Txn_ID", "TransactionID"],
        "User ID": ["User_ID", "CustomerID"],
        "Amount": ["TotalAmount", "TransactionAmount"],
        "Transaction Type": ["Type", "TxnType"],
    }

    def generate_row(self, index):
        return {
            "Transaction ID": f"TXN{index:06d}",
            "User ID": f"USR{random.randint(1000, 9999)}",
            "Amount": round(random.uniform(10, 5000), 2),
            "Transaction Type": random.choice(["Credit", "Debit", "Refund", "Withdrawal"]),
            "Timestamp": self.fake.date_time_this_year().isoformat(),
        }


DATASET_CLASSES = {
    "employee": FakeEmployeeData,
    "transaction": FakeTransactionData
}

def load_config_from_json(json_string):
    try:
        data = json.loads(json_string)

        filename = data.get("filename", "default.csv")
        config_values = data.get("config", {})
        schema_drift = data.get("schema_drift", False)
        data_errors = data.get("data_errors", False)
        dataset_type = data.get("dataset_type", "employee")

        config = CSVConfig([
            config_values.get("num_rows", 100),
            config_values.get("num_duplicates", 0),
            config_values.get("null_probability", 0.1)
        ])

        dataset_class = DATASET_CLASSES.get(dataset_type)
        if not dataset_class:
            raise ValueError(f"Invalid dataset type: {dataset_type}")

        return dataset_class(filename, config, schema_drift, data_errors)

    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return None

def lambda_handler(event, context=None):
    if isinstance(event, str):
        generator = load_config_from_json(event)
    else:
        generator = load_config_from_json(json.dumps(event))

    if not generator:
        return {
            "statusCode": 400,
            "body": "Invalid input JSON or configuration"
        }

    generator.generate_csv()

    s3_bucket = event.get("s3_bucket")
    s3_key = event.get("s3_key", os.path.basename(generator.filename))
    print(f"Using s3_bucket:{s3_bucket} and s3_key{s3_key}")

    if not s3_bucket:
        return {
            "statusCode": 400,
            "body": "Missing required S3 bucket name in 's3_bucket'"
        }

    try:
        s3 = boto3.client("s3")
        print("Uploading to S3...")
        start = time.time()
        with open(generator.filename, "rb") as f:
            s3.upload_fileobj(f, s3_bucket, s3_key)
        end = time.time()
        print(f"Upload done in {end - start:.2f} seconds")

        return {
            "statusCode": 200,
            "body": f"CSV file uploaded to s3://{s3_bucket}/{s3_key}"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error uploading to S3: {str(e)}"
        }
