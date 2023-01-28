from pydantic import BaseModel, validator, EmailStr


class VcacCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr

    @validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not (v and v.strip()):
            raise ValueError('Empty Value is not Allowed')
        return v

    @validator('password2')
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise ValueError('Not Correct Password')


class VcacGet(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
