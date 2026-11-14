from sqlalchemy.orm import Session

from app.models import StudentModel
from app.schemas.student import StudentCreate


def get_all_students(db: Session):
    return db.query(StudentModel).all()


def search_students(db: Session, name: str):
    return (
        db.query(StudentModel)
        .filter(StudentModel.name.ilike(f"%{name}%"))
        .all()
    )


def get_student_by_id(db: Session, student_id: int):
    return (
        db.query(StudentModel)
        .filter(StudentModel.id == student_id)
        .first()
    )


def create_student(db: Session, student_data: StudentCreate):
    new_student = StudentModel(
        name=student_data.name,
        email=student_data.email,
        course=student_data.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def update_student(
    db: Session,
    student_id: int,
    updated_data: StudentCreate
):
    student = get_student_by_id(db, student_id)

    if student is None:
        return None

    student.name = updated_data.name
    student.email = updated_data.email
    student.course = updated_data.course

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)

    if student is None:
        return None

    db.delete(student)
    db.commit()

    return student
