"""
Buisness logic module. Holds all of the class instances and methods
for interacting with the models database module.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Student, Grade, build_tables
import settings


class StudentManager:

    """Class repsonsible for managing our models and interactions with our models."""

    def __init__(self) -> None:
        self.engine = create_engine(settings.DB_ADDRESS)
        build_tables(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @property
    def get_session(self):

        """Create new session with current engine."""

        return self.Session()

    def add_student(self, name, surname, date_of_birth, email, phone_number):

        """Creates a new student model and adds new student to database."""

        new_student = Student(name=name,
                              surname=surname,
                              date_of_birth=date_of_birth,
                              email=email,
                              phone_number=phone_number)
        with self.get_session as session:
            session.add(new_student)
            session.commit()

    def remove_student(self, student_id):

        """Removes student with given ID from database."""

        with self.get_session as session:
            student = session.query(Student).filter(Student.id == student_id).first()
            if student:
                session.delete(student)
                session.commit()
                return True
            else:
                return False

    def get_student(self, student_id):

        """Gets student with given ID from database and returns a string representation."""

        with self.get_session as session:
            result = session.query(Student).filter(Student.id == student_id).first()
            return str(result)

    def update_student_email(self, student_id, new_email):

        """Updates email address of student with given ID"""

        with self.get_session as session:
            student = session.query(Student).filter(Student.id == student_id).first()
            student.email = new_email
            session.query(Student).filter(Student.id == student_id).first()
            session.commit()

    def view_all_students(self):

        """Retrieve all student from database and print a basic string representation."""

        with self.get_session as session:
            result = session.query(Student).all()
            for student in result:
                print(f"{student.id} - {student.name} {student.surname}")

    def add_grade(self, student_id, subject, grade):

        """Creates a new grade for a given student."""

        new_grade = Grade(student_id=student_id, subject=subject, grade=grade)
        with self.get_session as session:
            result = session.query(Student).filter(Student.id == student_id).first()
            if result:
                session.add(new_grade)
                session.commit()

    def view_grade(self, student_id):
        
        """View all grades of a given student"""

        with self.get_session as session:
            grades = session.query(Grade).filter(Grade.student_id == student_id).all()
            if grades:
                return [(grade.subject, grade.grade) for grade in grades]
            else:
                return None

