import json

from models.student import Student
from models.course import Course


class SchoolSystem:

    def __init__(self):
        self.students = []
        self.courses = []
        self.registrations = {}
    def add_student(self):
        student_id = input("Student ID: ")

        if not student_id:
            print("Student ID cannot be empty")
            return

        for student in self.students:
            if student.student_id == student_id:
                print("Student already exists")
                return

        name = input("Name: ")
        email = input("Email: ")
        phone = input("Phone Number: ")

        student = Student(
            student_id,
            name,
            email,
            phone
        )

        self.students.append(student)

        print("Student added successfully")
