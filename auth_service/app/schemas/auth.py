from pydantic import BaseModel

class Login(BaseModel):
    login: str
    access_token: str
    refresh_token: str

class UserResponse(BaseModel):
    id: int
    login: str

class SignUp(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
