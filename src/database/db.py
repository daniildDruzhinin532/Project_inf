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
            special_group TEXT,  -- Специальная группа (например, 'Вера', 'Радиофизик')
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
    Вставляет тестовые записи в таблицы с учетом разделения по полу на уровне комнат.
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

    # Проверка и добавление общежитий (теперь смешанные)
    cursor.execute("SELECT COUNT(*) FROM Hostel")
    if cursor.fetchone()[0] == 0:
        hostels = [
            (1, 100, 1),  # Общежитие 1 со 100 комнатами
            (2, 150, 2),  # Общежитие 2 со 150 комнатами
        ]
        cursor.executemany("INSERT INTO Hostel (Num_hostel, count_rooms, Command_ID) VALUES (?, ?, ?)", hostels)
        print("Добавлены общежития.")

    # Проверка и добавление комнат с указанием пола и специальных групп
    cursor.execute("SELECT COUNT(*) FROM Room")
    if cursor.fetchone()[0] == 0:
        # Комнаты в общежитии 1 (смешанные по полу)
        hostel1_rooms = [
            # Мужские комнаты
            (4, 101, 1, 'male', 'Радиофизик'),    # Комната для радиофизиков
            (3, 102, 1, 'male', None),
            (4, 103, 1, 'male', None),
            # Женские комнаты  
            (4, 201, 1, 'female', 'Вера'),        # Комната для всех Вер
            (3, 202, 1, 'female', None),
            (4, 203, 1, 'female', None),
        ]
        
        # Комнаты в общежитии 2 (смешанные по полу)
        hostel2_rooms = [
            # Мужские комнаты
            (3, 301, 2, 'male', None),
            (4, 302, 2, 'male', None),
            # Женские комнаты
            (3, 401, 2, 'female', None),
            (4, 402, 2, 'female', None),
        ]
        
        cursor.executemany("INSERT INTO Room (Num_resid, Num_room, Hostel_ID, gender, special_group) VALUES (?, ?, ?, ?, ?)",
                        hostel1_rooms + hostel2_rooms)
        print("Добавлены комнаты.")

    # Проверка и добавление студентов с указанием пола
    cursor.execute("SELECT COUNT(*) FROM Student")
    if cursor.fetchone()[0] == 0:
        students = [
            # Мужчины
            ("Радиофизик1", "Лентяев", 123456, "studpass1", "male"),
            ("Витюха", "Битый", 222333, "studpass4", "male"),
            ("Илюха", "Химик", 333444, "studpass5", "male"),
            ("Жека", "Покойник", 444555, "studpass6", "male"),
            ("Батрых", "Редько", 555666, "studpass7", "male"),
            ("Павел", "Башмачников", 666777, "studpass8", "male"),
            ("Жорка", "Змей", 777888, "studpass9", "male"),
            ("Радиофизик2", "Пузанов", 888999, "studpass10", "male"),
            ("Вова", "Винт", 999000, "studpass11", "male"),
            ("Дима", "Космос", 100101, "studpass12", "male"),
            ("Артем", "Исаев", 101102, "studpass13", "male"),
            ("Радиофизик3", "Дотеров", 103104, "studpass15", "male"),
            ("Константин", "Изфильма", 105106, "studpass17", "male"),
            
            # Женщины
            ("Вера", "Староверовна", 654321, "studpass2", "female"),
            ("Вера", "Вперуновна", 111222, "studpass3", "female"),
            ("Светлана", "Попова", 102103, "studpass14", "female"),
            ("Юлия", "Лазарева", 104105, "studpass16", "female"),
            ("Наталья", "Андреева", 106107, "studpass18", "female"),
            ("Вера", "Ведовна", 107108, "studpass19", "female"),
            ("Вера", "Вбоговна", 108109, "studpass20", "female"),
        ]
        cursor.executemany("INSERT INTO Student (Name, Surname, student_ticket, password, gender) VALUES (?, ?, ?, ?, ?)", students)
        print("Добавлены студенты.")

    # Автоматическое расселение студентов по правилам
    cursor.execute("SELECT COUNT(*) FROM Stud_room")
    if cursor.fetchone()[0] == 0:
        
        # Функция для расселения студентов в комнату
        def settle_students(room_id, student_ids):
            for student_id in student_ids:
                try:
                    cursor.execute("INSERT INTO Stud_room (Student_ID, Room_ID) VALUES (?, ?)", (student_id, room_id))
                except sqlite3.IntegrityError:
                    pass  # Уже расселен
        
        # 1. Расселяем радиофизиков в их специальную комнату
        cursor.execute('''
            SELECT ID FROM Room WHERE special_group = 'Радиофизик' AND gender = 'male'
        ''')
        radio_room_result = cursor.fetchone()
        if radio_room_result:
            radio_room_id = radio_room_result[0]
            cursor.execute("SELECT ID FROM Student WHERE Surname LIKE 'Радиофизик%' AND gender = 'male'")
            radio_students = [row[0] for row in cursor.fetchall()]
            if radio_students:
                settle_students(radio_room_id, radio_students)
                print(f"Расселены радиофизики в комнату {radio_room_id}")
        
        # 2. Расселяем студентов с именем Вера в их специальную комнату
        cursor.execute('''
            SELECT ID FROM Room WHERE special_group = 'Вера' AND gender = 'female'
        ''')
        vera_room_result = cursor.fetchone()
        if vera_room_result:
            vera_room_id = vera_room_result[0]
            cursor.execute("SELECT ID FROM Student WHERE Name = 'Вера' AND gender = 'female'")
            vera_students = [row[0] for row in cursor.fetchall()]
            if vera_students:
                settle_students(vera_room_id, vera_students)
                print(f"Расселены студентки с именем Вера в комнату {vera_room_id}")
        
        # 3. Расселяем остальных студентов в обычные комнаты с учетом пола
        cursor.execute("SELECT ID FROM Student WHERE ID NOT IN (SELECT Student_ID FROM Stud_room)")
        remaining_students = [row[0] for row in cursor.fetchall()]
        
        for student_id in remaining_students:
            # Определяем пол студента
            cursor.execute("SELECT gender FROM Student WHERE ID = ?", (student_id,))
            gender = cursor.fetchone()[0]
            
            # Находим подходящую комнату (того же пола, не переполненную, без специальной группы)
            cursor.execute('''
                SELECT r.ID 
                FROM Room r 
                LEFT JOIN Stud_room sr ON r.ID = sr.Room_ID 
                WHERE r.gender = ? AND r.special_group IS NULL
                GROUP BY r.ID 
                HAVING COUNT(sr.Student_ID) < r.Num_resid
                LIMIT 1
            ''', (gender,))
            
            room_result = cursor.fetchone()
            if room_result:
                room_id = room_result[0]
                settle_students(room_id, [student_id])
        
        print("Расселение завершено.")

    # Проверка и добавление типов заявок
    cursor.execute("SELECT COUNT(*) FROM Type_request")
    if cursor.fetchone()[0] == 0:
        type_requests = [
            ("Заселение", "Заявка на заселение в комнату"),
            ("Выселение", "Заявка на выселение"),
            ("Переселение", "Заявка на переселение"),
            ("Выселение за нарушение", "Административное выселение"),
        ]
        cursor.executemany("INSERT INTO Type_request (name, comment) VALUES (?, ?)", type_requests)
        print("Добавлены типы заявок.")

    # Проверка и добавление заявок
    cursor.execute("SELECT COUNT(*) FROM Request")
    if cursor.fetchone()[0] == 0:
        requests = [
            (1, "Заселение в общагу 1", "2025-11-01", 1, "Прошу заселить в комнату для радиофизиков"),
            (2, "Выселение", "2025-11-05", 2, "Прошу выселить"),
            (3, "Переселение", "2025-11-10", 3, "Прошу переселить в другую комнату"),
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
    
    # Проверяем комнаты с студентами
    cursor.execute('''
        SELECT 
            h.Num_hostel as Общежитие,
            r.Num_room as Комната,
            r.gender as Пол_комнаты,
            r.special_group as Группа,
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
        print(f"Общежитие {room[0]}, Комната {room[1]}: {room[2]} ({room[3] or 'обычная'}) - {room[4]}/{room[5]} мест")
        if room[6]:
            print(f"  Студенты: {room[6]}")
    
    # Проверяем разделение по полу
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