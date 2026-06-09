# Project Reflection

## 1. What was the hardest part of this project?

The hardest part of this project was implementing the registration logic. I had to ensure that students could not register for the same course more than once and that courses could not exceed their capacity. Managing the relationships between students, courses, and registrations required careful planning and testing.Adding the date and time of registration and deleting option on the admins end.

## 2. Which classes did you create and why?

I created the following classes:

### Person

The Person class serves as a base class and stores common information such as name, email, and phone number.

### Student

The Student class inherits from Person and adds the student_id attribute. It represents individual students in the system.

### Course

The Course class stores information about courses, including the course ID, course name, trainer, and capacity.

### SchoolSystem

The SchoolSystem class manages the main functionality of the application. It handles student management, course management, registrations, searching, file saving, deletion, and file loading.

## 3. How does your registration logic prevent duplicate registrations?

Before registering a student for a course, the system checks whether the student is already registered for that course. If the course ID already exists in the student's registration record, the registration is rejected and an appropriate message is displayed.

## 4. How does your system check if a course is full?

The system counts the number of students currently registered for a course and compares it with the course capacity. If the number of registered students is equal to or greater than the course capacity, the registration is denied and the user is informed that the course is full.

## 5. What bugs did you face and how did you fix them?

One of the main bugs I encountered was a module import error caused by running files from the wrong directory. I fixed this by using the correct project structure and imports.

I also encountered issues when loading and saving JSON files. Some files were empty or incorrectly formatted, which caused errors. I fixed this by initializing the JSON files with valid empty structures such as [] and {} and adding error handling.

Another issue was duplicate student and course entries. I solved this by checking existing IDs before adding new records.

## 6. Which part of the code would you improve if you had more time?

If I had more time, I would improve the user interface by making the menus more interactive and user-friendly.implement better data validation, and improve the reporting system by generating detailed registration reports.
