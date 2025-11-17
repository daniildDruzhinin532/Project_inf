# src/database/db.py

import sqlite3
from sqlite3 import Connection

def get_connection(db_name: str = "hostel.db") -> Connection:
    """
    Создает соединение с базой данных SQLite.
    Если файл базы данных не существует, он будет создан.
    """
    return sqlite3.connect(db_name)


def create_tables(db_name: str = "hostel.db"):
    """
    Создает таблицы с учетом разделения по полу на уровне комнат.
    """
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

    # Таблица для общежитий (теперь без разделения по полу)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Hostel (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Num_hostel INTEGER NOT NULL,
            count_rooms INTEGER NOT NULL,
            Command_ID INTEGER,
            FOREIGN KEY (Command_ID) REFERENCES Command(ID)
        )
    ''')

    # Таблица для комнат (добавляем поле пола для комнаты)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Room (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Num_resid INTEGER NOT NULL,  -- Количество мест в комнате
            Num_room INTEGER NOT NULL,   -- Номер комнаты
            Hostel_ID INTEGER,
            gender TEXT NOT NULL CHECK(gender IN ('male', 'female')),  -- Пол для комнаты
            FOREIGN KEY (Hostel_ID) REFERENCES Hostel(ID)
        )
    ''')

    # Таблица для студентов (добавляем поле пола)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Surname TEXT NOT NULL,
            student_ticket INTEGER NOT NULL,
            password TEXT NOT NULL,
            gender TEXT NOT NULL CHECK(gender IN ('male', 'female'))  -- Пол студента
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
    """
    Вставляет тестовые записи в таблицы.
    """
    conn = get_connection(db_name)
    cursor = conn.cursor()

    # Проверка и добавление комендантов
    cursor.execute("SELECT COUNT(*) FROM Command")
    if cursor.fetchone()[0] == 0:
        commands = [
            ("Иван", "Иванов", "pass123"),
            ("Мария", "Петрова", "pass456"),
        ]
        cursor.executemany("INSERT INTO Command (Name, Surname, password) VALUES (?, ?, ?)", commands)
        print("Добавлены коменданты.")

    # Добавление общежитий с привязкой к комендантам
    cursor.execute("SELECT COUNT(*) FROM Hostel")
    if cursor.fetchone()[0] == 0:
        hostels = [
            (1, 100, 1),  # Общежитие 1 закреплено за комендантом 1
            (2, 150, 2),  # Общежитие 2 закреплено за комендантом 2
        ]
        cursor.executemany("INSERT INTO Hostel (Num_hostel, count_rooms, Command_ID) VALUES (?, ?, ?)", hostels)
        print("Добавлены общежития.")

    # Добавление комнат (без специальных групп)
    cursor.execute("SELECT COUNT(*) FROM Room")
    if cursor.fetchone()[0] == 0:
        
        hostel1_rooms = [
            # Мужские комнаты в общежитии 1
            (4, 101, 1, 'male'),
            (3, 102, 1, 'male'),
            (4, 103, 1, 'male'),
            # Женские комнаты в общежитии 1
            (4, 201, 1, 'female'),
            (3, 202, 1, 'female'),
            (4, 203, 1, 'female'),
        ]
        
        hostel2_rooms = [
            # Мужские комнаты в общежитии 2
            (3, 301, 2, 'male'),
            (4, 302, 2, 'male'),
            (3, 303, 2, 'male'),
            # Женские комнаты в общежитии 2
            (3, 401, 2, 'female'),
            (4, 402, 2, 'female'),
            (3, 403, 2, 'female'),
        ]
        
        cursor.executemany("INSERT INTO Room (Num_resid, Num_room, Hostel_ID, gender) VALUES (?, ?, ?, ?)",
                        hostel1_rooms + hostel2_rooms)
        print("Добавлены комнаты.")

    # Добавление студентов (включая новых)
    cursor.execute("SELECT COUNT(*) FROM Student")
    if cursor.fetchone()[0] == 0:
        students = [
            # Существующие студенты (мужчины)
            ("Алексей", "Иванов", 123456, "studpass1", "male"),
            ("Дмитрий", "Петров", 222333, "studpass4", "male"),
            ("Илья", "Сидоров", 333444, "studpass5", "male"),
            ("Евгений", "Козлов", 444555, "studpass6", "male"),
            ("Андрей", "Новиков", 555666, "studpass7", "male"),
            ("Павел", "Морозов", 666777, "studpass8", "male"),
            ("Георгий", "Зайцев", 777888, "studpass9", "male"),
            ("Сергей", "Павлов", 888999, "studpass10", "male"),
            ("Владимир", "Семенов", 999000, "studpass11", "male"),
            ("Артем", "Голубев", 100101, "studpass12", "male"),
            ("Максим", "Виноградов", 101102, "studpass13", "male"),
            ("Кирилл", "Белов", 103104, "studpass15", "male"),
            ("Константин", "Медведев", 105106, "studpass17", "male"),
            
            # Существующие студенты (женщины)
            ("Анна", "Смирнова", 654321, "studpass2", "female"),
            ("Елена", "Кузнецова", 111222, "studpass3", "female"),
            ("Ольга", "Попова", 102103, "studpass14", "female"),
            ("Юлия", "Васильева", 104105, "studpass16", "female"),
            ("Наталья", "Романова", 106107, "studpass18", "female"),
            ("Ирина", "Зайцева", 107108, "studpass19", "female"),
            ("Мария", "Соколова", 108109, "studpass20", "female"),
            
            # Новые студенты, которые хотят заселиться (10 человек)
            ("Александр", "Орлов", 200001, "pass2001", "male"),
            ("Никита", "Лебедев", 200002, "pass2002", "male"),
            ("Роман", "Егоров", 200003, "pass2003", "male"),
            ("Станислав", "Комаров", 200004, "pass2004", "male"),
            ("Вадим", "Щербаков", 200005, "pass2005", "male"),
            ("Татьяна", "Максимова", 200006, "pass2006", "female"),
            ("Екатерина", "Фомина", 200007, "pass2007", "female"),
            ("Светлана", "Давыдова", 200008, "pass2008", "female"),
            ("Людмила", "Беляева", 200009, "pass2009", "female"),
            ("Галина", "Гаврилова", 200010, "pass2010", "female"),
            
            # Студенты, которые просто в базе (3 человека)
            ("Виктор", "Титов", 300001, "pass3001", "male"),
            ("Аркадий", "Субботин", 300002, "pass3002", "male"),
            ("Лариса", "Федотова", 300003, "pass3003", "female"),
        ]
        cursor.executemany("INSERT INTO Student (Name, Surname, student_ticket, password, gender) VALUES (?, ?, ?, ?, ?)", students)
        print("Добавлены студенты.")

    # Расселение студентов по комнатам (случайное распределение)
    cursor.execute("SELECT COUNT(*) FROM Stud_room")
    if cursor.fetchone()[0] == 0:
        
        def settle_students(room_id, student_ids):
            for student_id in student_ids:
                try:
                    cursor.execute("INSERT INTO Stud_room (Student_ID, Room_ID) VALUES (?, ?)", (student_id, room_id))
                except sqlite3.IntegrityError:
                    pass
        
        # Получаем всех студентов, которые должны быть заселены (первые 20)
        cursor.execute("SELECT ID, gender FROM Student WHERE ID <= 20")
        students_to_settle = cursor.fetchall()
        
        # Расселяем студентов по комнатам соответствующего пола
        for student_id, gender in students_to_settle:
            cursor.execute('''
                SELECT r.ID 
                FROM Room r 
                LEFT JOIN Stud_room sr ON r.ID = sr.Room_ID 
                WHERE r.gender = ?
                GROUP BY r.ID 
                HAVING COUNT(sr.Student_ID) < r.Num_resid
                LIMIT 1
            ''', (gender,))
            
            room_result = cursor.fetchone()
            if room_result:
                room_id = room_result[0]
                settle_students(room_id, [student_id])
        
        print("Расселение завершено.")

    # Добавление типов заявок
    cursor.execute("SELECT COUNT(*) FROM Type_request")
    if cursor.fetchone()[0] == 0:
        type_requests = [
            ("Заселение", "Заявка на заселение в комнату"),
            ("Выселение", "Заявка на выселение"),
            ("Переселение", "Заявка на переселение"),
        ]
        cursor.executemany("INSERT INTO Type_request (name, comment) VALUES (?, ?)", type_requests)
        print("Добавлены типы заявок.")

    # Добавление заявок
    cursor.execute("SELECT COUNT(*) FROM Request")
    if cursor.fetchone()[0] == 0:
        requests = [
            # Заявки на заселение от новых студентов (10 человек)
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
            
            # Заявки на выселение (5 человек)
            (2, "Выселение из общежития", "2025-01-25", 1, "Хочу выселиться из общежития"),
            (2, "Выселение из общежития", "2025-01-26", 2, "Хочу выселиться из общежития"),
            (2, "Выселение из общежития", "2025-01-27", 3, "Хочу выселиться из общежития"),
            (2, "Выселение из общежития", "2025-01-28", 4, "Хочу выселиться из общежития"),
            (2, "Выселение из общежития", "2025-01-29", 5, "Хочу выселиться из общежития"),
            
            # Заявки на переселение (3 человека)
            (3, "Переселение в другую комнату", "2025-01-30", 6, "Прошу переселить в другую комнату"),
            (3, "Переселение в другую комнату", "2025-01-31", 7, "Прошу переселить в другую комнату"),
            (3, "Переселение в другую комнату", "2025-02-01", 8, "Прошу переселить в другую комнату"),
            
        ]
        cursor.executemany("INSERT INTO Request (Type_request_ID, name, date, student_id, text) VALUES (?, ?, ?, ?, ?)", requests)
        print("Добавлены заявки.")

    conn.commit()
    conn.close()


