from models.person import Person

class Student(Person):

    def __init__(self, student_id, name, email, phone_number):
        super().__init__(name, email, phone_number)
        self.student_id = student_id

    def display(self):
        print(f"Student ID: {self.student_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone_number}")