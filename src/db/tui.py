from .backend.errors import DuplicateIDError, InvalidAgeError, RecordNotFoundError
from .backend.memory import StudentTable


class StudentTUI:
    def __init__(self):
        self.table = StudentTable()

    def _print_menu(self):
        print("\n=== База студентов ===")
        print("1. Добавить запись")
        print("2. Показать все записи")
        print("3. Найти записи по фильтру")
        print("4. Обновить запись")
        print("5. Удалить запись")
        print("0. Выход")

    def _read_int(self, prompt):
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число")

    def _read_optional_int(self, prompt):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число или оставьте поле пустым")

    def _print_records(self, records):
        if records == []:
            print("Записи не найдены")
            return

        for record in records:
            print(record)

    def _add_student(self):
        print("\nДобавление записи")
        student_id = self._read_int("id: ")
        first_name = input("first_name: ").strip()
        second_name = input("second_name: ").strip()
        age = self._read_int("age: ")
        sex = input("sex: ").strip()

        try:
            record = self.table.create_record(student_id, first_name, second_name, age, sex)
            print("Запись добавлена:", record)
        except (InvalidAgeError, DuplicateIDError) as e:
            print("Ошибка:", e)

    def _show_all_students(self):
        print("\nСписок записей")
        records = self.table.select_record()
        self._print_records(records)

    def _find_students_by_filter(self):
        print("\nПоиск по фильтру")
        print("Если поле не нужно, просто нажмите Enter")

        student_id = self._read_optional_int("id: ")
        first_name = input("first_name: ").strip()
        second_name = input("second_name: ").strip()
        age = self._read_optional_int("age: ")
        sex = input("sex: ").strip()

        if first_name == "":
            first_name = None
        if second_name == "":
            second_name = None
        if sex == "":
            sex = None

        records = self.table.select_record(student_id, first_name, second_name, age, sex)
        self._print_records(records)

    def _update_student(self):
        print("\nОбновление записи")
        student_id = self._read_int("id записи, которую нужно обновить: ")
        print("Если поле не нужно менять, просто нажмите Enter")

        new_id = self._read_optional_int("new_id: ")
        first_name = input("first_name: ").strip()
        second_name = input("second_name: ").strip()
        age = self._read_optional_int("age: ")
        sex = input("sex: ").strip()

        if first_name == "":
            first_name = None
        if second_name == "":
            second_name = None
        if sex == "":
            sex = None

        try:
            record = self.table.update_record(
                student_id, first_name, second_name, age, sex, new_id
            )
            print("Запись обновлена:", record)
        except (InvalidAgeError, DuplicateIDError, RecordNotFoundError) as e:
            print("Ошибка:", e)

    def _delete_student(self):
        print("\nУдаление записи")
        student_id = self._read_int("id записи, которую нужно удалить: ")

        try:
            record = self.table.delete_record(student_id)
            print("Запись удалена:", record)
        except RecordNotFoundError as e:
            print("Ошибка:", e)

    def run(self):
        while True:
            self._print_menu()
            action = input("Выберите действие: ").strip()

            if action == "1":
                self._add_student()
            elif action == "2":
                self._show_all_students()
            elif action == "3":
                self._find_students_by_filter()
            elif action == "4":
                self._update_student()
            elif action == "5":
                self._delete_student()
            elif action == "0":
                print("Выход из программы")
                break
            else:
                print("Неизвестная команда")


def run():
    app = StudentTUI()
    app.run()
