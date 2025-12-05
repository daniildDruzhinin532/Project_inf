# src/database/db.py

import sqlite3
from sqlite3 import Connection

def get_connection(db_name: str = "hostel.db") -> Connection:

    return sqlite3.connect(db_name)


def create_tables(db_name: str = "hostel.db"):
    
    conn = get_connection(db_name)
    cursor = conn.cursor()

    # Таблица для комендантов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Command (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Surname TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Таблица для общежитий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Hostel (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Num_hostel INTEGER NOT NULL,
            count_rooms INTEGER NOT NULL,
            Command_ID INTEGER,
            FOREIGN KEY (Command_ID) REFERENCES Command(ID)
        )
    ''')

    # Таблица для комнат
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Room (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Num_resid INTEGER NOT NULL,
            Num_room INTEGER NOT NULL,
            Hostel_ID INTEGER,
            FOREIGN KEY (Hostel_ID) REFERENCES Hostel(ID)
        )
    ''')

    # Таблица для студентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Surname TEXT NOT NULL,
            student_ticket INTEGER NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Таблица для связи студентов и комнат
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Stud_room (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Student_ID INTEGER,
            Room_ID INTEGER,
            FOREIGN KEY (Student_ID) REFERENCES Student(ID),
            FOREIGN KEY (Room_ID) REFERENCES Room(ID),
            UNIQUE(Student_ID, Room_ID)
        )
    ''')

    # Таблица для типов заявок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Type_request (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            comment TEXT
        )
    ''')

    # Таблица для заявок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Request (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Type_request_ID INTEGER,
            name TEXT NOT NULL,
            date DATE NOT NULL,
            student_id INTEGER,
            text TEXT,
            FOREIGN KEY (Type_request_ID) REFERENCES Type_request(ID),
            FOREIGN KEY (student_id) REFERENCES Student(ID)
        )
    ''')

    conn.commit()
    conn.close()


def insert_sample_data(db_name: str = "hostel.db"):
    conn = get_connection(db_name)
    cursor = conn.cursor()


    cursor.execute("SELECT COUNT(*) FROM Command")
    if cursor.fetchone()[0] == 0:
        commands = [
            ("Иван", "Иванов", "pass123"),
        ]
        cursor.executemany("INSERT INTO Command (Name, Surname, password) VALUES (?, ?, ?)", commands)
        print("Добавлены коменданты.")

    
    cursor.execute("SELECT COUNT(*) FROM Hostel")
    if cursor.fetchone()[0] == 0:
        hostels = [
            (1, 100, 1),
            (2, 150, 2),
        ]
        cursor.executemany("INSERT INTO Hostel (Num_hostel, count_rooms, Command_ID) VALUES (?, ?, ?)", hostels)
        print("Добавлены общежития.")

    
    cursor.execute("SELECT COUNT(*) FROM Room")
    if cursor.fetchone()[0] == 0:
        
        hostel1_rooms = [
            (4, 101, 1),
            (3, 102, 1),
            (4, 103, 1),
            (4, 201, 1),
            (3, 202, 1),
            (4, 203, 1),
        ]
        
        hostel2_rooms = [
            (3, 301, 2),
            (4, 302, 2),
            (3, 303, 2),
            (3, 401, 2),
            (4, 402, 2),
            (3, 403, 2),
        ]
        
        cursor.executemany("INSERT INTO Room (Num_resid, Num_room, Hostel_ID) VALUES (?, ?, ?)",
                        hostel1_rooms + hostel2_rooms)
        print("Добавлены комнаты.")

    # Добавление студентов (включая новых)
    cursor.execute("SELECT COUNT(*) FROM Student")
    if cursor.fetchone()[0] == 0:
        students = [
            # Существующие студенты
            ("Алексей", "Иванов", 123456, "studpass1"),
            ("Дмитрий", "Петров", 222333, "studpass4"),
            ("Илья", "Сидоров", 333444, "studpass5"),
            ("Евгений", "Козлов", 444555, "studpass6"),
            ("Андрей", "Новиков", 555666, "studpass7"),
            ("Павел", "Морозов", 666777, "studpass8"),
            ("Георгий", "Зайцев", 777888, "studpass9"),
            ("Сергей", "Павлов", 888999, "studpass10"),
            ("Владимир", "Семенов", 999000, "studpass11"),
            ("Артем", "Голубев", 100101, "studpass12"),
            ("Максим", "Виноградов", 101102, "studpass13"),
            ("Кирилл", "Белов", 103104, "studpass15"),
            ("Константин", "Медведев", 105106, "studpass17"),
            ("Анна", "Смирнова", 654321, "studpass2"),
            ("Елена", "Кузнецова", 111222, "studpass3"),
            ("Ольга", "Попова", 102103, "studpass14"),
            ("Юлия", "Васильева", 104105, "studpass16"),
            ("Наталья", "Романова", 106107, "studpass18"),
            ("Ирина", "Зайцева", 107108, "studpass19"),
            ("Мария", "Соколова", 108109, "studpass20"),
            
            # Новые студенты, которые хотят заселиться 
            ("Александр", "Орлов", 200001, "pass2001"),
            ("Никита", "Лебедев", 200002, "pass2002"),
            ("Роман", "Егоров", 200003, "pass2003"),
            ("Станислав", "Комаров", 200004, "pass2004"),
            ("Вадим", "Щербаков", 200005, "pass2005"),
            ("Татьяна", "Максимова", 200006, "pass2006"),
            ("Екатерина", "Фомина", 200007, "pass2007"),
            ("Светлана", "Давыдова", 200008, "pass2008"),
            ("Людмила", "Беляева", 200009, "pass2009"),
            ("Галина", "Гаврилова", 200010, "pass2010"),
            
            # Студенты, которые просто в базе 
            ("Виктор", "Титов", 300001, "pass3001"),
            ("Аркадий", "Субботин", 300002, "pass3002"),
            ("Лариса", "Федотова", 300003, "pass3003"),
        ]
        cursor.executemany("INSERT INTO Student (Name, Surname, student_ticket, password) VALUES (?, ?, ?, ?)", students)
        print("Добавлены студенты.")


    cursor.execute("SELECT COUNT(*) FROM Stud_room")
    if cursor.fetchone()[0] == 0:
        
        def settle_students(room_id, student_ids):
            for student_id in student_ids:
                try:
                    cursor.execute("INSERT INTO Stud_room (Student_ID, Room_ID) VALUES (?, ?)", (student_id, room_id))
                except sqlite3.IntegrityError:
                    pass
        
        
        cursor.execute("SELECT ID FROM Student WHERE ID <= 20")
        students_to_settle = [row[0] for row in cursor.fetchall()]
        
        
        for student_id in students_to_settle:
            cursor.execute('''
                SELECT r.ID 
                FROM Room r 
                LEFT JOIN Stud_room sr ON r.ID = sr.Room_ID 
                GROUP BY r.ID 
                HAVING COUNT(sr.Student_ID) < r.Num_resid
                LIMIT 1
            ''')
            
            room_result = cursor.fetchone()
            if room_result:
                room_id = room_result[0]
                settle_students(room_id, [student_id])
        
        print("Расселение завершено.")

    
    cursor.execute("SELECT COUNT(*) FROM Type_request")
    if cursor.fetchone()[0] == 0:
        type_requests = [
            ("Заселение", "Заявка на заселение в комнату"),
            ("Выселение", "Заявка на выселение"),
            ("Переселение", "Заявка на переселение"),
        ]
        cursor.executemany("INSERT INTO Type_request (name, comment) VALUES (?, ?)", type_requests)
        print("Добавлены типы заявок.")


    cursor.execute("SELECT COUNT(*) FROM Request")
    if cursor.fetchone()[0] == 0:
        requests = [

            (1, "Заселение в общежитие", "2025-01-15", 21, "Прошу заселить в общежитие"),
            (1, "Заселение в общежитие", "2025-01-16", 22, "Прошу заселить в общежитие"),
            (1, "Заселение в общежитие", "2025-01-17", 23, "Прошу заселить в общежитие"),
            (1, "Заселение в общежитие", "2025-01-18", 24, "Прошу заселить в общежитие"),
            (1, "Заселение в общежитие", "2025-01-19", 25, "Прошу заселить в общежитие"),
            (1, "Заселение в общежитие", "2025-01-20", 26, "Прошу заселить в общежитие"),
            (1, "Заселение в общежитие", "2025-01-21", 27, "Прошу заселить в общежитие"),
            (1, "Заселение в общежитие", "2025-01-22", 28, "Прошу заселить в общежитие"),
            (1, "Заселение в общежитие", "2025-01-23", 29, "Прошу заселить в общежитие"),
            (1, "Заселение в общежитие", "2025-01-24", 30, "Прошу заселить в общежитие"),
            
            (2, "Выселение из общежития", "2025-01-25", 1, "Хочу выселиться из общежития"),
            (2, "Выселение из общежития", "2025-01-26", 2, "Хочу выселиться из общежития"),
            (2, "Выселение из общежития", "2025-01-27", 3, "Хочу выселиться из общежития"),
            (2, "Выселение из общежития", "2025-01-28", 4, "Хочу выселиться из общежития"),
            (2, "Выселение из общежития", "2025-01-29", 5, "Хочу выселиться из общежития"),
            

            (3, "Переселение в другую комнату", "2025-01-30", 6, "Прошу переселить в другую комнату"),
            (3, "Переселение в другую комнату", "2025-01-31", 7, "Прошу переселить в другую комнату"),
            (3, "Переселение в другую комнату", "2025-02-01", 8, "Прошу переселить в другую комнату"),
            
        ]
        cursor.executemany("INSERT INTO Request (Type_request_ID, name, date, student_id, text) VALUES (?, ?, ?, ?, ?)", requests)
        print("Добавлены заявки.")

    conn.commit()
    conn.close()


def check_settlement(db_name: str = "hostel.db"):
    conn = get_connection(db_name)
    cursor = conn.cursor()
    
    print("\n=== ПРОВЕРКА РАССЕЛЕНИЯ ===")
    
    cursor.execute('''
        SELECT 
            h.Num_hostel as Общежитие,
            r.Num_room as Комната,
            COUNT(sr.Student_ID) as Заселено,
            r.Num_resid as Всего_мест,
            GROUP_CONCAT(s.Name || ' ' || s.Surname) as Студенты
        FROM Room r
        JOIN Hostel h ON r.Hostel_ID = h.ID
        LEFT JOIN Stud_room sr ON r.ID = sr.Room_ID
        LEFT JOIN Student s ON sr.Student_ID = s.ID
        GROUP BY r.ID
        ORDER BY h.Num_hostel, r.Num_room
    ''')
    
    rooms = cursor.fetchall()
    for room in rooms:
        print(f"Общежитие {room[0]}, Комната {room[1]}: {room[2]}/{room[3]} мест")
        if room[4]:
            print(f"  Студенты: {room[4]}")
    
    print("\n=== РАССЕЛЕНИЕ ЗАВЕРШЕНО ===")
    
    conn.close()