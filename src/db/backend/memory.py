from .errors import DuplicateIDError, InvalidAgeError, RecordNotFoundError


class StudentTable:
    def __init__(self):
        self.student = []

    def create_record(self, student_id, first_name, second_name, age, sex):
        if age < 0:
            raise InvalidAgeError("Возраст не может быть отрицательным")

        for record in self.student:
            if record[0] == student_id:
                raise DuplicateIDError("Запись с таким id уже существует")

        new_record = (
            student_id,
            first_name.strip(),
            second_name.strip(),
            age,
            sex.strip(),
        )
        self.student.append(new_record)
        return new_record

    def select_record(self, student_id=None, first_name=None, second_name=None, age=None, sex=None):
        result = []

        for record in self.student:
            if student_id is not None and record[0] != student_id:
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

    def update_record(self, student_id, first_name=None, second_name=None, age=None, sex=None, new_id=None):
        for i in range(len(self.student)):
            record = list(self.student[i])

            if record[0] == student_id:
                if new_id is not None:
                    for j in range(len(self.student)):
                        if self.student[j][0] == new_id and self.student[j][0] != student_id:
                            raise DuplicateIDError("Запись с таким id уже существует")
                    record[0] = new_id

                if first_name is not None:
                    record[1] = first_name.strip()

                if second_name is not None:
                    record[2] = second_name.strip()

                if age is not None:
                    if age < 0:
                        raise InvalidAgeError("Возраст не может быть отрицательным")
                    record[3] = age

                if sex is not None:
                    record[4] = sex.strip()

                self.student[i] = tuple(record)
                return self.student[i]

        raise RecordNotFoundError("Запись не найдена")

    def delete_record(self, student_id):
        for i in range(len(self.student)):
            if self.student[i][0] == student_id:
                deleted_record = self.student[i]
                del self.student[i]
                return deleted_record

        raise RecordNotFoundError("Запись не найдена")
