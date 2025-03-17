import csv
from faker import Faker
import random

class FakeCSVGenerator:
    """
    Parent class responsible for generating a CSV file using Faker.
    Child classes should define `fieldnames` and implement `generate_row()`.
    """

    def __init__(self, filename="fake_data.csv", num_rows=100):
        self.filename = filename
        self.num_rows = num_rows
        self.fake = Faker()

    def generate_csv(self):
        """
        Generates a CSV file with fake data using the child class's defined structure.
        """
        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()

            for i in range(1, self.num_rows + 1):
                writer.writerow(self.generate_row(i))

        print(f"CSV file '{self.filename}' with {self.num_rows} rows generated successfully!")

    def generate_row(self, index):
        """
        Child classes should override this method to define their specific row structure.
        """
        raise NotImplementedError("Child class must implement generate_row()")


### 1. Employee Records ###
class FakeEmployeeData(FakeCSVGenerator):
    fieldnames = ["Employee ID", "Full Name", "Department", "Salary", "Hire Date", "Email"]

    def generate_row(self, index):
        return {
            "Employee ID": f"EMP{index:05d}",
            "Full Name": self.fake.name(),
            "Department": random.choice(["HR", "IT", "Finance", "Marketing", "Operations"]),
            "Salary": round(random.uniform(40000, 120000), 2),
            "Hire Date": self.fake.date_between(start_date="-10y", end_date="today").isoformat(),
            "Email": self.fake.company_email(),
        }


### 2. Product Catalog ###
class FakeProductData(FakeCSVGenerator):
    fieldnames = ["Product ID", "Product Name", "Category", "Price", "Stock Quantity"]

    def generate_row(self, index):
        return {
            "Product ID": f"PROD{index:05d}",
            "Product Name": self.fake.word().capitalize(),
            "Category": random.choice(["Electronics", "Clothing", "Food", "Books", "Furniture"]),
            "Price": round(random.uniform(5, 500), 2),
            "Stock Quantity": random.randint(0, 1000),
        }


### 3. Financial Transactions ###
class FakeTransactionData(FakeCSVGenerator):
    fieldnames = ["Transaction ID", "User ID", "Amount", "Transaction Type", "Timestamp"]

    def generate_row(self, index):
        return {
            "Transaction ID": f"TXN{index:06d}",
            "User ID": f"USR{random.randint(1000, 9999)}",
            "Amount": round(random.uniform(10, 5000), 2),
            "Transaction Type": random.choice(["Credit", "Debit", "Refund", "Withdrawal"]),
            "Timestamp": self.fake.date_time_this_year().isoformat(),
        }


### 4. Online User Accounts ###
class FakeUserData(FakeCSVGenerator):
    fieldnames = ["User ID", "Username", "Email", "Signup Date", "Last Login", "Account Status"]

    def generate_row(self, index):
        return {
            "User ID": f"USR{index:05d}",
            "Username": self.fake.user_name(),
            "Email": self.fake.email(),
            "Signup Date": self.fake.date_between(start_date="-5y", end_date="today").isoformat(),
            "Last Login": self.fake.date_time_this_year().isoformat(),
            "Account Status": random.choice(["Active", "Inactive", "Suspended"]),
        }


### 5. Healthcare Patient Records (Non-Sensitive) ###
class FakeHealthcareData(FakeCSVGenerator):
    fieldnames = ["Patient ID", "Full Name", "Age", "Blood Type", "Doctor", "Last Visit"]

    def generate_row(self, index):
        return {
            "Patient ID": f"PAT{index:06d}",
            "Full Name": self.fake.name(),
            "Age": random.randint(18, 90),
            "Blood Type": random.choice(["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]),
            "Doctor": f"Dr. {self.fake.last_name()}",
            "Last Visit": self.fake.date_between(start_date="-2y", end_date="today").isoformat(),
        }


### Example Usage ###
if __name__ == "__main__":
    datasets = {
        "fake_employees.csv": FakeEmployeeData,
        "fake_products.csv": FakeProductData,
        "fake_transactions.csv": FakeTransactionData,
        "fake_users.csv": FakeUserData,
        "fake_healthcare.csv": FakeHealthcareData,
    }

    for filename, cls in datasets.items():
        generator = cls(filename, num_rows=50)
        generator.generate_csv()
