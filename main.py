from typing import *



from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PATH =BASE_DIR /'db.sqlite3'

from sqlmodel import (
    SQLModel,
    create_engine,
    Session,
    Field,
    Relationship

)

engine = create_engine(f'sqlite:///{DB_PATH}')

class Student(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str = Field(nullable=False, unique=False, max_length=20, min_length=10 )
    age : int = Field(nullable=False, unique=True, max_length=10, min_length=5)
class Course(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str = Field(nullable=False, unique=False, max_length=20, min_length=10 )
    credit : int =Field(nullable=False, unique=False, max_length=15, min_length=10)

class Grade(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    course_id: int = Field(foreign_key="course.id")
    score : float = Field(nullable=False, max_length=5, min_length=4)
student: Student = Relationship(back_populates="grades")
course: Course = Relationship(back_populates="grades")

def create_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as sesion:
        yield sesion
create_table()


def add_student(name: str, age: int):
    with Session(engine) as session:
        student = Student(name=name, age=age)
        session.add(student)
        session.commit()
        session.refresh(student)
        return student
if __name__ == "__main__":
    create_table()
    name = input("nhập vào tên:")
    age = (input("nhập vào tuổi:"))
    s1 = add_student(name, age)
    print("Thêm:", s1)
