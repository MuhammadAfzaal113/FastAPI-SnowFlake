from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    name: str
    email: EmailStr


class ClientUpdate(BaseModel):
    name: str = None
    email: EmailStr = None
