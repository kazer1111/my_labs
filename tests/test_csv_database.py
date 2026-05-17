import unittest
from pathlib import Path

from src.db.backend.csv_file import CsvStudentTable
from src.db.backend.errors import InvalidStorageDataError


class TestCsvDatabase(unittest.TestCase):
    def setUp(self):
        self.path = Path("test_students.csv")
        if self.path.exists():
            self.path.unlink()

    def tearDown(self):
        if self.path.exists():
            self.path.unlink()

    def test_data_is_saved_between_instances(self):
        first_db = CsvStudentTable(self.path)
        first_db.create_record(1, "Ivan", "Ivanov", 20, "M")

        second_db = CsvStudentTable(self.path)
        records = second_db.select_record()

        self.assertEqual(records, [(1, "Ivan", "Ivanov", 20, "M")])

    def test_select_with_filter(self):
        db = CsvStudentTable(self.path)
        db.create_record(1, "Ivan", "Ivanov", 20, "M")
        db.create_record(2, "Maria", "Petrova", 21, "F")

        records = db.select_record(sex="F")
        self.assertEqual(records, [(2, "Maria", "Petrova", 21, "F")])

    def test_update_record(self):
        db = CsvStudentTable(self.path)
        db.create_record(1, "Ivan", "Ivanov", 20, "M")
        db.update_record(1, second_name="Sidorov")

        second_db = CsvStudentTable(self.path)
        self.assertEqual(second_db.select_record(), [(1, "Ivan", "Sidorov", 20, "M")])

    def test_invalid_csv_header(self):
        self.path.write_text("id,name\n1,Ivan\n", encoding="utf-8")
        db = CsvStudentTable(self.path)

        with self.assertRaises(InvalidStorageDataError):
            db.select_record()
