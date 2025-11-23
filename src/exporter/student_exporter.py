
import json
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
import yaml
import os
from pathlib import Path
from src.database.db import get_connection

class StudentExporter:
    def __init__(self, db_name: str = "hostel.db"):
        self.db_name = db_name
        self.output_dir = Path("out")
        
    def ensure_output_dir(self):
        """Создает папку out, если её нет"""
        self.output_dir.mkdir(exist_ok=True)
    
    def get_students_data(self):
        """Извлекает всех студентов из базы данных"""
        conn = get_connection(self.db_name)
        cursor = conn.cursor()
        
        
        cursor.execute("PRAGMA table_info(Student)")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]
        
        
        cursor.execute("SELECT * FROM Student")
        students = cursor.fetchall()
        
        conn.close()
        
        
        students_data = []
        for student in students:
            student_dict = {}
            for i, column_name in enumerate(column_names):
                student_dict[column_name] = student[i]
            students_data.append(student_dict)
        
        return students_data
    
    def export_to_json(self, students_data):
        """Экспортирует данные в JSON"""
        file_path = self.output_dir / "data.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(students_data, f, ensure_ascii=False, indent=2)
        print(f"Данные экспортированы в {file_path}")
    
    def export_to_csv(self, students_data):
        """Экспортирует данные в CSV"""
        file_path = self.output_dir / "data.csv"
        
        if not students_data:
        
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([])
            return
        
        
        fieldnames = students_data[0].keys()
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students_data)
        
        print(f"Данные экспортированы в {file_path}")
    
    def export_to_xml(self, students_data):
        """Экспортирует данные в XML"""
        file_path = self.output_dir / "data.xml"
        
        root = ET.Element("students")
        
        for student in students_data:
            student_elem = ET.SubElement(root, "student")
            for key, value in student.items():
                field_elem = ET.SubElement(student_elem, key)
                field_elem.text = str(value)
        
        
        xml_str = ET.tostring(root, encoding='utf-8')
        parsed_xml = minidom.parseString(xml_str)
        pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding='utf-8')
        
        
        pretty_xml_str = pretty_xml.decode('utf-8')
        pretty_xml_str = '\n'.join([line for line in pretty_xml_str.split('\n') if line.strip()])
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml_str)
        
        print(f"Данные экспортированы в {file_path}")
    
    def export_to_yaml(self, students_data):
        """Экспортирует данные в YAML"""
        file_path = self.output_dir / "data.yaml"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(students_data, f, allow_unicode=True, default_flow_style=False)
        
        print(f"Данные экспортированы в {file_path}")
    
    def export_all_formats(self):
        """Экспортирует данные во всех требуемых форматах"""
        try:
            self.ensure_output_dir()
            students_data = self.get_students_data()
            
            if not students_data:
                print("Нет данных студентов для экспорта")
                return
            
            print(f"Найдено {len(students_data)} студентов для экспорта")
            
            self.export_to_json(students_data)
            self.export_to_csv(students_data)
            self.export_to_xml(students_data)
            self.export_to_yaml(students_data)
            
            print("Экспорт всех форматов завершен успешно!")
            
        except Exception as e:
            print(f"Ошибка при экспорте данных: {e}")
            raise