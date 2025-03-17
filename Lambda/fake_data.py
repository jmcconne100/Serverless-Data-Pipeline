import csv
from faker import Faker

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


class FakePersonData(FakeCSVGenerator):
    """
    Child class that defines a specific dataset for fake person data.
    """

    fieldnames = ["ID", "Name", "Email", "Phone Number", "Address", "Company", "Job Title", "Date of Birth"]

    def generate_row(self, index):
        """
        Generates a fake row for person data.
        """
        return {
            "ID": index,
            "Name": self.fake.name(),
            "Email": self.fake.email(),
            "Phone Number": self.fake.phone_number(),
            "Address": self.fake.address().replace("\n", ", "),
            "Company": self.fake.company(),
            "Job Title": self.fake.job(),
            "Date of Birth": self.fake.date_of_birth(minimum_age=18, maximum_age=75).isoformat(),
        }


# Example usage
if __name__ == "__main__":
    person_data_generator = FakePersonData("fake_person_data.csv", num_rows=50)
    person_data_generator.generate_csv()