def check_settlement(db_name: str = "hostel.db"):
    """
    Проверяет корректность расселения студентов.
    """
    conn = get_connection(db_name)
    cursor = conn.cursor()
    
    print("\n=== ПРОВЕРКА РАССЕЛЕНИЯ ===")
    
    cursor.execute('''
        SELECT 
            h.Num_hostel as Общежитие,
            r.Num_room as Комната,
            r.gender as Пол_комнаты,
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
        print(f"Общежитие {room[0]}, Комната {room[1]}: {room[2]} - {room[3]}/{room[4]} мест")
        if room[5]:
            print(f"  Студенты: {room[5]}")
    
    cursor.execute('''
        SELECT 
            r.gender as Пол_комнаты,
            s.gender as Пол_студента,
            COUNT(*) as Количество
        FROM Stud_room sr
        JOIN Room r ON sr.Room_ID = r.ID
        JOIN Student s ON sr.Student_ID = s.ID
        GROUP BY r.gender, s.gender
    ''')
    
    print("\n=== ПРОВЕРКА РАЗДЕЛЕНИЯ ПО ПОЛУ ===")
    gender_check = cursor.fetchall()
    for check in gender_check:
        print(f"Комната: {check[0]}, Студент: {check[1]} - {check[2]} чел.")
    
    conn.close()