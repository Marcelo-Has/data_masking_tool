import faker
from app.utils import generate_uuid

# Initialize Faker for generating fake data
fake = faker.Faker()

# Define available field types with configuration options
FIELD_TYPES = {
    "Name": lambda: fake.name(),
    "Full Name": lambda: fake.name(),
    "Address": lambda: fake.address(),
    "Phone": lambda: fake.phone_number(),
    "Email": lambda: fake.email(),
    "UUID": generate_uuid,
    "Company": lambda: fake.company(),
    "Department": lambda: fake.job(),
    "City": lambda: fake.city(),
    "Country": lambda: fake.country(),
    "Zip Code": lambda: fake.zipcode(),
    "Product Name": lambda: fake.catch_phrase(),
    "State or Province": lambda: fake.state(),
}
