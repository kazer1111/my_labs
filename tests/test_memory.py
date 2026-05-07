import io
import unittest
from unittest.mock import patch

from src.db.backend.errors import DuplicateIDError, InvalidAgeError, RecordNotFoundError
from src.db.backend.memory import StudentTable
from src.db.tui import StudentTUI


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.student_table = StudentTable()

    def test_student_table_allocation(self):
        self.assertIsInstance(self.student_table, StudentTable)

    def test_create_record(self):
        cases = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Alice", "Johnson", 19, "F"),
        ]

        for test_data in cases:
            with self.subTest(test_data=test_data):
                record = self.student_table.create_record(*test_data)
                self.assertEqual(record, test_data)

    def test_create_record_strips_spaces(self):
        record = self.student_table.create_record(1, " John ", " Doe ", 20, " M ")
        self.assertEqual(record, (1, "John", "Doe", 20, "M"))

    def test_create_record_negative_age(self):
        with self.assertRaises(InvalidAgeError):
            self.student_table.create_record(1, "John", "Doe", -1, "M")

    def test_create_record_duplicate_id(self):
        self.student_table.create_record(1, "John", "Doe", 20, "M")

        with self.assertRaises(DuplicateIDError):
            self.student_table.create_record(1, "Jane", "Smith", 22, "F")

    def test_select_record(self):
        test_datas = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Alice", "Johnson", 19, "F"),
            (4, "Bob", "Brown", 20, "M"),
        ]

        for test_data in test_datas:
            self.student_table.create_record(*test_data)

        self.assertEqual(self.student_table.select_record(), test_datas)
        self.assertEqual(self.student_table.select_record(student_id=1), [test_datas[0]])
        self.assertEqual(self.student_table.select_record(first_name="Jane"), [test_datas[1]])
        self.assertEqual(self.student_table.select_record(second_name="Johnson"), [test_datas[2]])
        self.assertEqual(self.student_table.select_record(age=20), [test_datas[0], test_datas[3]])
        self.assertEqual(self.student_table.select_record(sex="F"), [test_datas[1], test_datas[2]])

    def test_update_record(self):
        self.student_table.create_record(1, "John", "Doe", 20, "M")
        record = self.student_table.update_record(1, "Petr", "Ivanov", 21, "M", 2)
        self.assertEqual(record, (2, "Petr", "Ivanov", 21, "M"))

    def test_update_record_negative_age(self):
        self.student_table.create_record(1, "John", "Doe", 20, "M")

        with self.assertRaises(InvalidAgeError):
            self.student_table.update_record(1, age=-5)

    def test_update_record_duplicate_id(self):
        self.student_table.create_record(1, "John", "Doe", 20, "M")
        self.student_table.create_record(2, "Jane", "Smith", 22, "F")

        with self.assertRaises(DuplicateIDError):
            self.student_table.update_record(1, new_id=2)

    def test_update_record_not_found(self):
        with self.assertRaises(RecordNotFoundError):
            self.student_table.update_record(100, first_name="Test")

    def test_delete_record(self):
        self.student_table.create_record(1, "John", "Doe", 20, "M")
        record = self.student_table.delete_record(1)
        self.assertEqual(record, (1, "John", "Doe", 20, "M"))
        self.assertEqual(self.student_table.select_record(), [])

    def test_delete_record_not_found(self):
        with self.assertRaises(RecordNotFoundError):
            self.student_table.delete_record(10)


class TestTUI(unittest.TestCase):
    def setUp(self):
        self.tui = StudentTUI()

    def test_tui_allocation(self):
        self.assertIsInstance(self.tui, StudentTUI)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_print_records_empty(self, fake_out):
        self.tui._print_records([])
        self.assertIn("Записи не найдены", fake_out.getvalue())

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_print_records_data(self, fake_out):
        self.tui._print_records([(1, "John", "Doe", 20, "M")])
        self.assertIn("John", fake_out.getvalue())

    @patch("builtins.input", side_effect=["abc", "5"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_int(self, fake_out, fake_input):
        value = self.tui._read_int("id: ")
        self.assertEqual(value, 5)
        self.assertIn("Ошибка", fake_out.getvalue())

    @patch("builtins.input", side_effect=["abc", "", ""])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_optional_int(self, fake_out, fake_input):
        value = self.tui._read_optional_int("id: ")
        self.assertEqual(value, None)
        self.assertIn("Ошибка", fake_out.getvalue())

    @patch("builtins.input", side_effect=["0"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_run_exit(self, fake_out, fake_input):
        self.tui.run()
        self.assertIn("Выход из программы", fake_out.getvalue())

    @patch("builtins.input", side_effect=["1", "John", "Doe", "20", "M"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_add_student(self, fake_out, fake_input):
        self.tui._add_student()
        self.assertEqual(self.tui.table.select_record(), [(1, "John", "Doe", 20, "M")])
        self.assertIn("Запись добавлена", fake_out.getvalue())

    @patch("builtins.input", side_effect=["1", "John", "Doe", "-5", "M"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_add_student_invalid_age(self, fake_out, fake_input):
        self.tui._add_student()
        self.assertIn("Ошибка", fake_out.getvalue())

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show_all_students(self, fake_out):
        self.tui.table.create_record(1, "John", "Doe", 20, "M")
        self.tui._show_all_students()
        self.assertIn("John", fake_out.getvalue())

    @patch("builtins.input", side_effect=["1", "", "", "", ""])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_find_students_by_filter(self, fake_out, fake_input):
        self.tui.table.create_record(1, "John", "Doe", 20, "M")
        self.tui._find_students_by_filter()
        self.assertIn("John", fake_out.getvalue())

    @patch("builtins.input", side_effect=["1", "2", "Petr", "Ivanov", "21", "M"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_update_student(self, fake_out, fake_input):
        self.tui.table.create_record(1, "John", "Doe", 20, "M")
        self.tui._update_student()
        self.assertEqual(self.tui.table.select_record(), [(2, "Petr", "Ivanov", 21, "M")])
        self.assertIn("Запись обновлена", fake_out.getvalue())

    @patch("builtins.input", side_effect=["1"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_student(self, fake_out, fake_input):
        self.tui.table.create_record(1, "John", "Doe", 20, "M")
        self.tui._delete_student()
        self.assertEqual(self.tui.table.select_record(), [])
        self.assertIn("Запись удалена", fake_out.getvalue())
