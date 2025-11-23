# main.py

from src.database.db import create_tables, insert_sample_data
from src.repository.repository import Repository
from src.exporter.student_exporter import StudentExporter
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
        print("5 - Обработать заявки")
        print("6 - Управление студентами в моём общежитии")
        print("7 - Экспорт данных студентов")
        print("0 - Выход")
        choice = input("Ваш выбор: ")

        if choice == "1":
            requests = repo.get_all_requests()
            print("\nСписок всех заявок:")
            for req in requests:
                student = repo.get_student(req.student_id)
                type_request = repo.get_type_request(req.type_request_id)
                print(f"{req.id}: {req.name} (Тип: {type_request.name}, Дата: {req.date}, Студент: {student.name} {student.surname}, Текст: {req.text})")

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

        elif choice == "5":
            process_requests_menu(repo, command_id)

        elif choice == "6":
            manage_students_menu(repo, command_id)

        elif choice == "7":
            export_data_menu()

        elif choice == "0":
            print("Выход из меню коменданта...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def manage_students_menu(repo, command_id):
    """Меню управления студентами в общежитии коменданта"""
    while True:
        print("\nУправление студентами:")
        print("1 - Показать студентов в моём общежитии")
        print("2 - Выселить студента из моего общежития")
        print("3 - Показать комнаты в моём общежитии")
        print("0 - Назад")
        choice = input("Ваш выбор: ")

        if choice == "1":
            students = repo.get_students_in_command_hostel(command_id)
            hostel = repo.get_hostel_by_command_id(command_id)
            print(f"\nСтуденты в вашем общежитии №{hostel.num_hostel}:")
            if students:
                for stud in students:
                    room = repo.get_student_room(stud.id)
                    print(f"{stud.id}: {stud.name} {stud.surname} (Комната: {room.num_room if room else 'Не заселен'})")
            else:
                print("В вашем общежитии нет студентов.")

        elif choice == "2":
            student_id = int(input("Введите ID студента для выселения: "))
            try:
                repo.evict_student_from_command_hostel(command_id, student_id)
                student = repo.get_student(student_id)
                print(f"Студент {student.name} {student.surname} выселен из вашего общежития.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "3":
            rooms = repo.get_rooms_in_command_hostel(command_id)
            hostel = repo.get_hostel_by_command_id(command_id)
            print(f"\nКомнаты в вашем общежитии №{hostel.num_hostel}:")
            if rooms:
                for room in rooms:
                    students_count = len(repo.get_students_in_room(room.id))
                    print(f"{room.id}: Комната {room.num_room}, Мест: {students_count}/{room.num_resid}")
            else:
                print("В вашем общежитии нет комнат.")

        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def process_requests_menu(repo, command_id):
    """Меню обработки заявок"""
    while True:
        print("\nОбработка заявок:")
        print("1 - Показать необработанные заявки")
        print("2 - Обработать конкретную заявку")
        print("0 - Назад")
        choice = input("Ваш выбор: ")

        if choice == "1":
            requests = repo.get_pending_requests()
            print("\nНеобработанные заявки:")
            if requests:
                for req in requests:
                    student = repo.get_student(req.student_id)
                    type_request = repo.get_type_request(req.type_request_id)
                    print(f"{req.id}: {type_request.name} - {req.name} (Студент: {student.name} {student.surname}, Дата: {req.date})")
            else:
                print("Нет необработанных заявок.")

        elif choice == "2":
            request_id = int(input("Введите ID заявки для обработки: "))
            request = repo.get_request(request_id)
            if not request:
                print("Заявка не найдена.")
                continue
                
            student = repo.get_student(request.student_id)
            type_request = repo.get_type_request(request.type_request_id)
            
            print(f"\nДетали заявки {request_id}:")
            print(f"Тип: {type_request.name}")
            print(f"Название: {request.name}")
            print(f"Студент: {student.name} {student.surname}")
            print(f"Дата: {request.date}")
            print(f"Текст: {request.text}")
            
            print("\nДействия:")
            print("1 - Одобрить заявку")
            print("2 - Отклонить заявку")
            print("0 - Отмена")
            action = input("Ваш выбор: ")
            
            if action == "1":
                process_approval(repo, request, student, type_request)
            elif action == "2":
                process_rejection(repo, request, student)
            elif action == "0":
                continue
            else:
                print("Неверный выбор.")

        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    def process_approval(repo, request, student, type_request):
        """Обработка одобрения заявки"""
        explanation = input("Введите пояснение для письма (или оставьте пустым): ")
        
        try:
            if request.type_request_id == 1: 
                free_rooms = repo.get_free_rooms()  # Заменили get_free_rooms_by_gender на get_free_rooms
                if not free_rooms:
                    print("Нет свободных комнат!")
                    return
                    
                print("\nДоступные комнаты:")
                for room in free_rooms:
                    print(f"{room.id}: Комната {room.num_room}, Общежитие {room.hostel_id}, Мест: {room.num_resid}")
                
                room_id = int(input("Введите ID комнаты для заселения: "))
                repo.settle_student(student.id, room_id)
                print(f"Студент {student.name} {student.surname} заселен в комнату {room_id}")
                
            elif request.type_request_id == 2:
                current_room = repo.get_student_room(student.id)
                if current_room:
                    repo.evict_student(student.id)
                    print(f"Студент {student.name} {student.surname} выселен из комнаты {current_room.id}")
                else:
                    print("Студент не проживает в общежитии")
                    
            elif request.type_request_id == 3:
                current_room = repo.get_student_room(student.id)
                if not current_room:
                    print("Студент не проживает в общежитии")
                    return
                    
                free_rooms = repo.get_free_rooms()  # Заменили get_free_rooms_by_gender на get_free_rooms
                print("\nДоступные комнаты для переселения:")
                for room in free_rooms:
                    print(f"{room.id}: Комната {room.num_room}, Общежитие {room.hostel_id}, Мест: {room.num_resid}")
                
                new_room_id = int(input("Введите ID новой комнаты: "))
                repo.transfer_student(student.id, new_room_id)
                print(f"Студент {student.name} {student.surname} переселен из комнаты {current_room.id} в комнату {new_room_id}")
            
            send_approval_email(student, request, explanation)
            repo.mark_request_processed(request.id)
            print("Заявка одобрена и письмо отправлено!")
            
        except Exception as e:
            print(f"Ошибка при обработке заявки: {e}")

def process_rejection(repo, request, student):
    """Обработка отклонения заявки"""
    explanation = input("Введите причину отклонения: ")
    
    send_rejection_email(student, request, explanation)
    repo.mark_request_processed(request.id)
    print("Заявка отклонена и письмо отправлено!")

def send_approval_email(student, request, explanation):
    """Имитация отправки письма об одобрении"""
    print(f"\n=== ПИСЬМО ОБ ОДОБРЕНИИ ===")
    print(f"Кому: {student.name} {student.surname}")
    print(f"Тема: Ваша заявка '{request.name}' одобрена")
    print(f"Сообщение: Ваша заявка от {request.date} была одобрена.")
    if explanation:
        print(f"Пояснение: {explanation}")
    print("=" * 40)

def send_rejection_email(student, request, explanation):
    """Имитация отправки письма об отклонении"""
    print(f"\n=== ПИСЬМО ОБ ОТКЛОНЕНИИ ===")
    print(f"Кому: {student.name} {student.surname}")
    print(f"Тема: Ваша заявка '{request.name}' отклонена")
    print(f"Сообщение: К сожалению, ваша заявка от {request.date} была отклонена.")
    print(f"Причина: {explanation}")
    print("=" * 40)

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
                    type_request = repo.get_type_request(req.type_request_id)
                    print(f"{req.id}: {req.name} (Тип: {type_request.name}, Дата: {req.date}, Текст: {req.text})")
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

def export_data_menu():
    """Меню для экспорта данных студентов"""
    print("\nЭкспорт данных студентов...")
    try:
        exporter = StudentExporter(DB_FILE)
        exporter.export_all_formats()
    except Exception as e:
        print(f"Ошибка при экспорте данных: {e}")
    input("Нажмите Enter для продолжения...")

def main():
    
    if not os.path.exists(DB_FILE):
        create_tables(DB_FILE)
        insert_sample_data(DB_FILE)

    repo = Repository(DB_FILE)

    
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
            surname = input("Введите фамилию: ")
            password = input("Введите пароль: ")
            command = repo.authenticate_command(surname, password)
            if command:
                print(f"Добро пожаловать, {command.name} {command.surname}!")
                command_menu(repo, command.id)
            else:
                print("Неверная фамилия или пароль для коменданта.")
                continue

        elif role == "2":
            surname = input("Введите фамилию: ")
            password = input("Введите пароль: ")
            student = repo.authenticate_student(surname, password)
            if student:
                print(f"Добро пожаловать, {student.name} {student.surname}!")
                student_menu(repo, student.id)
            else:
                print("Неверная фамилия или пароль для студента.")
        elif role not in [0, 1, 2]:
            print("Неправильный ввод выбора(числа от 0 до 2)")
            continue
    repo.close()

if __name__ == "__main__":
    main()