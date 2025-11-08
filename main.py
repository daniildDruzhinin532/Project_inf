from src.database.db import create_tables, insert_sample_data
from src.repository.repository import Repository
import os

DB_FILE = "hostel.db"

def command_menu(repo, command_id):
    """Меню для коменданта"""
    while True:
        print("\nМеню коменданта:")
        print("1 - Показать все заявки студентов")
        print("2 - Показать студентов в комнате (введите ID комнаты)")
        print("3 - Показать свободные комнаты")
        print("4 - Показать всех студентов")
        print("0 - Выход")
        choice = input("Ваш выбор: ")

        if choice == "1":
            requests = repo.get_all_requests()
            print("\nСписок всех заявок:")
            for req in requests:
                student = repo.get_student(req.student_id)
                print(f"{req.id}: {req.name} (Дата: {req.date}, Студент: {student.name} {student.surname}, Текст: {req.text})")

        elif choice == "2":
            room_id = int(input("Введите ID комнаты: "))
            students = repo.get_students_in_room(room_id)
            print(f"\nСтуденты в комнате {room_id}:")
            if students:
                for stud in students:
                    print(f"{stud.id}: {stud.name} {stud.surname}")
            else:
                print("В комнате нет студентов.")

        elif choice == "3":
            rooms = repo.get_free_rooms()
            print("\nСвободные комнаты:")
            if rooms:
                for room in rooms:
                    print(f"{room.id}: Номер {room.num_room}, Мест: {room.num_resid}, Общежитие: {room.hostel_id}")
            else:
                print("Нет свободных комнат.")

        elif choice == "4":
            students = repo.get_all_students()
            print("\nСписок всех студентов:")
            for stud in students:
                print(f"{stud.id}: {stud.name} {stud.surname} (Билет: {stud.student_ticket})")

        elif choice == "0":
            print("Выход из меню коменданта...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def student_menu(repo, student_id):
    """Меню для студента"""
    while True:
        print("\nМеню студента:")
        print("1 - Подать новую заявку")
        print("2 - Показать мои заявки")
        print("3 - Показать мою комнату")
        print("0 - Выход")
        choice = input("Ваш выбор: ")

        if choice == "1":
            type_request_id = int(input("Введите ID типа заявки (1 - Заселение, 2 - Выселение, 3 - Переселение): "))
            name = input("Название заявки: ")
            date = input("Дата (YYYY-MM-DD): ")
            text = input("Текст заявки: ")
            new_id = repo.add_request(type_request_id, name, date, student_id, text)
            print(f"Добавлена заявка с ID {new_id}.")

        elif choice == "2":
            requests = repo.get_requests_by_student(student_id)
            print("\nМои заявки:")
            if requests:
                for req in requests:
                    print(f"{req.id}: {req.name} (Дата: {req.date}, Текст: {req.text})")
            else:
                print("У вас нет заявок.")

        elif choice == "3":
            room = repo.get_student_room(student_id)
            if room:
                print(f"Ваша комната: ID {room.id}, Номер {room.num_room}, Общежитие {room.hostel_id}, Мест {room.num_resid}")
            else:
                print("Вы не заселены в комнату.")

        elif choice == "0":
            print("Выход из меню студента...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def main():
    # Если базы нет, создаем таблицы и вставляем тестовые данные
    if not os.path.exists(DB_FILE):
        create_tables(DB_FILE)
        insert_sample_data(DB_FILE)

    repo = Repository(DB_FILE)

    # Авторизация
    while True:
        print("\nАвторизация:")
        print("1 - Войти как комендант")
        print("2 - Войти как студент")
        print("0 - Выход")
        role = input("Выберите роль: ")

        if role == "0":
            print("Выход из программы...")
            break

        if role == "1":
            command = repo.authenticate_command(surname, password)
            if command:
                print(f"Добро пожаловать, {command.name} {command.surname}!")
                command_menu(repo, command.id)
            else:
                print("Неверная фамилия или пароль для коменданта.")

        elif role == "2":
            student = repo.authenticate_student(surname, password)
            if student:
                print(f"Добро пожаловать, {student.name} {student.surname}!")
                student_menu(repo, student.id)
            else:
                print("Неверная фамилия или пароль для студента.")
        elif role != 1 and role != 2 and role != 0:
            print("Неправильный ввод выбора(числа от 0 до 2)")
            continue

        else:
            print("Неверный выбор роли.")
        surname = input("Введите фамилию: ")
        password = input("Введите пароль: ")

    repo.close()

if __name__ == "__main__":
    main()