import json
import os
from datetime import datetime

from models.course import Course
from models.student import Student


class SchoolSystem:

    def __init__(self):
        self.students = []
        self.courses = []
        self.registrations = {}
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        os.makedirs(self.data_dir, exist_ok=True)
        self.load_data(silent=True)

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def find_course(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    def prompt_non_empty(self, prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty. Please enter a value.")

    def student_field_exists(self, field_name, value, exclude_id=None):
        normalized_value = value.strip().lower()
        for student in self.students:
            if exclude_id and student.student_id == exclude_id:
                continue
            current_value = getattr(student, field_name, "")
            if isinstance(current_value, str) and current_value.strip().lower() == normalized_value:
                return True
        return False

    def course_registration_count(self, course_id):
        return sum(1 for courses in self.registrations.values() if course_id in courses)

    def available_slots(self, course):
        return int(course.capacity) - self.course_registration_count(course.course_id)

    def add_student(self):
        student_id = self.prompt_non_empty("Student ID: ")

        if self.find_student(student_id):
            print("Student ID already exists")
            return

        name = self.prompt_non_empty("Name: ")
        if self.student_field_exists("name", name):
            print("Student name already exists")
            return

        email = self.prompt_non_empty("Email: ")
        if "@" not in email:
            print("Email must contain @")
            return

        if self.student_field_exists("email", email):
            print("Email already exists")
            return

        phone = self.prompt_non_empty("Phone Number: ")
        if self.student_field_exists("phone_number", phone):
            print("Phone number already exists")
            return

        student = Student(student_id, name, email, phone)
        self.students.append(student)
        self.save_data(silent=True)
        print("Student added successfully")

    def view_students(self):
        if not self.students:
            print("No students found")
            return

        for student in sorted(self.students, key=lambda student: student.name.lower()):
            student.display()
            print()

    def search_student(self):
        student_id = self.prompt_non_empty("Student ID: ")
        student = self.find_student(student_id)

        if student:
            student.display()
            return

        print("Student not found")

    def add_course(self):
        course_id = self.prompt_non_empty("Course ID: ")

        if self.find_course(course_id):
            print("Course already exists")
            return

        course_name = self.prompt_non_empty("Course Name: ")
        trainer = self.prompt_non_empty("Trainer: ")
        capacity = self.prompt_non_empty("Capacity: ")

        if not capacity.isdigit() or int(capacity) <= 0:
            print("Course capacity must be a positive number")
            return

        course = Course(course_id, course_name, trainer, int(capacity))
        self.courses.append(course)
        self.save_data(silent=True)
        print("Course added successfully")

    def view_courses(self):
        if not self.courses:
            print("No courses found")
            return

        for course in sorted(self.courses, key=self.available_slots, reverse=True):
            course.display()
            print(f"Available Slots: {self.available_slots(course)}")
            print()

    def register_student(self):
        student_id = self.prompt_non_empty("Student ID: ")
        course_id = self.prompt_non_empty("Course ID: ")

        student = self.find_student(student_id)
        course = self.find_course(course_id)

        if not student:
            print("Student not found")
            return

        if not course:
            print("Course not found")
            return

        if self.available_slots(course) <= 0:
            print("Course is full")
            return

        if student_id not in self.registrations:
            self.registrations[student_id] = []

        if course_id in self.registrations[student_id]:
            print("Student already registered for this course")
            return

        self.registrations[student_id].append(course_id)
        registration_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        student.registration_dates[course_id] = registration_datetime
        self.save_data(silent=True)

        print("Student registered successfully")
        print(f"Registration Date/Time: {registration_datetime}")

    def view_students_in_course(self):
        course_id = self.prompt_non_empty("Course ID: ")
        found = False

        for student_id, courses in self.registrations.items():
            if course_id in courses:
                student = self.find_student(student_id)
                if student:
                    student.display()
                    registration_date = student.registration_dates.get(course_id, "N/A")
                    print(f"Registration Date: {registration_date}")
                    print()
                    found = True

        if not found:
            print("No students found for this course")

    def view_courses_for_student(self):
        student_id = self.prompt_non_empty("Student ID: ")

        if student_id not in self.registrations:
            print("No registrations found")
            return

        found = False

        for course_id in self.registrations[student_id]:
            course = self.find_course(course_id)
            if course:
                course.display()
                registration_date = self.find_student(student_id).registration_dates.get(course_id, "N/A")
                print(f"Registration Date: {registration_date}")
                print()
                found = True

        if not found:
            print("No courses found for this student")

    def save_data(self, silent=False):
        students_data = []
        courses_data = []

        for student in self.students:
            students_data.append({
                "student_id": student.student_id,
                "name": student.name,
                "email": student.email,
                "phone_number": student.phone_number,
                "registration_dates": student.registration_dates,
            })

        for course in self.courses:
            courses_data.append({
                "course_id": course.course_id,
                "course_name": course.course_name,
                "trainer": course.trainer,
                "capacity": course.capacity,
            })

        os.makedirs(self.data_dir, exist_ok=True)

        with open(os.path.join(self.data_dir, "students.json"), "w") as file:
            json.dump(students_data, file, indent=4)

        with open(os.path.join(self.data_dir, "courses.json"), "w") as file:
            json.dump(courses_data, file, indent=4)

        with open(os.path.join(self.data_dir, "registration.json"), "w") as file:
            json.dump(self.registrations, file, indent=4)

        if not silent:
            print("Data saved successfully")

    def load_data(self, silent=False):
        os.makedirs(self.data_dir, exist_ok=True)

        try:
            with open(os.path.join(self.data_dir, "students.json"), "r") as file:
                students_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            students_data = []

        try:
            with open(os.path.join(self.data_dir, "courses.json"), "r") as file:
                courses_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            courses_data = []

        try:
            with open(os.path.join(self.data_dir, "registration.json"), "r") as file:
                registrations_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            registrations_data = {}

        self.students = []
        self.courses = []
        self.registrations = {}

        for student in students_data:
            try:
                new_student = Student(
                    student["student_id"],
                    student["name"],
                    student["email"],
                    student["phone_number"],
                )
                if "registration_dates" in student:
                    new_student.registration_dates = student["registration_dates"]
                self.students.append(new_student)
            except KeyError:
                print("Skipped invalid student data")

        for course in courses_data:
            try:
                capacity = int(course["capacity"])
                if capacity > 0:
                    self.courses.append(Course(
                        course["course_id"],
                        course["course_name"],
                        course["trainer"],
                        capacity,
                    ))
            except (KeyError, ValueError):
                print("Skipped invalid course data")

        for student_id, courses in registrations_data.items():
            if self.find_student(student_id) and isinstance(courses, list):
                valid_courses = []
                for course_id in courses:
                    course = self.find_course(course_id)
                    if course and course_id not in valid_courses:
                        if self.course_registration_count(course_id) < int(course.capacity):
                            valid_courses.append(course_id)
                if valid_courses:
                    self.registrations[student_id] = valid_courses

        if not silent:
            print("Data loaded successfully")

    def delete_student(self):
        student_id = self.prompt_non_empty("Student ID to delete: ")
        student = self.find_student(student_id)

        if not student:
            print("Student not found")
            return

        confirm = input(f"Are you sure you want to delete student {student.name}? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion cancelled")
            return

        self.students.remove(student)
        if student_id in self.registrations:
            del self.registrations[student_id]
        self.save_data(silent=True)
        print("Student deleted successfully")

    def delete_course(self):
        course_id = self.prompt_non_empty("Course ID to delete: ")
        course = self.find_course(course_id)

        if not course:
            print("Course not found")
            return

        confirm = input(f"Are you sure you want to delete course {course.course_name}? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion cancelled")
            return

        self.courses.remove(course)
        for student_id in list(self.registrations.keys()):
            if course_id in self.registrations[student_id]:
                self.registrations[student_id].remove(course_id)
                if not self.registrations[student_id]:
                    del self.registrations[student_id]
        self.save_data(silent=True)
        print("Course deleted successfully")

    def update_student(self):
        student_id = self.prompt_non_empty("Student ID to update: ")
        student = self.find_student(student_id)

        if not student:
            print("Student not found")
            return

        print(f"\nCurrent Details:")
        student.display()

        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Email")
        print("3. Phone Number")
        print("4. All details")

        choice = self.prompt_non_empty("Choose option: ")

        if choice == "1":
            new_name = self.prompt_non_empty("New Name: ")
            if self.student_field_exists("name", new_name, exclude_id=student_id):
                print("Student name already exists")
                return
            student.name = new_name
            self.save_data(silent=True)
            print("Name updated successfully")

        elif choice == "2":
            new_email = self.prompt_non_empty("New Email: ")
            if "@" not in new_email:
                print("Invalid email format")
                return
            if self.student_field_exists("email", new_email, exclude_id=student_id):
                print("Email already exists")
                return
            student.email = new_email
            self.save_data(silent=True)
            print("Email updated successfully")

        elif choice == "3":
            new_phone = self.prompt_non_empty("New Phone Number: ")
            if self.student_field_exists("phone_number", new_phone, exclude_id=student_id):
                print("Phone number already exists")
                return
            student.phone_number = new_phone
            self.save_data(silent=True)
            print("Phone number updated successfully")

        elif choice == "4":
            new_name = self.prompt_non_empty("New Name: ")
            new_email = self.prompt_non_empty("New Email: ")
            new_phone = self.prompt_non_empty("New Phone Number: ")

            if "@" not in new_email:
                print("Invalid email format")
                return
            if self.student_field_exists("name", new_name, exclude_id=student_id):
                print("Student name already exists")
                return
            if self.student_field_exists("email", new_email, exclude_id=student_id):
                print("Email already exists")
                return
            if self.student_field_exists("phone_number", new_phone, exclude_id=student_id):
                print("Phone number already exists")
                return
            student.name = new_name
            student.email = new_email
            student.phone_number = new_phone
            self.save_data(silent=True)
            print("All details updated successfully")

        else:
            print("Invalid option")

    def update_course(self):
        course_id = self.prompt_non_empty("Course ID to update: ")
        course = self.find_course(course_id)

        if not course:
            print("Course not found")
            return

        print(f"\nCurrent Details:")
        course.display()

        print("\nWhat would you like to update?")
        print("1. Course Name")
        print("2. Trainer")
        print("3. Capacity")
        print("4. All details")

        choice = self.prompt_non_empty("Choose option: ")

        if choice == "1":
            new_name = self.prompt_non_empty("New Course Name: ")
            course.course_name = new_name
            self.save_data(silent=True)
            print("Course name updated successfully")

        elif choice == "2":
            new_trainer = self.prompt_non_empty("New Trainer: ")
            course.trainer = new_trainer
            self.save_data(silent=True)
            print("Trainer updated successfully")

        elif choice == "3":
            new_capacity = self.prompt_non_empty("New Capacity: ")
            if not new_capacity.isdigit() or int(new_capacity) <= 0:
                print("Capacity must be a positive number")
                return
            if self.course_registration_count(course_id) > int(new_capacity):
                print("Cannot reduce capacity below current registration count")
                return
            course.capacity = int(new_capacity)
            self.save_data(silent=True)
            print("Capacity updated successfully")

        elif choice == "4":
            new_name = self.prompt_non_empty("New Course Name: ")
            new_trainer = self.prompt_non_empty("New Trainer: ")
            new_capacity = self.prompt_non_empty("New Capacity: ")
            if not new_capacity.isdigit() or int(new_capacity) <= 0:
                print("Invalid input. Update cancelled")
                return
            if self.course_registration_count(course_id) > int(new_capacity):
                print("Cannot reduce capacity below current registration count")
                return
            course.course_name = new_name
            course.trainer = new_trainer
            course.capacity = int(new_capacity)
            self.save_data(silent=True)
            print("All course details updated successfully")

        else:
            print("Invalid option")

    def show_available_slots(self):
        course_id = self.prompt_non_empty("Course ID: ")
        course = self.find_course(course_id)

        if not course:
            print("Course not found")
            return

        registered = self.course_registration_count(course_id)
        available = self.available_slots(course)

        print(f"\n--- Course: {course.course_name} ---")
        print(f"Total Capacity: {course.capacity}")
        print(f"Registered Students: {registered}")
        print(f"Available Slots: {available}")

    def export_report(self):
        filename = self.prompt_non_empty("Enter filename for report (without .txt): ")
        filename = filename + ".txt"

        with open(filename, "w") as file:
            file.write("=" * 60 + "\n")
            file.write("STUDENT COURSE REGISTRATION REPORT\n")
            file.write("=" * 60 + "\n\n")
            file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            file.write("-" * 60 + "\n")
            file.write("STUDENTS\n")
            file.write("-" * 60 + "\n\n")
            if not self.students:
                file.write("No students found\n\n")
            else:
                for i, student in enumerate(sorted(self.students, key=lambda s: s.name.lower()), 1):
                    file.write(f"{i}. Student ID: {student.student_id}\n")
                    file.write(f"   Name: {student.name}\n")
                    file.write(f"   Email: {student.email}\n")
                    file.write(f"   Phone: {student.phone_number}\n")
                    course_list = self.registrations.get(student.student_id, [])
                    if course_list:
                        file.write("   Registered Courses:\n")
                        for course_id in course_list:
                            date = student.registration_dates.get(course_id, "N/A")
                            file.write(f"     - {course_id} ({date})\n")
                    file.write("\n")

            file.write("-" * 60 + "\n")
            file.write("COURSES\n")
            file.write("-" * 60 + "\n\n")
            if not self.courses:
                file.write("No courses found\n\n")
            else:
                for i, course in enumerate(sorted(self.courses, key=self.available_slots, reverse=True), 1):
                    file.write(f"{i}. Course ID: {course.course_id}\n")
                    file.write(f"   Name: {course.course_name}\n")
                    file.write(f"   Trainer: {course.trainer}\n")
                    file.write(f"   Capacity: {course.capacity}\n")
                    registered = self.course_registration_count(course.course_id)
                    file.write(f"   Registered Students: {registered}\n")
                    file.write(f"   Available Slots: {self.available_slots(course)}\n")
                    file.write("\n")

        print(f"Report exported to {filename}")

    def delete_report(self):
        filename = self.prompt_non_empty("Enter filename to delete (without .txt): ")
        filename = filename + ".txt"

        try:
            confirm = input(f"Are you sure you want to delete {filename}? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Deletion cancelled")
                return

            os.remove(filename)
            print(f"Report {filename} deleted successfully")
        except FileNotFoundError:
            print(f"Report file {filename} not found")
        except Exception as e:
            print(f"Error deleting file: {e}")
