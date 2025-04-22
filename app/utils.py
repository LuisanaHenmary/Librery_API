from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.auth import ALGORITHM, SECRET_KEY, jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"username": username, "is_admin": is_admin}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def require_admin(user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Solo para administradores")
    return user
