import csv
from faker import Faker

def generate_fake_csv(filename="fake_data.csv", num_rows=100):
    """
    Generates a CSV file with fake data using the Faker library.

    Args:
        filename (str): The name of the output CSV file.
        num_rows (int): The number of rows of fake data to generate.
    """

    # Initialize Faker
    fake = Faker()

    # Define the CSV column headers
    fieldnames = ["ID", "Name", "Email", "Phone Number", "Address", "Company", "Job Title", "Date of Birth"]

    # Open a CSV file for writing
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()

        # Generate fake data rows
        for i in range(1, num_rows + 1):
            writer.writerow({
                "ID": i,
                "Name": fake.name(),
                "Email": fake.email(),
                "Phone Number": fake.phone_number(),
                "Address": fake.address().replace("\n", ", "),
                "Company": fake.company(),
                "Job Title": fake.job(),
                "Date of Birth": fake.date_of_birth(minimum_age=18, maximum_age=75).isoformat(),
            })

    print(f"CSV file '{filename}' with {num_rows} rows generated successfully!")

# Example usage
generate_fake_csv("fake_data.csv", num_rows=50)
