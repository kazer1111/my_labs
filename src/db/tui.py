from .backend.memory import create_record, delete_record, select_record, update_record


def _print_menu():
    print("\n=== База студентов ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("4. Обновить запись")
    print("5. Удалить запись")
    print("0. Выход")


def _read_int(prompt):
    while True:
        raw = input(prompt).strip()

        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число")


def _read_optional_int(prompt):
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым")


def _print_records(records):
    if records == []:
        print("Записи не найдены")
        return

    for record in records:
        print(record)


def _add_student():
    print("\nДобавление записи")
    student_id = _read_int("id: ")
    first_name = input("first_name: ").strip()
    second_name = input("second_name: ").strip()
    age = _read_int("age: ")
    sex = input("sex: ").strip()

    try:
        record = create_record(student_id, first_name, second_name, age, sex)
        print("Запись добавлена:", record)
    except ValueError as e:
        print("Ошибка:", e)


def _show_all_students():
    print("\nСписок записей")
    records = select_record()
    _print_records(records)


def _find_students_by_filter():
    print("\nПоиск по фильтру")
    print("Если поле не нужно, просто нажмите Enter")

    student_id = _read_optional_int("id: ")
    first_name = input("first_name: ").strip()
    second_name = input("second_name: ").strip()
    age = _read_optional_int("age: ")
    sex = input("sex: ").strip()

    if first_name == "":
        first_name = None
    if second_name == "":
        second_name = None
    if sex == "":
        sex = None

    records = select_record(student_id, first_name, second_name, age, sex)
    _print_records(records)


def _update_student():
    print("\nОбновление записи")
    student_id = _read_int("id записи, которую нужно обновить: ")
    print("Если поле не нужно менять, просто нажмите Enter")

    new_id = _read_optional_int("new_id: ")
    first_name = input("first_name: ").strip()
    second_name = input("second_name: ").strip()
    age = _read_optional_int("age: ")
    sex = input("sex: ").strip()

    if first_name == "":
        first_name = None
    if second_name == "":
        second_name = None
    if sex == "":
        sex = None

    try:
        record = update_record(student_id, first_name, second_name, age, sex, new_id)
        print("Запись обновлена:", record)
    except ValueError as e:
        print("Ошибка:", e)


def _delete_student():
    print("\nУдаление записи")
    student_id = _read_int("id записи, которую нужно удалить: ")

    try:
        record = delete_record(student_id)
        print("Запись удалена:", record)
    except ValueError as e:
        print("Ошибка:", e)


def run():
    while True:
        _print_menu()
        action = input("Выберите действие: ").strip()

        if action == "1":
            _add_student()
        elif action == "2":
            _show_all_students()
        elif action == "3":
            _find_students_by_filter()
        elif action == "4":
            _update_student()
        elif action == "5":
            _delete_student()
        elif action == "0":
            print("Выход из программы")
            break
        else:
            print("Неизвестная команда")
