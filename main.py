from fastapi import FastAPI ,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()

posts =[
    {"PR" : 1, "Title":"APEX"},
    {"PR" : 2, "Title":"NEURON"},
    {"PR" : 3, "Title":"ULTRON"}
]

@app.get("/")
def home(request : Request):
    return templates.TemplateResponse(request ,
        "index.html",
        {
            "posts":posts,
            "username":"Patil Shivtej",
            "course":"Super Intelligence",
        }
    )

@app.get("/api/posts",include_in_schema=False)
def get_posts():
    return posts