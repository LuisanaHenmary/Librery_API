from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    name: str = Field(...)
    ci: str = Field(...)
    email: str = Field(...)
    phone_number: str = Field(...)
    password: str = Field(...)
    is_admin: bool = False

class UserLogin(BaseModel):
    name: str = Field(...)
    password: str = Field(...)