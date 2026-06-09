from services.school_system import SchoolSystem

# Simple admin credentials
ADMIN_PASSWORD = "admin123"

def admin_login():
    """Simple admin login system"""
    print("\n===== ADMIN LOGIN =====")
    password = input("Enter admin password: ").strip()
    
    if password == ADMIN_PASSWORD:
        print("Login successful!")
        return True
    else:
        print("Incorrect password. Access denied.")
        return False

def main_menu():
    system = SchoolSystem()
    is_admin = False
    
    while True:
        print("\n===== Student Course Registration System =====")
        
        # Show admin status
        if is_admin:
            print("[ADMIN MODE ENABLED]\n")
            print("--- Basic Operations ---")
            print("1. Add Student")
            print("2. View Students (Sorted Alphabetically)")
            print("3. Search Student")
            print("4. Add Course")
            print("5. View Courses (Sorted by Available Slots)")
            print("6. Register Student to Course (with Date/Time)")
            print("7. View Students in a Course")
            print("8. View Courses for a Student")
            print("9. Show Available Slots in Course")
            
            print("\n--- Admin Operations ---")
            print("10. Update Student Details")
            print("11. Update Course Details")
            print("12. Delete Student")
            print("13. Delete Course")
            print("14. Export Report to File")
            print("15. Delete Report File")
            
            print("\n--- Data Management ---")
            print("16. Save Data")
            print("17. Load Data")
            print("18. Logout (Admin Mode)")
            print("0. Exit")
        else:
            print("--- Main Operations ---")
            print("1. Add Student")
            print("2. View Students (Sorted Alphabetically)")
            print("3. Search Student")
            print("4. Add Course")
            print("5. View Courses (Sorted by Available Slots)")
            print("6. Register Student to Course (with Date/Time)")
            print("7. View Students in a Course")
            print("8. View Courses for a Student")
            print("9. Show Available Slots in Course")
            
            print("\n--- Data Management ---")
            print("10. Save Data")
            print("11. Load Data")
            print("12. Admin Login")
            print("0. Exit")

        choice = input("\nChoose option: ").strip()

        if is_admin:
            # Admin mode options
            if choice == "1":
                system.add_student()
            elif choice == "2":
                system.view_students()
            elif choice == "3":
                system.search_student()
            elif choice == "4":
                system.add_course()
            elif choice == "5":
                system.view_courses()
            elif choice == "6":
                system.register_student()
            elif choice == "7":
                system.view_students_in_course()
            elif choice == "8":
                system.view_courses_for_student()
            elif choice == "9":
                system.show_available_slots()
            elif choice == "10":
                system.update_student()
            elif choice == "11":
                system.update_course()
            elif choice == "12":
                system.delete_student()
            elif choice == "13":
                system.delete_course()
            elif choice == "14":
                system.export_report()
            elif choice == "15":
                system.delete_report()
            elif choice == "16":
                system.save_data()
            elif choice == "17":
                system.load_data()
            elif choice == "18":
                print("Logged out from admin mode")
                is_admin = False
            elif choice == "0":
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

        else:
            # Regular user mode options
            if choice == "1":
                system.add_student()
            elif choice == "2":
                system.view_students()
            elif choice == "3":
                system.search_student()
            elif choice == "4":
                system.add_course()
            elif choice == "5":
                system.view_courses()
            elif choice == "6":
                system.register_student()
            elif choice == "7":
                system.view_students_in_course()
            elif choice == "8":
                system.view_courses_for_student()
            elif choice == "9":
                system.show_available_slots()
            elif choice == "10":
                system.save_data()
            elif choice == "11":
                system.load_data()
            elif choice == "12":
                if admin_login():
                    is_admin = True
            elif choice == "0":
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()