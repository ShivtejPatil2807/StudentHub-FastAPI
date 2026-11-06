from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="StudentHub",
    description="Student Management System",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")

# Temporary student data
students = [
    {
        "id": 1,
        "name": "Rahul",
        "email": "rahul@gmail.com",
        "course": "Computer Science"
    },
    {
        "id": 2,
        "name": "Priya",
        "email": "priya@gmail.com",
        "course": "Information Technology"
    }
]


# HOME PAGE
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "StudentHub"}
    )


# TEST API
@app.get("/api")
def test_api():
    return {"message": "StudentHub API is running!"}


# GET: All students
@app.get("/students")
def get_students():
    return students


# GET: Search students using query parameter
@app.get("/students/search")
def search_students(name: str):
    results = [
        student for student in students
        if name.lower() in student["name"].lower()
    ]

    return results


# GET: Single student using path parameter
@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# POST: Add new student
@app.post("/students", status_code=201)
def add_student(student: dict):

    new_student = {
        **student,
        "id": max(
            (s["id"] for s in students),
            default=0
        ) + 1
    }

    students.append(new_student)

    return {
        "message": "Student added successfully",
        "student": new_student
    }


# PUT: Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_data: dict):

    for index, student in enumerate(students):
        if student["id"] == student_id:

            students[index] = {
                **updated_data,
                "id": student_id
            }

            return {
                "message": "Student updated successfully",
                "student": students[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# DELETE: Remove student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for index, student in enumerate(students):
        if student["id"] == student_id:

            deleted_student = students.pop(index)

            return {
                "message": "Student deleted successfully",
                "student": deleted_student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
