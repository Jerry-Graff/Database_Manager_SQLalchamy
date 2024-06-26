"""
This is the main programme loop. The user interafce displays allows the
user to add to and explore the database of students. Defensive prorgamming
has been encourperated to account for unexpected inputs.
"""

from datetime import date
from student_manager import StudentManager
from utilities import draw_line
from constants import MAIN_MENU, STUDENT_EDIT_MENU


def main():
    """Main program loop ."""
    student_manager = StudentManager()

    while True:
        draw_line()
        print(MAIN_MENU)
        draw_line()
        user_option = input(": ").strip()
        if user_option == "0":
            break
        # View Students
        if user_option == "1":
            draw_line()
            print("Students:")
            draw_line()
            student_manager.view_all_students()
        # View Student Grades
        elif user_option == "2":
            draw_line()
            print("Students:")
            draw_line()
            student_manager.view_all_students()
            try:
                student_grade = int(input("Please enter the ID of the student you would like to view:\n"))
                grades = student_manager.view_grade(student_grade)
                if grades:
                    draw_line()
                    print("Grades:")
                    draw_line()
                    for subject, grade in grades:
                        print(f"{subject}: {grade}")
                else:
                    print("No grades found for the student.")
            except ValueError:
                print("Invalid input. Please enter a valid student ID.")
        # Update Student
        elif user_option == "3":
            try:
                student_id = int(input("Please enter the ID of the student you would like to edit:\n"))
                while True:
                    student = student_manager.get_student(student_id)
                    if not student:
                        print("No student found with that ID.")
                        break
                    draw_line()
                    print(student)
                    draw_line()
                    print(STUDENT_EDIT_MENU)
                    edit_option = input(": ").strip()
                    if edit_option == "0":
                        break
                    if edit_option == "1":
                        subject = input("Please enter a subject: ").strip()
                        try:
                            grade = int(input("Please enter the grade score: "))
                            student_manager.add_grade(student_id, subject, grade)
                        except ValueError:
                            print("Invalid input. Please enter a valid grade.")
                    elif edit_option == "2":
                        new_email = input("Please enter new email address: ").strip()
                        student_manager.update_student_email(student_id, new_email)
                    else:
                        print("Invalid option. Please choose a valid option.")
            except ValueError:
                print("Invalid input. Please enter a valid student ID.")
        # Add student
        elif user_option == "4":
            print("Please enter the following data to add a student:")
            name = input("Name: ").strip()
            surname = input("Surname: ").strip()
            date_of_birth = input("Date of Birth(DD-MM-YYYY): ").strip()
            try:
                day, month, year = map(int, date_of_birth.split('-'))
                date_of_birth = date(year, month, day)
                email = input("Email: ").strip()
                phone_number = input("Phone Number: ").strip()
                student_manager.add_student(name, surname, date_of_birth, email, phone_number)
            except ValueError:
                print("Invalid date format. Please enter the date in DD-MM-YYYY format.")
        # Delete Student
        elif user_option == "5":
            draw_line()
            print("Students:")
            draw_line()
            student_manager.view_all_students()
            draw_line()
            try:
                user_delete = int(input("Enter ID of student you would like to delete: "))
                print(f"Are you sure you would like to delete student: {user_delete}?")
                user_confirm = input("(Y/N): ").strip().upper()
                if user_confirm == "Y":
                    if student_manager.remove_student(user_delete):
                        print(f"Student {user_delete} Successfully Removed")
                    else:
                        print(f"Student {user_delete} is not a valid student. Please try again.")
                else:
                    print("Delete student cancelled")
            except ValueError:
                print("Invalid input. Please enter a valid student ID.")
        else:
            print("Invalid option. Please select a valid menu option.")


if __name__ == "__main__":
    main()
