from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_handler import decode_jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):  # ✅ Изменяем на False, чтобы вручную управлять ошибками
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if credentials is None:
            raise HTTPException(status_code=401, detail="Missing authorization header")  # ✅ Было 403, теперь 401

        if credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")  # ✅ Было 403, теперь 401

        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=401, detail="Invalid token or expired token")  # ✅ Было 403, теперь 401

        return credentials.credentials

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decode_jwt(jwtoken)
            return bool(payload)
        except:
            return False
