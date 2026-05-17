from .database import StudentDatabase


class MemoryStudentTable(StudentDatabase):
    def __init__(self):
        self.student = []

    def _load_records(self):
        return self.student.copy()

    def _save_records(self, records):
        self.student = records.copy()
