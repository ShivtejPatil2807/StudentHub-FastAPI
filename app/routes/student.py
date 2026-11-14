from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services import student as student_service


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# GET: All students
@router.get("", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return student_service.get_all_students(db)


# GET: Search students
@router.get("/search", response_model=list[StudentResponse])
def search_students(name: str, db: Session = Depends(get_db)):
    return student_service.search_students(db, name)


# GET: Single student
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = student_service.get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# POST: Add student
@router.post("", status_code=201)
def add_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    try:
        new_student = student_service.create_student(db, student_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return {
        "message": "Student added successfully",
        "student": new_student
    }


# PUT: Update student
@router.put("/{student_id}")
def update_student(
    student_id: int,
    updated_data: StudentCreate,
    db: Session = Depends(get_db)
):
    try:
        student = student_service.update_student(
            db, student_id, updated_data
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "message": "Student updated successfully",
        "student": student
    }


# DELETE: Remove student
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = student_service.get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Save the response data before deleting the database record
    student_data = {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "course": student.course
    }

    student_service.delete_student(db, student_id)

    return {
        "message": "Student deleted successfully",
        "student": student_data
    }
