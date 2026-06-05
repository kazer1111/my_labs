import json
from pathlib import Path

from .database import StudentDatabase
from .errors import InvalidStorageDataError, StorageFileError


class FileStudentTable(StudentDatabase):
    def __init__(self, path="data/students.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load_records(self):
        if not self.path.exists():
            return []

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            raise InvalidStorageDataError("Файл JSON поврежден")
        except OSError:
            raise StorageFileError("Ошибка при чтении файла")

        if type(data) != dict:
            raise InvalidStorageDataError("Некорректная структура файла")

        if "columns" not in data or "records" not in data:
            raise InvalidStorageDataError("Некорректная структура файла")

        if tuple(data["columns"]) != self.columns:
            raise InvalidStorageDataError("Некорректная структура таблицы")

        result = []

        for record in data["records"]:
            if type(record) != dict:
                raise InvalidStorageDataError("Некорректная запись в файле")

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

        return result

    def _save_records(self, records):
        data = {
            "columns": list(self.columns),
            "records": [],
        }

        for record in records:
            data["records"].append(
                {
                    "student_id": record[0],
                    "first_name": record[1],
                    "second_name": record[2],
                    "age": record[3],
                    "sex": record[4],
                }
            )

        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError:
            raise StorageFileError("Ошибка при записи файла")
