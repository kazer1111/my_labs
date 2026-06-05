import json
import unittest
from pathlib import Path

from src.db.backend.errors import InvalidStorageDataError
from src.db.backend.file import FileStudentTable


class TestFileDatabase(unittest.TestCase):
    def setUp(self):
        self.path = Path("test_students.json")
        if self.path.exists():
            self.path.unlink()

    def tearDown(self):
        if self.path.exists():
            self.path.unlink()

    def test_data_is_saved_between_instances(self):
        first_db = FileStudentTable(self.path)
        first_db.create_record(1, "Ivan", "Ivanov", 20, "M")

        second_db = FileStudentTable(self.path)
        records = second_db.select_record()

        self.assertEqual(records, [(1, "Ivan", "Ivanov", 20, "M")])

    def test_update_record_in_file(self):
        db = FileStudentTable(self.path)
        db.create_record(1, "Ivan", "Ivanov", 20, "M")
        db.update_record(1, first_name="Petr", age=21)

        second_db = FileStudentTable(self.path)
        records = second_db.select_record()
        self.assertEqual(records, [(1, "Petr", "Ivanov", 21, "M")])

    def test_delete_record_in_file(self):
        db = FileStudentTable(self.path)
        db.create_record(1, "Ivan", "Ivanov", 20, "M")
        db.delete_record(1)

        second_db = FileStudentTable(self.path)
        self.assertEqual(second_db.select_record(), [])

    def test_invalid_json(self):
        self.path.write_text("{ bad json", encoding="utf-8")
        db = FileStudentTable(self.path)

        with self.assertRaises(InvalidStorageDataError):
            db.select_record()

    def test_json_structure_is_saved(self):
        db = FileStudentTable(self.path)
        db.create_record(1, "Ivan", "Ivanov", 20, "M")

        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(
            data["columns"],
            ["student_id", "first_name", "second_name", "age", "sex"],
        )
