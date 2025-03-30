from sqlalchemy.orm import Session
from app.db.models import Users
from app.schemas.user_schema import UserCreate, UserLogin
from app.auth.auth_handler import sign_jwt, verify_refresh_token, decode_jwt
from fastapi.exceptions import HTTPException
from app.auth.security import hash_password, verify_password
from app.schemas.auth import RefreshTokenRequest
from fastapi import Response

def creating_user(db: Session, user: UserCreate):
    existing_user = db.query(Users).filter(Users.login == user.login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    hashed_pass = hash_password(user.password)
    new_user = Users(login=user.login, password=hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    tokens = sign_jwt(new_user.login)

    return {
        "user": {"id": new_user.id, "login": new_user.login},
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"]
    }

def loggining_user(db: Session, user: UserLogin):
    existing_user = db.query(Users).filter(Users.login == user.login).first()

    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Ошибка входа")
    
    return sign_jwt(user.login)

def refreshing_users_token(request: RefreshTokenRequest):
    login = verify_refresh_token(request.refresh_token)
    if not login:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token") 
    
    return sign_jwt(login)

def get_users_info(db: Session, token: str) -> Response:
    payload = decode_jwt(token)
    
    if not payload:  
        return Response(status_code=401) 
    
    query = db.query(Users.id, Users.login).filter(Users.login == payload["login"]).first()
    
    if not query: 
        return Response(status_code=401)  
    
    return Response(status_code=200)  
