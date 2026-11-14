from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.database import engine, Base
from app.models import StudentModel
from app.routes.student import router as student_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI
app = FastAPI(
    title="StudentHub",
    description="Student Management System",
    version="1.0.0"
)


# Templates
templates = Jinja2Templates(directory="app/templates")


# Register student routes
app.include_router(student_router)


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
