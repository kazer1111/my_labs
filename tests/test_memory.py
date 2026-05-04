import io
import unittest
from unittest.mock import patch

from src.db.backend.csv_file import CsvStudentTable
from src.db.backend.errors import (
    DuplicateIDError,
    InvalidAgeError,
    InvalidStorageDataError,
    RecordNotFoundError,
)
from src.db.backend.file import FileStudentTable
from src.db.backend.memory import MemoryStudentTable
from src.db.tui import StudentTUI


class TestMemoryDatabase(unittest.TestCase):
    def setUp(self):
        self.student_table = MemoryStudentTable()

    def test_create_record(self):
        record = self.student_table.create_record(1, "John", "Doe", 20, "M")
        self.assertEqual(record, (1, "John", "Doe", 20, "M"))

    def test_create_record_duplicate_id(self):
        self.student_table.create_record(1, "John", "Doe", 20, "M")

        with self.assertRaises(DuplicateIDError):
            self.student_table.create_record(1, "Jane", "Smith", 22, "F")

    def test_create_record_negative_age(self):
        with self.assertRaises(InvalidAgeError):
            self.student_table.create_record(1, "John", "Doe", -1, "M")

    def test_select_record(self):
        self.student_table.create_record(1, "John", "Doe", 20, "M")
        self.student_table.create_record(2, "Jane", "Smith", 22, "F")
        records = self.student_table.select_record(sex="F")
        self.assertEqual(records, [(2, "Jane", "Smith", 22, "F")])

    def test_update_record(self):
        self.student_table.create_record(1, "John", "Doe", 20, "M")
        record = self.student_table.update_record(1, first_name="Petr", new_id=2)
        self.assertEqual(record, (2, "Petr", "Doe", 20, "M"))

    def test_delete_record(self):
        self.student_table.create_record(1, "John", "Doe", 20, "M")
        record = self.student_table.delete_record(1)
        self.assertEqual(record, (1, "John", "Doe", 20, "M"))

    def test_delete_record_not_found(self):
        with self.assertRaises(RecordNotFoundError):
            self.student_table.delete_record(10)

