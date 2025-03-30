from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.cruds.user_crud import creating_user, loggining_user, refreshing_users_token, get_users_info
from app.schemas.user_schema import UserCreate, UserLogin
from app.auth.auth_bearer import JWTBearer
from app.schemas.auth import Login, RefreshTokenRequest, SignUp

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sign-up", response_model=SignUp)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return creating_user(db, user)

@router.post("/login", response_model=Login) 
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return loggining_user(db, user)

@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest):
    return refreshing_users_token(request)

@router.get("/validate", dependencies=[Depends(JWTBearer())])
def info_user(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    return get_users_info(db, token)
