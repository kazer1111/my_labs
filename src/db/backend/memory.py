Student = []


def create_record(student_id, first_name, second_name, age, sex):
    if age < 0:
        raise ValueError("Возраст не может быть отрицательным")

    for record in Student:
        if record[0] == student_id:
            raise ValueError("Запись с таким id уже существует")

    new_record = (
        student_id,
        first_name.strip(),
        second_name.strip(),
        age,
        sex.strip(),
    )
    Student.append(new_record)

    return new_record


def select_record(
    student_id=None, first_name=None, second_name=None, age=None, sex=None
):
    result = []

    for record in Student:
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


def update_record(
    student_id, first_name=None, second_name=None, age=None, sex=None, new_id=None
):
    for i in range(len(Student)):
        record = list(Student[i])

        if record[0] == student_id:
            if new_id is not None:
                for j in range(len(Student)):
                    if Student[j][0] == new_id and Student[j][0] != student_id:
                        raise ValueError("Запись с таким id уже существует")
                record[0] = new_id

            if first_name is not None:
                record[1] = first_name.strip()

            if second_name is not None:
                record[2] = second_name.strip()

            if age is not None:
                if age < 0:
                    raise ValueError("Возраст не может быть отрицательным")
                record[3] = age

            if sex is not None:
                record[4] = sex.strip()

            Student[i] = tuple(record)
            return Student[i]

    raise ValueError("Запись не найдена")


def delete_record(student_id):
    for i in range(len(Student)):
        if Student[i][0] == student_id:
            deleted_record = Student[i]
            del Student[i]

            return deleted_record

    raise ValueError("Запись не найдена")
