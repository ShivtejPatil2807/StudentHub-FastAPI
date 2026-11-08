from pydantic import BaseModel, EmailStr, Field, ConfigDict


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    course: str = Field(min_length=2, max_length=100)

    model_config = ConfigDict(str_strip_whitespace=True)


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    course: str
