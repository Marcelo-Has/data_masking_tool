import uuid
import random
from datetime import datetime, timedelta

def generate_uuid():
    """Generate a random UUID."""
    return str(uuid.uuid4())

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Function to create a row number generator based on prefix and suffix
def create_row_number_generator(prefix="ROW-", suffix=""):
    count = 1
    while True:
        yield f"{prefix}{str(count).zfill(4)}{suffix}"
        count += 1

# Helper functions for field types
def generate_row_number(prefix="ROW-", start=1):
    """Generate a row number with an optional prefix."""
    count = start
    while True:
        yield f"{prefix}{str(count).zfill(4)}"
        count += 1
