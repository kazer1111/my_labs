import csv
from pathlib import Path

from .database import StudentDatabase
from .errors import InvalidStorageDataError, StorageFileError


class CsvStudentTable(StudentDatabase):
    def __init__(self, path="data/students.csv"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load_records(self):
        if not self.path.exists():
            return []

        try:
            with open(self.path, "r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames is None:
                    return []

                if tuple(reader.fieldnames) != self.columns:
                    raise InvalidStorageDataError("Некорректная структура таблицы")

                result = []

                for record in reader:
                    try:
                        result.append(
                            (
                                int(record["student_id"]),
                                str(record["first_name"]),
                                str(record["second_name"]),
                                int(record["age"]),
                                str(record["sex"]),
                            )
                        )
                    except (KeyError, TypeError, ValueError):
                        raise InvalidStorageDataError("Некорректная запись в файле")
        except OSError:
            raise StorageFileError("Ошибка при чтении файла")

        return result

    def _save_records(self, records):
        try:
            with open(self.path, "w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.columns)
                writer.writeheader()

                for record in records:
                    writer.writerow(
                        {
                            "student_id": record[0],
                            "first_name": record[1],
                            "second_name": record[2],
                            "age": record[3],
                            "sex": record[4],
                        }
                    )
        except OSError:
            raise StorageFileError("Ошибка при записи файла")
