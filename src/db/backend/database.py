from abc import ABC, abstractmethod

from .errors import DuplicateIDError, InvalidAgeError, RecordNotFoundError


class StudentDatabase(ABC):
    columns = ("student_id", "first_name", "second_name", "age", "sex")

    @abstractmethod
    def _load_records(self):
        pass

    @abstractmethod
    def _save_records(self, records):
        pass

    def create_record(self, student_id,first_name,second_name,age,sex):
        records = self._load_records()

        if age < 0:
            raise InvalidAgeError("Возраст не может быть отрицательным")

        for record in records :
            if record[0] == student_id:
                raise DuplicateIDError("Запись с таким id уже существует")

        new_record = (
            student_id,
            first_name.strip(),
            second_name.strip(),
            age,
            sex.strip(),
        )
        records.append(new_record)
        self._save_records(records)

        return new_record

    def select_record(self, student_id=None,first_name=None,second_name=None,age=None,sex=None):
        records = self._load_records()
        result = []

        for record in records:
            if student_id is not None and record[0]!=student_id:
                continue

            if first_name is not None and record[1] != first_name:
                continue

            if second_name is not None and record[2] != second_name:
                continue

            if age is not None and record[3] != age:
                continue

            if sex is not None and record[4] != sex:
                continue

            result.append(record)

        return result

    def update_record(self, student_id, first_name=None,second_name=None, age=None, sex=None,new_id=None):
        records = self._load_records()

        for i in range(len(records)):
            record = list(records[i])

            if record[0] == student_id:
                if new_id is not None:
                    for j in range(len(records)):
                        if records[j][0] == new_id and records[j][0] != student_id:
                            raise DuplicateIDError("Запись с таким id уже существует")
                    record[0] = new_id

                if first_name is not None :
                    record[1] = first_name.strip()

                if second_name is not None:
                    record[2] = second_name.strip()

                if age is not None:
                    if age < 0:
                        raise InvalidAgeError("Возраст не может быть отрицательным")
                    record[3] = age

                if sex is not None:
                    record[4] = sex.strip()

                records[i] = tuple(record)
                self._save_records(records)
                return records[i]

        raise RecordNotFoundError("Запись не найдена")

    def delete_record(self, student_id):
        records = self._load_records()

        for i in range(len(records)):
            if records[i][0] == student_id:
                deleted_record = records[i]
                del records[i]
                self._save_records(records)

                return deleted_record

        raise RecordNotFoundError("Запись не найдена")
