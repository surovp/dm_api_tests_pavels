from pydantic import BaseModel, StrictStr


class LoginCredentialsModel(BaseModel):
    login: StrictStr
    password: StrictStr
    remember_me: bool
