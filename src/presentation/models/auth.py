from pydantic import BaseModel


class LoginDataModel(BaseModel):
    login: str
    password: str


class LogoutResultModel(BaseModel):
    status: bool
