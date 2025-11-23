import sqlite3
from src.database.db import get_connection
from src.models.models import Command, Hostel, Room, StudRoom, Student, TypeRequest, Request

class Repository:
    def __init__(self, db_name: str):
        self.conn = get_connection(db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    
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

    
    def authenticate_command(self, surname: str, password: str):
        self.cursor.execute("SELECT * FROM Command WHERE Surname = ? AND password = ?", (surname, password))
        row = self.cursor.fetchone()
        return Command(*row) if row else None

    
    def get_all_students(self):
        self.cursor.execute("SELECT * FROM Student")
        rows = self.cursor.fetchall()
        
        students = []
        for row in rows:
            students.append(Student(row[0], row[1], row[2], row[3], row[4]))
        return students

    def get_student(self, student_id: int):
        self.cursor.execute("SELECT * FROM Student WHERE ID = ?", (student_id,))
        row = self.cursor.fetchone()
        if row:
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

    
    def authenticate_student(self, surname: str, password: str):
        self.cursor.execute("SELECT * FROM Student WHERE Surname = ? AND password = ?", (surname, password))
        row = self.cursor.fetchone()
        if row:
            return Student(row[0], row[1], row[2], row[3], row[4])
        return None

    
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
            room_id = row[0]
            num_resid = row[1]
            num_room = row[2]
            hostel_id = row[3]
            rooms.append(Room(room_id, num_resid, num_room, hostel_id))
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
            return Room(row[0], row[1], row[2], row[3])
        return None
    
    def get_type_request(self, type_request_id: int):
        """Получает тип заявки по ID"""
        self.cursor.execute("SELECT * FROM Type_request WHERE ID = ?", (type_request_id,))
        row = self.cursor.fetchone()
        return TypeRequest(*row) if row else None

    def get_pending_requests(self):
        """Получает все необработанные заявки"""
        self.cursor.execute("SELECT * FROM Request")
        return [Request(*row) for row in self.cursor.fetchall()]

    def settle_student(self, student_id: int, room_id: int):
        """Заселяет студента в комнату"""

        self.cursor.execute("SELECT * FROM Stud_room WHERE Student_ID = ?", (student_id,))
        if self.cursor.fetchone():
            raise Exception("Студент уже заселен в комнату")
        
        
        self.cursor.execute("""
            SELECT r.Num_resid, COUNT(sr.ID) as current 
            FROM Room r 
            LEFT JOIN Stud_room sr ON r.ID = sr.Room_ID 
            WHERE r.ID = ? 
            GROUP BY r.ID
        """, (room_id,))
        result = self.cursor.fetchone()
        if result and result[1] >= result[0]:
            raise Exception("В комнате нет свободных мест")
        
        self.cursor.execute("INSERT INTO Stud_room (Student_ID, Room_ID) VALUES (?, ?)", (student_id, room_id))
        self.conn.commit()

    def evict_student(self, student_id: int):
        """Выселяет студента из комнаты"""
        self.cursor.execute("DELETE FROM Stud_room WHERE Student_ID = ?", (student_id,))
        self.conn.commit()

    def transfer_student(self, student_id: int, new_room_id: int):
        """Переселяет студента в другую комнату"""
        
        self.evict_student(student_id)
        
        self.settle_student(student_id, new_room_id)

    def mark_request_processed(self, request_id: int):
        """Помечает заявку как обработанную (удаляет её)"""
        self.cursor.execute("DELETE FROM Request WHERE ID = ?", (request_id,))
        self.conn.commit()

    
    
    def get_hostel_by_command_id(self, command_id: int):
        """Получает общежитие по ID коменданта"""
        self.cursor.execute("SELECT * FROM Hostel WHERE Command_ID = ?", (command_id,))
        row = self.cursor.fetchone()
        return Hostel(*row) if row else None

    def get_students_in_command_hostel(self, command_id: int):
        """Получает студентов в общежитии коменданта"""
        self.cursor.execute("""
            SELECT s.* FROM Student s
            JOIN Stud_room sr ON s.ID = sr.Student_ID
            JOIN Room r ON sr.Room_ID = r.ID
            JOIN Hostel h ON r.Hostel_ID = h.ID
            WHERE h.Command_ID = ?
        """, (command_id,))
        rows = self.cursor.fetchall()
        students = []
        for row in rows:
            students.append(Student(row[0], row[1], row[2], row[3], row[4]))
        return students

    def evict_student_from_command_hostel(self, command_id: int, student_id: int):
        """Выселяет студента из общежития коменданта"""
        self.cursor.execute("""
            SELECT sr.ID FROM Stud_room sr
            JOIN Room r ON sr.Room_ID = r.ID
            JOIN Hostel h ON r.Hostel_ID = h.ID
            WHERE h.Command_ID = ? AND sr.Student_ID = ?
        """, (command_id, student_id))
        
        if not self.cursor.fetchone():
            raise Exception("Студент не находится в вашем общежитии")
        
        self.cursor.execute("DELETE FROM Stud_room WHERE Student_ID = ?", (student_id,))
        self.conn.commit()

    def get_rooms_in_command_hostel(self, command_id: int):
        """Получает комнаты в общежитии коменданта"""
        self.cursor.execute("""
            SELECT r.* FROM Room r
            JOIN Hostel h ON r.Hostel_ID = h.ID
            WHERE h.Command_ID = ?
        """, (command_id,))
        rows = self.cursor.fetchall()
        rooms = []
        for row in rows:
            rooms.append(Room(row[0], row[1], row[2], row[3]))
        return rooms