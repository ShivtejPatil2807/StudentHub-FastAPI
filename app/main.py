
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

# Create FastAPI application
app = FastAPI(
    title="StudentHub",
    description="Student Management System",
    version="1.0.0"
)

# Configure Jinja2 templates
templates = Jinja2Templates(directory="app/templates")


# Home page
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "StudentHub"}
    )


# Test API endpoint
@app.get("/api")
def test_api():
    return {
        "message": "Welcome to StudentHub API!",
        "status": "Running successfully"
    }
