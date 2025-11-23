# src/models/models.py

from dataclasses import dataclass

@dataclass
class Command:
    id: int
    name: str
    surname: str
    password: str

@dataclass
class Hostel:
    id: int
    num_hostel: int
    count_rooms: int
    command_id: int

@dataclass
class Room:
    id: int
    num_resid: int
    num_room: int
    hostel_id: int

@dataclass
class StudRoom:
    id: int
    student_id: int
    room_id: int

@dataclass
class Student:
    id: int
    name: str
    surname: str
    student_ticket: int
    password: str
    
@dataclass
class TypeRequest:
    id: int
    name: str
    comment: str

@dataclass
class Request:
    id: int
    type_request_id: int
    name: str
    date: str
    student_id: int
    text: str