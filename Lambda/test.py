import csv
import random
from faker import Faker

class CSVConfig:
    """
    Configuration object for FakeCSVGenerator.
    Ensures valid values for num_rows, num_duplicates, and null_probability.
    """

    def __init__(self, config_list=None):
        # Default values
        default_values = [100, 0, 0.1]  # num_rows, num_duplicates, null_probability

        # Use provided config_list or fallback to default values
        self.config_list = config_list if config_list else default_values

        # Ensure config_list is valid
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


class FakeCSVGenerator:
    """
    Parent class for generating fake CSV data using a configuration object.
    Child classes should define `fieldnames` and implement `generate_row()`.
    """

    def __init__(self, filename="fake_data.csv", config=CSVConfig()):
        self.filename = filename
        self.config = config
        self.fake = Faker()

    def generate_csv(self):
        """
        Generates a CSV file with fake data, handling duplicates and null values if specified.
        """
        data = []
        for i in range(1, self.config.num_rows + 1):
            row = self.generate_row(i)
            if self.config.null_probability > 0:  # Apply nulls if probability > 0
                row = self.introduce_nulls(row)
            data.append(row)

        # Introduce duplicates if num_duplicates > 0
        if self.config.num_duplicates > 0:
            duplicates = random.choices(data, k=self.config.num_duplicates)
            data.extend(duplicates)

        # Shuffle data to mix duplicates randomly
        random.shuffle(data)

        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"CSV file '{self.filename}' with {len(data)} rows (including duplicates) generated successfully!")

    def generate_row(self, index):
        """
        Child classes should override this method to define their specific row structure.
        """
        raise NotImplementedError("Child class must implement generate_row()")

    def introduce_nulls(self, row):
        """
        Randomly replaces some fields in the row with None (empty value) based on `null_probability`.
        """
        return {key: (value if random.random() > self.config.null_probability else None) for key, value in row.items()}


### **1. Employee Records** ###
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


### **2. Product Catalog** ###
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


### **3. Financial Transactions** ###
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


### **4. Online User Accounts** ###
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


### **5. Healthcare Patient Records (Non-Sensitive)** ###
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


### **Example Usage** ###
if __name__ == "__main__":
    # Employee Data with 15% null probability, 10 duplicates
    employee_config = CSVConfig([50, 10, 0.15])
    employee_generator = FakeEmployeeData("fake_employees.csv", employee_config)
    employee_generator.generate_csv()

    # Product Data (No duplicates, No nulls)
    product_config = CSVConfig([50, 0, 0.0])
    product_generator = FakeProductData("fake_products.csv", product_config)
    product_generator.generate_csv()

    # Transaction Data with Some duplicates and 5% null probability
    transaction_config = CSVConfig([50, 5, 0.05])
    transaction_generator = FakeTransactionData("fake_transactions.csv", transaction_config)
    transaction_generator.generate_csv()

    # User Data with 30% null probability
    user_config = CSVConfig([50, 0, 0.30])
    user_generator = FakeUserData("fake_users.csv", user_config)
    user_generator.generate_csv()

    # Healthcare Data with 20% null probability, 5 duplicates
    healthcare_config = CSVConfig([50, 5, 0.20])
    healthcare_generator = FakeHealthcareData("fake_healthcare.csv", healthcare_config)
    healthcare_generator.generate_csv()
