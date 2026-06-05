import io
import unittest
from unittest.mock import patch

from src.db.backend.csv_file import CsvStudentTable
from src.db.backend.file import FileStudentTable
from src.db.backend.memory import MemoryStudentTable
from src.db.tui import StudentTUI


class TestTUI(unittest.TestCase):
    @patch("builtins.input", side_effect=["1"])
    def test_memory_choice(self, fake_input):
        tui = StudentTUI()
        self.assertIsInstance(tui.table, MemoryStudentTable)

    @patch("builtins.input", side_effect=["2"])
    def test_json_choice(self, fake_input):
        tui = StudentTUI()
        self.assertIsInstance(tui.table, FileStudentTable)

    @patch("builtins.input", side_effect=["3"])
    def test_csv_choice(self, fake_input):
        tui = StudentTUI()
        self.assertIsInstance(tui.table, CsvStudentTable)

    @patch("builtins.input", side_effect=["1", "0"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_run_exit(self, fake_out, fake_input):
        tui = StudentTUI()
        tui.run()
        self.assertIn("Выход из программы", fake_out.getvalue())
