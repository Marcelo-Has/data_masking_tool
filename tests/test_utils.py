import unittest
from app.utils import (
    generate_uuid,
    generate_random_date,
    create_row_number_generator,
    generate_row_number
)
from datetime import datetime, timedelta

class TestUtils(unittest.TestCase):

    def test_generate_uuid(self):
        uuid1 = generate_uuid()
        uuid2 = generate_uuid()
        self.assertNotEqual(uuid1, uuid2)
        self.assertEqual(len(uuid1), 36)  # Standard UUID string length
        self.assertTrue(uuid1.count('-') == 4)  # UUID has 4 hyphens

    def test_generate_random_date(self):
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 12, 31)

        for _ in range(100):
            random_date = generate_random_date(start_date, end_date)
            self.assertTrue(start_date <= random_date <= end_date)

    def test_create_row_number_generator(self):
        # Test the default prefix and suffix
        generator = create_row_number_generator()
        self.assertEqual(next(generator), "ROW-0001")
        self.assertEqual(next(generator), "ROW-0002")
        self.assertEqual(next(generator), "ROW-0003")

        # Test with custom prefix and suffix
        custom_generator = create_row_number_generator(prefix="ID-", suffix="-END")
        self.assertEqual(next(custom_generator), "ID-0001-END")
        self.assertEqual(next(custom_generator), "ID-0002-END")
        self.assertEqual(next(custom_generator), "ID-0003-END")

    def test_generate_row_number(self):
        # Test the default prefix and start
        generator = generate_row_number()
        self.assertEqual(next(generator), "ROW-0001")
        self.assertEqual(next(generator), "ROW-0002")
        self.assertEqual(next(generator), "ROW-0003")

        # Test with custom prefix and start
        custom_generator = generate_row_number(prefix="Item-", start=10)
        self.assertEqual(next(custom_generator), "Item-0010")
        self.assertEqual(next(custom_generator), "Item-0011")
        self.assertEqual(next(custom_generator), "Item-0012")


if __name__ == '__main__':
    unittest.main()
