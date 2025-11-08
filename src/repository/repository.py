import sqlite3
from src.database.db import get_connection
from src.models.models import Command, Hostel, Room, StudRoom, Student, TypeRequest, Request

class Repository:
    def __init__(self, db_name: str):
        self.conn = get_connection(db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    # CRUD для Command (комендант)
    def get_all_commands(self):
        self.cursor.execute("SELECT * FROM Command")
        return [Command(*row) for row in self.cursor.fetchall()]

    def get_command(self, command_id: int):
        self.cursor.execute("SELECT * FROM Command WHERE ID = ?", (command_id,))
        row = self.cursor.fetchone()
        return Command(*row) if row else None

    def add_command(self, name: str, surname: str, password: str):
        self.cursor.execute("INSERT INTO Command (Name, Surname, password) VALUES (?, ?, ?)", (name, surname, password))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_command(self, command_id: int, name: str, surname: str, password: str):
        self.cursor.execute("UPDATE Command SET Name = ?, Surname = ?, password = ? WHERE ID = ?", (name, surname, password, command_id))
        self.conn.commit()

    def delete_command(self, command_id: int):
        self.cursor.execute("DELETE FROM Command WHERE ID = ?", (command_id,))
        self.conn.commit()

    # Авторизация для коменданта
    def authenticate_command(self, surname: str, password: str):
        self.cursor.execute("SELECT * FROM Command WHERE Surname = ? AND password = ?", (surname, password))
        row = self.cursor.fetchone()
        return Command(*row) if row else None

    # CRUD для Student (студент)
    def get_all_students(self):
        self.cursor.execute("SELECT * FROM Student")
        rows = self.cursor.fetchall()
        # Обрабатываем случай, когда в таблице есть дополнительные поля
        students = []
        for row in rows:
            if len(row) == 6:  # С учетом поля gender
                students.append(Student(row[0], row[1], row[2], row[3], row[4], row[5]))
            else:  # Без поля gender
                students.append(Student(row[0], row[1], row[2], row[3], row[4]))
        return students

    def get_student(self, student_id: int):
        self.cursor.execute("SELECT * FROM Student WHERE ID = ?", (student_id,))
        row = self.cursor.fetchone()
        if row:
            if len(row) == 6:  # С учетом поля gender
                return Student(row[0], row[1], row[2], row[3], row[4], row[5])
            else:  # Без поля gender
                return Student(row[0], row[1], row[2], row[3], row[4])
        return None

    def add_student(self, name: str, surname: str, student_ticket: int, password: str):
        self.cursor.execute("INSERT INTO Student (Name, Surname, student_ticket, password) VALUES (?, ?, ?, ?)", (name, surname, student_ticket, password))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_student(self, student_id: int, name: str, surname: str, student_ticket: int, password: str):
        self.cursor.execute("UPDATE Student SET Name = ?, Surname = ?, student_ticket = ?, password = ? WHERE ID = ?", (name, surname, student_ticket, password, student_id))
        self.conn.commit()

    def delete_student(self, student_id: int):
        self.cursor.execute("DELETE FROM Student WHERE ID = ?", (student_id,))
        self.conn.commit()

    # Авторизация для студента
    def authenticate_student(self, surname: str, password: str):
        self.cursor.execute("SELECT * FROM Student WHERE Surname = ? AND password = ?", (surname, password))
        row = self.cursor.fetchone()
        if row:
            if len(row) == 6:  # С учетом поля gender
                return Student(row[0], row[1], row[2], row[3], row[4], row[5])
            else:  # Без поля gender
                return Student(row[0], row[1], row[2], row[3], row[4])
        return None

    # CRUD для Request (заявки)
    def get_all_requests(self):
        self.cursor.execute("SELECT * FROM Request")
        return [Request(*row) for row in self.cursor.fetchall()]

    def get_request(self, request_id: int):
        self.cursor.execute("SELECT * FROM Request WHERE ID = ?", (request_id,))
        row = self.cursor.fetchone()
        return Request(*row) if row else None

    def add_request(self, type_request_id: int, name: str, date: str, student_id: int, text: str):
        self.cursor.execute("INSERT INTO Request (Type_request_ID, name, date, student_id, text) VALUES (?, ?, ?, ?, ?)", (type_request_id, name, date, student_id, text))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_request(self, request_id: int, type_request_id: int, name: str, date: str, student_id: int, text: str):
        self.cursor.execute("UPDATE Request SET Type_request_ID = ?, name = ?, date = ?, student_id = ?, text = ? WHERE ID = ?", (type_request_id, name, date, student_id, text, request_id))
        self.conn.commit()

    def delete_request(self, request_id: int):
        self.cursor.execute("DELETE FROM Request WHERE ID = ?", (request_id,))
        self.conn.commit()

    # Методы для связанных данных (слой доступа к данным)
    def get_requests_by_student(self, student_id: int):
        """
        Получает все заявки конкретного студента.
        """
        self.cursor.execute("SELECT * FROM Request WHERE student_id = ?", (student_id,))
        return [Request(*row) for row in self.cursor.fetchall()]

    def get_students_in_room(self, room_id: int):
        """
        Получает список студентов в конкретной комнате.
        """
        self.cursor.execute("""
            SELECT s.* FROM Student s
            JOIN Stud_room sr ON s.ID = sr.Student_ID
            WHERE sr.Room_ID = ?
        """, (room_id,))
        rows = self.cursor.fetchall()
        students = []
        for row in rows:
            if len(row) == 6:  # С учетом поля gender
                students.append(Student(row[0], row[1], row[2], row[3], row[4], row[5]))
            else:  # Без поля gender
                students.append(Student(row[0], row[1], row[2], row[3], row[4]))
        return students

    def get_rooms_in_hostel(self, hostel_id: int):
        """
        Получает список комнат в конкретном общежитии.
        """
        self.cursor.execute("SELECT * FROM Room WHERE Hostel_ID = ?", (hostel_id,))
        rows = self.cursor.fetchall()
        rooms = []
        for row in rows:
            if len(row) == 6:  # С учетом полей gender и special_group
                rooms.append(Room(row[0], row[1], row[2], row[3], row[4], row[5]))
            else:  # Без дополнительных полей
                rooms.append(Room(row[0], row[1], row[2], row[3]))
        return rooms

    def get_free_rooms(self):
        """
        Получает список свободных комнат (где количество студентов меньше Num_resid).
        Подсчет студентов в комнате через JOIN.
        """
        self.cursor.execute("""
            SELECT r.*, COUNT(sr.ID) as current_resid
            FROM Room r
            LEFT JOIN Stud_room sr ON r.ID = sr.Room_ID
            GROUP BY r.ID
            HAVING current_resid < r.Num_resid
        """)
        rows = self.cursor.fetchall()
        rooms = []
        for row in rows:
            # Берем только первые 4 поля для Room (игнорируем current_resid и дополнительные поля)
            rooms.append(Room(row[0], row[1], row[2], row[3]))
        return rooms

    def get_student_room(self, student_id: int):
        """
        Получает комнату студента (если заселен).
        """
        self.cursor.execute("""
            SELECT r.* FROM Room r
            JOIN Stud_room sr ON r.ID = sr.Room_ID
            WHERE sr.Student_ID = ?
        """, (student_id,))
        row = self.cursor.fetchone()
        if row:
            if len(row) == 6:  # С учетом полей gender и special_group
                return Room(row[0], row[1], row[2], row[3], row[4], row[5])
            else:  # Без дополнительных полей
                return Room(row[0], row[1], row[2], row[3])
        return None